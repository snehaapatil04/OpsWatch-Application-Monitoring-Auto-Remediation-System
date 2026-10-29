-- OpsWatch database schema
-- Run this once after creating the database:
--   mysql -u root -p opswatch < schema.sql

CREATE DATABASE IF NOT EXISTS opswatch;
USE opswatch;

CREATE TABLE IF NOT EXISTS incidents (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    app_name      VARCHAR(100)  NOT NULL,
    severity      ENUM('watch', 'critical') NOT NULL,
    cpu_percent   INT           NOT NULL,
    disk_percent  INT           NOT NULL,
    status        ENUM('open', 'resolved') NOT NULL DEFAULT 'open',
    action_taken  VARCHAR(255)  DEFAULT NULL,
    created_at    DATETIME      DEFAULT CURRENT_TIMESTAMP,
    resolved_at   DATETIME      DEFAULT NULL
);

-- Handy queries you'll want later:
-- All open incidents:      SELECT * FROM incidents WHERE status = 'open';
-- Resolution time report:  SELECT app_name, TIMESTAMPDIFF(SECOND, created_at, resolved_at) AS resolve_seconds FROM incidents WHERE status = 'resolved';
