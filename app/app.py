from flask import Flask, request, make_response, jsonify
import mysql.connector
from datetime import datetime, timedelta
import os
import socket
import time
time.sleep(5)  # Delay for 5 seconds

app = Flask(__name__)

# Database connection
def get_db_connection():
    return mysql.connector.connect(
        host="db",
        user="Valery",
        password="P@ssw0rd",
        database="Valery_DB"
    )

# Create the access_log table if it doesn't exist
with get_db_connection() as db:
    cursor = db.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS access_log (
        id INT AUTO_INCREMENT PRIMARY KEY,
        access_time DATETIME,
        client_ip VARCHAR(50),
        server_ip VARCHAR(50)
    )
    """)
    db.commit()

@app.route('/')
def index():
    with get_db_connection() as db:
        cursor = db.cursor()
        cursor.execute("INSERT INTO access_log (access_time, client_ip, server_ip) VALUES (%s, %s, %s)",
                       (datetime.now(), request.remote_addr, socket.gethostbyname(socket.gethostname()),))
        db.commit()

    # Create a cookie
    response = make_response(f"Server IP: {socket.gethostbyname(socket.gethostname())}")
    response.set_cookie('server_ip', socket.gethostbyname(socket.gethostname()), max_age=300)
    return response

@app.route('/showcount')
def show_count():
    with get_db_connection() as db:
        cursor = db.cursor()
        cursor.execute("SELECT COUNT(*) FROM access_log")
        result = cursor.fetchone()
        global_counter = result[0]

    with open("/app/logs/log.log", "a") as f:
        f.write(f"Enter function showcount. Row count: {global_counter}\n")

    return str(global_counter)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
