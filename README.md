# OpsWatch – Application Monitoring & Auto-Remediation System

OpsWatch is a Python-based application monitoring project that tracks application health, records incidents in MySQL, and demonstrates automated remediation through predefined simulated recovery actions.

## Features

- Monitors the displayed health status of 6 sample applications.
- Flask REST APIs for creating and retrieving incidents.
- MySQL database for incident history and remediation results.
- JavaScript dashboard with automatic refresh.
- Python automation bot that polls for new incidents every 5 seconds.
- Severity-based incident handling for Watch and Critical incidents.
- Simulated successful and failed recovery scenarios.
- Records incident detection, remediation attempts, and outcomes.

## Tech Stack

- Python
- Flask
- MySQL
- JavaScript
- HTML and CSS
- REST APIs

## Testing Results

Tested the incident detection and simulated remediation workflow using 20 generated critical incidents.

| Metric | Result |
|---|---:|
| Total test incidents | 20 |
| Incidents detected | 20 |
| Successful simulated recoveries | 15 |
| Failed simulated recoveries | 5 |
| Detection rate | 100% |
| Simulated recovery success rate | 75% |
| Average resolution time | 2.8 seconds |

These results are from a local simulation, not production monitoring.

## Project Structure

- `server.py` – Flask application and REST API endpoints
- `bot.py` – Incident detection and simulated remediation bot
- `dashboard.html` – Monitoring dashboard
- `schema.sql` – MySQL database schema
- `test_opswatch.py` – Automated incident testing script
- `requirements.txt` – Python dependencies

## Running the Project

1. Install dependencies:

   `pip install -r requirements.txt`

2. Configure the MySQL database and environment variables.

3. Run the Flask server:

   `python server.py`

4. In another terminal, run the automation bot:

   `python bot.py`

5. Open `http://127.0.0.1:5000` in your browser.

6. Run the test script when the server and bot are running:

   `python test_opswatch.py`

## Note

Recovery actions are simulated for demonstration and testing purposes. The project does not restart real services or perform actual infrastructure remediation.