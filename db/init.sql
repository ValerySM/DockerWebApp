CREATE DATABASE IF NOT EXISTS Valery_DB;
USE Valery_DB;

CREATE TABLE IF NOT EXISTS access_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    access_time DATETIME,
    client_ip VARCHAR(50),
    server_ip VARCHAR(50),
    INDEX idx_access_time (access_time),
    INDEX idx_client_ip (client_ip)
);