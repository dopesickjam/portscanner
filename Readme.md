# simple port scanner
the application is prepared to use the heroku service,
since heroku is an external service and will not be on a trusted network.

sends a message to telegram

1. env.example
```
bot_token       = 'telegram bot token'
bot_chatID      = 'telegram chat id'
start_route     = 'test' #route for remote run
port_range      = 20000 #port scan range
thread_limit    = 100 #number of parallel streams
socket_timeout  = 0.5 #time to wait for a port response
```
2. server_list - list of the server whose need check
3. allowed_ports - list of the server and port whose allowed to be opened, separeted by two dots

##
example for trigger:
curl https://name-app.herokuapp.com/test?service=run