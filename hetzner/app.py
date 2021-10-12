from dotenv import load_dotenv
from fabric import Connection
from datetime import datetime, timezone, timedelta
import os, sys, logging, requests, json, paramiko
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

load_dotenv()
hetzner_token = os.getenv('hetzner_token')
hetzner_url = os.getenv('hetzner_url')
ssh_key = os.getenv('ssh_key')

def serverCreate():
    logging.info('Starting proccess for creating server in hetzner cloud')
    headers = {
        'Authorization': f'Bearer {hetzner_token}',
        'Content-Type': 'application/json'
    }
    data = {
        'automount': 'false',
        'firewalls': [],
        'image': 'ubuntu-20.04',
        'labels': {},
        'location': 'nbg1',
        'name': 'secure',
        'networks': [],
        'server_type': 'cx11',
        'ssh_keys': [f'{ssh_key}'],
        'start_after_create': 'true',
        'user_data': '',
        'volumes': []
    }
    response = requests.post(
        f'{hetzner_url}/servers',
        headers=headers,
        json=data
    )

    response = response.json()

    server_id = response['server']['id']
    server_ip = response['server']['public_net']['ipv4']['ip']

    logging.info(f'Server was created with IP: {server_ip} and ID: {server_id}')
    return server_id, server_ip

def serverWaiting(server_ip):
    while True:
        try:
            logging.info(f'Waiting when server {server_ip} arise')
            c = Connection(host=server_ip, user='root', port=22)
            c.run('uname -a')
            return c
        except OSError:
            pass
    logging.info(f'Server {server_ip} is UP')

def serverPrepare(c, server_ip):
    logging.info('installing dependencies system packages')
    c.run('apt update')
    c.run('apt install -y python3 python3-pip')
    c.run('mkdir -p /app')

    logging.info('installing dependencies portscanner')

    p = paramiko.SSHClient()
    p.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    p.connect( hostname = server_ip, port = 22, username = 'root' )

    ftp_client = p.open_sftp()
    for f in os.listdir('app/'):
        ftp_client.put(f'./app/{f}',f'/app/{f}')
    ftp_client.close()
    c.run('pip3 install -r /app/requirements.txt')

    logging.info(f'{server_ip} was prepared')

def runPortscanner(c, server_ip):
    logging.info(f'{datetime.now(timezone.utc)} ::: Run portscanner :::')

    c.run('cd /app && python3 portscanner.py')
    logging.info(f'{datetime.now(timezone.utc)} ::: Scanning was done :::')

def serverDelete(server_id):
    logging.info('Deleting server')
    headers = {
        'Authorization': f'Bearer {hetzner_token}'
    }
    response = requests.delete(
        f'{hetzner_url}/servers/{server_id}',
        headers = headers
    )
    logging.info('Server was deleted')

server_id, server_ip = serverCreate()
c = serverWaiting(server_ip)
serverPrepare(c, server_ip)
runPortscanner(c, server_ip)
serverDelete(server_id)