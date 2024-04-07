import os
import json
from datetime import datetime
from flask import Flask, request, render_template, redirect, url_for
import socket
import threading

app = Flask(__name__)

@app.route('/')
def index():
    return redirect(url_for('static', filename='index.html'))

@app.route('/imessage.html')
def imessage():
    return redirect(url_for('static', filename='imessage.html'))

@app.route('/submit_message', methods=['POST'])
def submit_message():
    if request.method == 'POST':
        username = request.form['username']
        message = request.form['message']
        timestamp = datetime.now().isoformat()

        send_to_socket(username, message, timestamp)
        
        return redirect(url_for('imessage'))

@app.errorhandler(404)
def page_not_found(error):
    return redirect(url_for('static', filename='error.html')), 404

def send_to_socket(username, message, timestamp):
    data_dict = {
        timestamp: {
            "username": username,
            "message": message
        }
    }
    data_json = json.dumps(data_dict)
    
    UDP_IP = "127.0.0.1"
    UDP_PORT = 5000

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.sendto(data_json.encode(), (UDP_IP, UDP_PORT))

def socket_server_thread():
    UDP_IP = "127.0.0.1"
    UDP_PORT = 5000
    
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind((UDP_IP, UDP_PORT))
        
        while True:
            data, addr = sock.recvfrom(1024)
            data_dict = json.loads(data.decode())
            
            save_to_json(data_dict)

def save_to_json(data_dict):
    filename = 'storage/data.json'
    
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            existing_data = json.load(file)
    else:
        existing_data = {}
    
    existing_data.update(data_dict)
    
    with open(filename, 'w') as file:
        json.dump(existing_data, file, indent=4)

if __name__ == '__main__':
    http_thread = threading.Thread(target=app.run, kwargs={'port': 3000})
    http_thread.start()
    
    
    socket_thread = threading.Thread(target=socket_server_thread)
    socket_thread.start()
