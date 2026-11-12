
-- OpsWatch database schema
-- Run this to create the database and incidents table.

CREATE DATABASE IF NOT EXISTS opswatch;
USE opswatch;

CREATE TABLE IF NOT EXISTS incidents (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    app_name VARCHAR(100) NOT NULL,
    severity ENUM('watch', 'critical') NOT NULL,
    cpu_percent INT NOT NULL,
    disk_percent INT NOT NULL,
    status ENUM('open', 'resolved', 'failed') NOT NULL DEFAULT 'open',
    action_taken VARCHAR(255) DEFAULT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    resolved_at DATETIME DEFAULT NULL,
    detected_at DATETIME DEFAULT NULL,
    attempted_at DATETIME DEFAULT NULL,
    remediation_status ENUM(
        'not_attempted',
        'succeeded',
        'failed',
        'not_required'
    ) DEFAULT 'not_attempted',
    simulate_recovery_failure TINYINT(1) DEFAULT '0'
);

-- Handy queries

-- All open incidents
-- SELECT * FROM incidents WHERE status = 'open';

-- Count incidents by status
-- SELECT status, COUNT(*) FROM incidents GROUP BY status;

-- Resolution time report
-- SELECT app_name,
--        TIMESTAMPDIFF(SECOND, created_at, resolved_at) AS resolve_seconds
-- FROM incidents
-- WHERE status = 'resolved' AND resolved_at IS NOT NULL;
