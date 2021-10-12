import threading, logging, socket, json, time, requests, os, sys
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

load_dotenv()
messanger       = os.getenv('messanger')
slack_url       = os.getenv('slack_url')
bot_token       = os.getenv('bot_token')
bot_chatID      = os.getenv('bot_chatID')
port_range      = int(os.getenv('port_range'))
thread_limit    = int(os.getenv('thread_limit'))
socket_timeout  = float(os.getenv('socket_timeout'))

def MessageSend(server, port, allowed_ports):
    if f'{server}:{port}' not in allowed_ports:
        bot_message = f'Server: {server}\nPort: {port}\nStatus: OPEN'

        if messanger == 'telegram':
            send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
            response = requests.get(send_text)
        if messanger == 'slack':
            headers = {'Content-type': 'application/json'}
            response = requests.post(
                slack_url, json={'text': str(bot_message)},
                headers=headers
            )
    else:
        logging.info(f'{port} is allowed')

def portscan(port, server, allowed_ports):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(socket_timeout)
    try:
        con = s.connect((server, port))
        logging.warning(f'Port: {port} is open.')
        MessageSend(server, port, allowed_ports)
        con.close()
    except: 
        pass

def service(allowed_ports):
    f = open("server_list", "r")
    for server in f:
        logging.info(f'{datetime.now(timezone.utc)} ::: Scanning server: {server.strip()} :::')
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
        logging.info(f'{datetime.now(timezone.utc)} ::: Server scanned: {server.strip()} :::')

def allowed_list():
    allowed_ports = []
    f = open("allowed_ports", "r")
    for server in f:
        allowed_ports.append(server.strip())
    
    return tuple(allowed_ports)

allowed_ports = allowed_list()
service(allowed_ports)