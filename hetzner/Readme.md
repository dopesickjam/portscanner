# simple port scanner
the application is prepared to use the hetzner cloud,
since vps is an external service and will not be on a trusted network.

sends a message to telegram or slack

## Pre-requisites
* python >= 3.6.0

1. .env.example for main app.py
```
hetzner_token = '${hetzner_token}' # token which create for project in hetzner cloud
hetzner_url = 'https://api.hetzner.cloud/v1'
ssh_key = 'name of ssh key' #ssh key, which add to project in hetzner cloud, for remotely access when vps is growed up 
```
2. .env.example for app/portscanner.py
```
bot_token       = 'telegram bot token'
bot_chatID      = 'telegram chat id'
port_range      = 20000 #port scan range, max is 65535
thread_limit    = 400 #number of parallel streams, 400-500 recommend for cx11
socket_timeout  = 0.5 #time to wait for a port response
slack_url       = 'webhook_slack'
messanger       = 'telegram' or 'slack'
```
2. app/server_list - list of the server whose need check
3. app/allowed_ports - list of the server and port whose allowed to be opened, separeted by two dots
4. for start:
```
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
python app.py
```