from flask import Flask, request, make_response, jsonify
import mysql.connector
from datetime import datetime, timedelta
import os
import socket
import time
import logging

time.sleep(5)  # Delay for 5 seconds

app = Flask(__name__)
logging.basicConfig(filename='/app/logs/app.log', level=logging.INFO)

def get_db_connection():
    try:
        return mysql.connector.connect(
            host="db",
            user="root",
            password="your_password",
            database="your_database"
        )
    except mysql.connector.Error as err:
        logging.error("Database connection failed: {}".format(err))
        return None

@app.before_first_request
def init_db():
    with get_db_connection() as db:
        if db is None:
            return
        cursor = db.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS access_log (
            id INT AUTO_INCREMENT PRIMARY KEY,
            access_time DATETIME,
            client_ip VARCHAR(50),
            server_ip VARCHAR(50),
            INDEX idx_access_time (access_time),
            INDEX idx_client_ip (client_ip)
        )
        """)
        db.commit()

@app.route('/')
def index():
    db = get_db_connection()
    if db is None:
        return "Database connection failed", 500
    
    with db:
        cursor = db.cursor()
        cursor.execute("INSERT INTO access_log (access_time, client_ip, server_ip) VALUES (%s, %s, %s)",
                       (datetime.now(), request.remote_addr, socket.gethostbyname(socket.gethostname()),))
        db.commit()

    response = make_response("Server IP: {}".format(socket.gethostbyname(socket.gethostname())))
    response.set_cookie('server_ip', socket.gethostbyname(socket.gethostname()), max_age=300)
    return response

@app.route('/showcount')
def show_count():
    db = get_db_connection()
    if db is None:
        return "Database connection failed", 500

    with db:
        cursor = db.cursor()
        cursor.execute("SELECT COUNT(*) FROM access_log")
        result = cursor.fetchone()
        global_counter = result[0]

    logging.info("Enter function showcount. Row count: {}".format(global_counter))

    return str(global_counter)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)