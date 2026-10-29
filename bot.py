"""
OpsWatch Remediation Bot
-------------------------
This is your "automation" piece. It runs completely independently of the
dashboard, exactly like a scheduled RPA bot would in Automation Anywhere:

  1. Polls MySQL every few seconds for open incidents
  2. Decides what action to take based on severity
  3. Takes the action (here: simulated) and writes the result back to MySQL

Run with:  python bot.py
Leave it running in its own terminal while the dashboard is open.
"""

import mysql.connector
import time
import random

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "root",          # <-- same password as server.py
    "database": "opswatch",
}

POLL_INTERVAL_SECONDS = 5

# Simple "playbook" - in a real Automation Anywhere bot, each of these
# would be an actual bot action (restart service, clear disk, page on-call)
ACTIONS = {
    "watch": "Added to watchlist, no action needed yet",
    "critical": "Auto-remediation: service restarted, disk cache cleared",
}


def get_db():
    return mysql.connector.connect(**DB_CONFIG)


def process_open_incidents():
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM incidents WHERE status = 'open'")
    open_incidents = cur.fetchall()

    for incident in open_incidents:
        # Simulate the bot "working" on it (a real bot would run steps here)
        time.sleep(0.5)

        action = ACTIONS.get(incident["severity"], "Reviewed, no action available")

        # Only auto-resolve criticals - watch items just get logged and left open,
        # like a real triage bot escalating only what needs escalation
        if incident["severity"] == "critical":
            update = db.cursor()
            update.execute(
                """UPDATE incidents
                   SET status = 'resolved', action_taken = %s, resolved_at = NOW()
                   WHERE id = %s""",
                (action, incident["id"]),
            )
            db.commit()
            update.close()
            print(f"[BOT] Resolved incident #{incident['id']} ({incident['app_name']}): {action}")
        else:
            print(f"[BOT] Incident #{incident['id']} ({incident['app_name']}) left on watchlist")

    cur.close()
    db.close()


if __name__ == "__main__":
    print(f"OpsWatch bot started. Polling every {POLL_INTERVAL_SECONDS}s. Ctrl+C to stop.")
    while True:
        try:
            process_open_incidents()
        except Exception as e:
            print(f"[BOT] Error: {e}")
        time.sleep(POLL_INTERVAL_SECONDS)
