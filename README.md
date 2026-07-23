## py_mcbot

This is a discord bot to control a minecraft server

![](icon.png "py_mcbot icon")

## Installation

If you don't have installed uv already
``pip install uv``

Clone the repo

``git clone https://github.com/matter123test/py_mcbot``

``cd py_mcbot``

## Create a server

Note: *Supports fabric or papermc*

``uv run tools\configure_server.py``

After running this command it will create a folder `server`

Make sure to accept the Eula in `server/eula.txt`

## Configuration
Create a file named config.toml
```toml
[bot]
# discord bot token
token = "" 
# discord server id
# this is required to synchronize slash commands faster
guild = 123456 
# discord users that are allowed to use admin commands such as /exec
admins = [123456]

[server]
# example: "C:/Users/user/Desktop/server"
folder = "path to server folder" 
log = "path to latest.log file"
# minimal server run command args
run = ["java", "-Xmx3G", "-jar", "server.jar", "nogui"] 

# mcrcon is required to comunicate with the server
[server.mcrcon]
host = "localhost"
password = "1234"
port = 25575
delay_seconds = 1
```

Inside the server folder modify the `server.properties`
and set the values:

Note: these values must match with the config.toml's mcrcon configuration

```properties
enable-rcon=true
rcon.password=1234
rcon.port=25575
```

For cracked player support set online mode to false

```properties
online-mode=false
```

## Run

Run the bot:

``uv run run.py``

## Backups

Backups by default will be created at `backups`

To create a backup:

``uv run tools\backup.py``


## Commands
User commands:

Name          | Description   | Args
------------- | ------------- | -------------
/start  | Start the minecraft server
/stop  | Stop the minecraft server
/status | Get the minecraft server status
/players | Get the online players in the minecraft server
/tps | Get the current ticks per second in the minecraft server
/say | Sends a message to the minecraft server chat | message
/logs | Get the last 10 lines of the minecraft server logs file
/chat | Get the last 10 lines of player messages in the minecraft server chat

Admin commands:

Name          | Description   | Args
------------- | ------------- | -------------
/exec | Execute a command on the minecraft server | command
/forcestop | Stop the minecraft server even if there are players

