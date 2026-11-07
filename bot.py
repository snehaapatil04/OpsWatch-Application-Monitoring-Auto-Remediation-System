
"""
OpsWatch Remediation Bot
-------------------------
Polls MySQL for open incidents, records detection,
and performs simulated remediation for critical incidents.

Run: python bot.py
"""

import mysql.connector
import time

import os

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("root"),
    "database": os.getenv("DB_NAME", "opswatch")
},


POLL_INTERVAL_SECONDS = 5

ACTIONS = {
    "watch": "Added to watchlist, no action needed yet",
    "critical": "Simulated recovery: service restarted, disk cache cleared",
}


def get_db():
    return mysql.connector.connect(**DB_CONFIG)


def process_open_incidents():
    db = get_db()
    cur = db.cursor(dictionary=True)

    try:
        cur.execute(cur.execute("""
    SELECT * FROM incidents
    WHERE status = 'open' AND detected_at IS NULL
""")
        )
        incidents = cur.fetchall()

        for incident in incidents:
            incident_id = incident["id"]
            severity = incident["severity"]

            # Record detection only once
            if incident["detected_at"] is None:
                cur.execute(
                    """
                    UPDATE incidents
                    SET detected_at = NOW()
                    WHERE id = %s
                    """,
                    (incident_id,)
                )
                db.commit()

            if severity == "critical":
                action = ACTIONS["critical"]

                cur.execute(
                    """
                    UPDATE incidents
                    SET attempted_at = NOW()
                    WHERE id = %s
                    """,
                    (incident_id,)
                )
                db.commit()

                if incident["simulate_recovery_failure"]:
                    cur.execute(
                        """
                        UPDATE incidents
                        SET status = 'failed',
                            remediation_status = 'failed',
                            action_taken = %s
                        WHERE id = %s
                        """,
                        ("Simulated recovery failed", incident_id)
                    )
                    print(
                        f"[BOT] Recovery failed for incident #{incident_id}"
                    )

                else:
                    cur.execute(
                        """
                        UPDATE incidents
                        SET status = 'resolved',
                            remediation_status = 'succeeded',
                            action_taken = %s,
                            resolved_at = NOW()
                        WHERE id = %s
                        """,
                        (action, incident_id)
                    )
                    print(
                        f"[BOT] Resolved incident #{incident_id}"
                    )

                db.commit()

            else:
                cur.execute(
                    """
                    UPDATE incidents
                    SET remediation_status = 'not_required'
                    WHERE id = %s
                    """,
                    (incident_id,)
                )
                db.commit()

                print(
                    f"[BOT] Incident #{incident_id} remains on watchlist"
                )

    finally:
        cur.close()
        db.close()


if __name__ == "__main__":
    print(
        f"OpsWatch bot started. Polling every "
        f"{POLL_INTERVAL_SECONDS} seconds."
    )

    while True:
        try:
            process_open_incidents()
        except Exception as error:
            print(f"[BOT] Error: {error}")

        time.sleep(POLL_INTERVAL_SECONDS)
