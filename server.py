"""
OpsWatch API server
--------------------
Connects the browser dashboard to MySQL.
Run with:  python server.py
Then open: http://localhost:5000
"""

from flask import Flask, request, jsonify, send_from_directory
import mysql.connector
import os

app = Flask(__name__, static_folder=".")

DB_CONFIG = {
    "host": "localhost",
    "user": "root",          # change to your MySQL username
    "password": "root",          # <-- put your MySQL password here
    "database": "opswatch",
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
    cur.execute("SELECT * FROM incidents ORDER BY created_at DESC LIMIT 50")
    rows = cur.fetchall()
    cur.close()
    db.close()
    # datetime objects aren't JSON serializable by default -> convert to string
    for r in rows:
        r["created_at"] = str(r["created_at"])
        r["resolved_at"] = str(r["resolved_at"]) if r["resolved_at"] else None
    return jsonify(rows)


@app.route("/api/incidents", methods=["POST"])
def create_incident():
    data = request.json
    db = get_db()
    cur = db.cursor()
    cur.execute(
        """INSERT INTO incidents (app_name, severity, cpu_percent, disk_percent, status)
           VALUES (%s, %s, %s, %s, 'open')""",
        (data["app_name"], data["severity"], data["cpu_percent"], data["disk_percent"]),
    )
    db.commit()
    new_id = cur.lastrowid
    cur.close()
    db.close()
    return jsonify({"id": new_id}), 201


if __name__ == "__main__":
    app.run(debug=True, port=5000)
