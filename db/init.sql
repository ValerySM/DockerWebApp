CREATE DATABASE IF NOT EXISTS app_db;
USE app_db;

CREATE TABLE IF NOT EXISTS counter (
    id INT PRIMARY KEY,
    value INT
);
INSERT INTO counter (id, value) VALUES (1, 0);

CREATE TABLE IF NOT EXISTS access_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp DATETIME,
    client_ip VARCHAR(255),
    internal_ip VARCHAR(255)
);
