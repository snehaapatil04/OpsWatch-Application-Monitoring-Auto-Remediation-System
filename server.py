
"""
OpsWatch API Server
--------------------
Connects the dashboard to MySQL and supports
controlled incident creation for failure testing.

Run: python server.py
"""

from flask import Flask, request, jsonify, send_from_directory
import mysql.connector

app = Flask(__name__, static_folder=".")

import os

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("root"),
    "database": os.getenv("DB_NAME", "opswatch")
}



def get_db():
    return mysql.connector.connect(**DB_CONFIG)


@app.route("/")
def dashboard():
    return send_from_directory(".", "dashboard.html")


@app.route("/api/incidents", methods=["GET"])
def list_incidents():
    db = get_db()
    cur = db.cursor(dictionary=True)

    try:
        cur.execute(
            "SELECT * FROM incidents ORDER BY created_at DESC LIMIT 50"
        )
        rows = cur.fetchall()

        for row in rows:
            row["created_at"] = str(row["created_at"])
            row["resolved_at"] = (
                str(row["resolved_at"]) if row["resolved_at"] else None
            )
            row["detected_at"] = (
                str(row["detected_at"]) if row["detected_at"] else None
            )
            row["attempted_at"] = (
                str(row["attempted_at"]) if row["attempted_at"] else None
            )

        return jsonify(rows)

    finally:
        cur.close()
        db.close()


@app.route("/api/incidents", methods=["POST"])
def create_incident():
    data = request.get_json(silent=True) or {}

    required = ["app_name", "severity", "cpu_percent", "disk_percent"]

    missing = [field for field in required if field not in data]

    if missing:
        return jsonify({"error": "Missing fields", "fields": missing}), 400

    if data["severity"] not in ("watch", "critical"):
        return jsonify({"error": "Invalid severity"}), 400

    try:
        cpu = int(data["cpu_percent"])
        disk = int(data["disk_percent"])

        if not (0 <= cpu <= 100 and 0 <= disk <= 100):
            return jsonify({"error": "CPU and disk must be between 0 and 100"}), 400

    except (TypeError, ValueError):
        return jsonify({"error": "CPU and disk must be numbers"}), 400

    simulate_failure = data.get("simulate_recovery_failure", False)

    if not isinstance(simulate_failure, bool):
        return jsonify({"error": "simulate_recovery_failure must be true or false"}), 400

    if simulate_failure and data["severity"] != "critical":
        return jsonify({
            "error": "Recovery failure simulation requires critical severity"
        }), 400

    db = get_db()
    cur = db.cursor()

    try:
        cur.execute(
            """
            INSERT INTO incidents
            (app_name, severity, cpu_percent, disk_percent,
             status, simulate_recovery_failure)
            VALUES (%s, %s, %s, %s, 'open', %s)
            """,
            (
                data["app_name"],
                data["severity"],
                cpu,
                disk,
                simulate_failure,
            ),
        )

        db.commit()
        new_id = cur.lastrowid

        return jsonify({"id": new_id, "message": "Incident created"}), 201

    finally:
        cur.close()
        db.close()


if __name__ == "__main__":
    app.run(debug=True, port=5000)
