
"""
OpsWatch Failure Injection Test
--------------------------------
Creates simulated incidents, waits for bot processing,
and calculates detection and remediation metrics.

Run this while server.py and bot.py are running.
"""

import time
import requests
import mysql.connector

API_URL = "http://127.0.0.1:5000/api/incidents"

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "root",
    "database": "opswatch",
}

TEST_COUNT = 20


def create_test_incidents():
    print("\nCreating simulated incidents...")

    for i in range(TEST_COUNT):
        data = {
            "app_name": "Test-Service",
            "severity": "critical",
            "cpu_percent": 90 + (i % 11),
            "disk_percent": 80 + (i % 21),
            "simulate_recovery_failure": i % 4 == 0,
        }

        response = requests.post(API_URL, json=data, timeout=10)
        response.raise_for_status()

        print(f"Created incident #{response.json()['id']}")

    print(f"\nSuccessfully created {TEST_COUNT} incidents.")


def get_test_results():
    db = mysql.connector.connect(**DB_CONFIG)
    cur = db.cursor(dictionary=True)

    try:
        cur.execute(
            """
            SELECT
                COUNT(*) AS total,
                SUM(detected_at IS NOT NULL) AS detected,
                SUM(remediation_status = 'succeeded') AS succeeded,
                SUM(remediation_status = 'failed') AS failed,
                AVG(
                    CASE
                        WHEN resolved_at IS NOT NULL
                        THEN TIMESTAMPDIFF(
                            SECOND, created_at, resolved_at
                        )
                    END
                ) AS avg_resolution_seconds
            FROM incidents
            WHERE app_name = 'Test-Service'
            """
        )

        return cur.fetchone()

    finally:
        cur.close()
        db.close()


if __name__ == "__main__":
    create_test_incidents()

    print("\nWaiting for bot to process incidents...")

    # Bot polls every 5 seconds; allow additional processing time.
    time.sleep(15)

    results = get_test_results()

    total = results["total"] or 0
    detected = results["detected"] or 0
    succeeded = results["succeeded"] or 0
    failed = results["failed"] or 0

    print("\n========== OPSWATCH TEST REPORT ==========")
    print(f"Total incidents: {total}")
    print(f"Detected incidents: {detected}")
    print(f"Successful recoveries: {succeeded}")
    print(f"Failed recoveries: {failed}")

    if total:
        print(f"Detection rate: {detected / total * 100:.2f}%")
        print(f"Auto-resolution rate: {succeeded / total * 100:.2f}%")

    if results["avg_resolution_seconds"] is not None:
        print(
            "Average resolution time: "
            f"{results['avg_resolution_seconds']:.2f} seconds"
        )

    print("==========================================")
