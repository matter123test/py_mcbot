## py_mcbot

This is a simple discord bot to control a minecraft server

![](icon.png "py_mcbot icon")

## Installation

If you don't have installed uv already
``pip install uv``

Clone the repo

``git clone https://github.com/matter123test/py_mcbot``

``cd py_mcbot``

``uv venv``

## Create a server

Note: *Supports fabric or papermc*

``uv run tools\configure_server.py``

After running this command it will create a folder `server`

Make sure to accept the Eula in `server/eula.txt`

## Configuration
Create a file named config.toml
```toml
[bot]
token = "" # discord bot token
guild = 123456 # discord server id
# discord users that are allowed to use admin commands
admins = [123456]

[server]
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