# OpsWatch — Application Monitoring & Auto-Remediation

A small end-to-end project simulating what an Application Maintenance
automation pipeline does: **monitor → detect → log to a database →
automatically remediate**.

## How it works

```
dashboard.html  --(writes new incidents)-->  server.py (Flask API)  -->  MySQL
                <--(reads current state)--/
bot.py  --(polls MySQL every 5s, resolves critical incidents)-->  MySQL
```

- **dashboard.html** — simulates live app metrics in the browser, and posts
  an incident to the API whenever an app goes into "watch" or "critical" state.
- **server.py** — a small Flask API that lets the browser read/write to MySQL
  (browsers can't talk to MySQL directly).
- **bot.py** — runs independently, like a scheduled RPA bot. It polls MySQL
  for open incidents and auto-resolves the critical ones, writing back what
  action it took. This is the actual "automation" piece.

## Setup (one-time)

1. **Install MySQL** if you don't have it already (mysql.com, or via your
   package manager).

2. **Create the database and table:**
   ```
   mysql -u root -p < schema.sql
   ```

3. **Install Python dependencies:**
   ```
   pip install -r requirements.txt
   ```

4. **Set your MySQL password** in both `server.py` and `bot.py`
   (look for `"password": ""` near the top of each file).

## Running it

Open **three terminals**:

**Terminal 1 — start the API/dashboard server:**
```
python server.py
```
Then open http://localhost:5000 in your browser.

**Terminal 2 — start the automation bot:**
```
python bot.py
```
Leave this running. Watch its terminal output — you'll see it print each
incident it resolves in real time.

**Terminal 3 (optional) — inspect the database directly:**
```
mysql -u root -p opswatch
SELECT * FROM incidents ORDER BY created_at DESC;
```

## What to watch for

1. Leave the dashboard open for a minute or two. Some apps will drift into
   "Watch" or "Critical".
2. Check bot.py's terminal — within 5 seconds it will pick up any critical
   incident and resolve it.
3. Refresh the dashboard's incident log — you'll see the entry change from
   "ALERT" to "AUTO-RESOLVED" with the action the bot took, all pulled live
   from MySQL.

## Ideas to extend this further

- Add a `resolve_seconds` calculation and show average resolution time on
  the dashboard (a real "ticket analytics" metric).
- Have bot.py send an actual email (via `smtplib`) instead of just printing,
  for critical incidents it *can't* auto-resolve.
- Replace bot.py's logic with an actual Automation Anywhere bot that polls
  the same MySQL table — same architecture, just swapping the automation
  engine.
