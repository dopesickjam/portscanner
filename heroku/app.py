from flask import Flask, flash, redirect, render_template, request, session, abort, send_from_directory
import threading
import socket
import json
import time
import requests
from dotenv import load_dotenv
import os

load_dotenv()
bot_token       = os.getenv('bot_token')
bot_chatID      = os.getenv('bot_chatID')
start_route     = os.getenv('start_route')
port_range      = int(os.getenv('port_range'))
thread_limit    = int(os.getenv('thread_limit'))
socket_timeout  = float(os.getenv('socket_timeout'))

app = Flask(__name__,
    static_url_path='',
    template_folder='templates')

def TelegramSend(server, port, allowed_ports):
    if f'{server}:{port}' not in allowed_ports:
        bot_message = f'Server: {server}\nPort: {port}\nStatus: OPEN'
        send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
        response = requests.get(send_text)
    else:
        print(f'{port} is allowed')

def portscan(port, server, allowed_ports):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(socket_timeout)
    try:
        con = s.connect((server, port))
        print('Port:',port,"is open.")
        TelegramSend(server, port, allowed_ports)
        con.close()
    except: 
        pass

def service(allowed_ports):
    f = open("server_list", "r")
    for server in f:
        print ("Scanning server: "+server)
        current_port = 1 
        first_port = 1
        last_port = thread_limit
        while last_port <= port_range:
            for x in range(first_port,last_port):
                t = threading.Thread(target=portscan,kwargs={'port':current_port, 'server': server.strip(), 'allowed_ports': allowed_ports})
                current_port += 1     
                t.start() 
            #thread limit
            first_port = last_port
            last_port = last_port+thread_limit
            time.sleep(1)
        print ("Server scanned: "+server)

def allowed_list():
    allowed_ports = []
    f = open("allowed_ports", "r")
    for server in f:
        allowed_ports.append(server.strip())
    
    return tuple(allowed_ports)

@app.route('/')
def index():
    return render_template('index.html')

@app.route(f'/{start_route}')
def service_query():
    if request.args.get('service') == 'run':
        allowed_ports = allowed_list()
        service(allowed_ports)
        return 'you god damn right'
    else:
        return 'you can run but you cannot hide'

if __name__ == "__main__":
    app.run(debug=True,host='127.0.0.1', port=5000)