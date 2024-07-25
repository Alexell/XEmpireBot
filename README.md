# Bot for [Musk Empire](https://alexell.ru/cc/musk)

![img1](.github/images/demo.png)

> 🇷🇺 README на русском доступен [здесь](README-RU.md)

## Functionality
| Feature                           | Supported  |
|-----------------------------------|:----------:|
| Multithreading                    |     ✅     |
| Binding a proxy to a session      |     ✅     |
| Sleep before run each session     |     ✅     |
| Claim daily grant                 |     ✅     |
| Claim reward for friends          |     ✅     |
| Claim reward for completed quests |     ✅     |
| Claim offline bonus               |     ✅     |
| Automatic taps                    |     ✅     |
| PvP negotiations                  |     ✅     |
| Docker                            |     ✅     |

## [Options](https://github.com/Alexell/MuskEmpireBot/blob/main/.env-example)
| Option                  | Description                                                       |
|-------------------------|-------------------------------------------------------------------|
| **API_ID / API_HASH**   | Platform data for launching a Telegram session (default: Android) |
| **TAPS_ENABLED**        | Taps enabled (True / False)                                       |
| **TAPS_PER_SECOND**     | Random number of taps per second (e.g. [20,30], max. 30)          |
| **PVP_ENABLED**         | PvP negotiations enabled (True / False)                           |
| **PVP_LEAGUE**          | League in negotiations (e.g. bronze)                              |
| **PVP_STRATEGY**        | Strategy in negotiations (e.g. random)                            |
| **PVP_COUNT**           | Number of negotiations per cycle (e.g. 10)                        |
| **SLEEP_BETWEEN_START** | Sleep before start each session (e.g. [20, 360])                  |
| **ERRORS_BEFORE_STOP**  | The number of failed requests after which the bot will stop       |
| **USE_PROXY_FROM_FILE** | Whether to use proxy from the `proxies.txt` file (True / False)   |

You can obtain the **API_ID** and **API_HASH** after creating an application at [my.telegram.org/apps](https://my.telegram.org/apps)

**PvP negotiations** are disabled by default. Enable at your own risk. Upgrade your negotiation and ethics skills to win in case of a tie. The default strategy is randomly selected for each negotiation. If you wish, you can specify your own strategy, which will be used **in all** negotiations. Strategy names for the **PVP_STRATEGY** parameter: `aggressive`, `flexible`, `protective`. The **PVP_COUNT** parameter determines the number of negotiations the bot will conduct in one cycle (the bot performs all actions, then sleeps for an hour, which is the recurring cycle).

## Quick start
### Windows
1. Ensure you have **Python 3.10** or a newer version installed.
2. Use `INSTALL.bat` to install, then specify your API_ID and API_HASH in the .env file.
3. Use `START.bat` to launch the bot (or in the console: `python main.py`).

### Linux
1. Clone the repository: `git clone https://github.com/Alexell/MuskEmpireBot.git && cd MuskEmpireBot`
2. Run the installation: `chmod +x INSTALL.sh START.sh && ./INSTALL.sh`, then specify your API_ID and API_HASH in the .env file.
3. Use `./START.sh` to run the bot (or in the console: `python3 main.py`).

## Running in Docker
```
$ git clone https://github.com/Alexell/MuskEmpireBot.git
$ cd MuskEmpireBot
$ cp .env-example .env
$ nano .env # specify your API_ID and API_HASH, the rest can be left as default
```
### Docker Compose (recommended)
```
$ docker-compose run bot -a 1 # first run for authorization (override arguments)
$ docker-compose start # start in background mode (default arguments: -a 2)
```
### Docker
```
$ docker build -t muskempire_bot .
$ docker run --name MuskEmpireBot -v .:/app -it muskempire_bot -a 1 # first run for authorization
$ docker rm MuskEmpireBot # remove container to recreate with default arguments
$ docker run -d --restart unless-stopped --name MuskEmpireBot -v .:/app muskempire_bot # start in background mode (default arguments: -a 2)
```

## Manual installation
You can download [**Repository**](https://github.com/Alexell/MuskEmpireBot) by cloning it to your system and installing the necessary dependencies:
```
$ git clone https://github.com/Alexell/MuskEmpireBot.git
$ cd MuskEmpireBot

# Linux
$ python3 -m venv venv
$ source venv/bin/activate
$ pip3 install -r requirements.txt
$ cp .env-example .env
$ nano .env # specify your API_ID and API_HASH, the rest can be left as default
$ python3 main.py

# Windows (first, install Python 3.10 or a newer version)
> python -m venv venv
> venv\Scripts\activate
> pip install -r requirements.txt
> copy .env-example .env
> # specify your API_ID and API_HASH, the rest can be left as default
> python main.py
```

Also for quick launch you can use arguments:
```
$ python3 main.py --action (1/2)
# or
$ python3 main.py -a (1/2)

# 1 - Create session
# 2 - Run bot
```

## Running a bot in the background (Linux)
```
$ cd MuskEmpireBot

# with logging
$ setsid venv/bin/python3 main.py --action 2 >> app.log 2>&1 &

# without logging
$ setsid venv/bin/python3 main.py --action 2 > /dev/null 2>&1 &

# Now you can close the console, and the bot will continue its work.
```

### Find the bot process
```
$ ps aux | grep "python3 main.py" | grep -v grep
```