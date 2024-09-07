# Bot for [X Empire](https://alexell.pro/cc/xempire) (Musk Empire)

![img1](.github/images/demo.png)

> 🇷🇺 README на русском доступен [здесь](README-RU.md)

## Functionality
| Feature                               | Supported  |
|---------------------------------------|:----------:|
| Multithreading                        |     ✅     |
| Binding a proxy to a session          |     ✅     |
| Sleep before run each session         |     ✅     |
| Claim daily grant                     |     ✅     |
| Claim reward for friends              |     ✅     |
| Claim reward for quests               |     ✅     |
| Claim offline bonus                   |     ✅     |
| Automatic taps                        |     ✅     |
| PvP negotiations                      |     ✅     |
| Daily quiz and rebus solution         |     ✅     |
| Investing in funds (combo for profit) |     ✅     |
| Automatic skill improvement           |     ✅     |
| Docker                                |     ✅     |

## [Options](https://github.com/Alexell/XEmpireBot/blob/main/.env-example)
| Option                  | Description                                                                                |
|-------------------------|--------------------------------------------------------------------------------------------|
| **API_ID / API_HASH**   | Platform data for launching a Telegram session                                             |
| **TAPS_ENABLED**        | Taps enabled (True / False)                                                                |
| **TAPS_PER_SECOND**     | Random number of taps per second (e.g. [20,30], max. 30)                                   |
| **INVEST_ENABLED**      | Investments enabled (True / False)                                                         |
| **PVP_ENABLED**         | PvP negotiations enabled (True / False)                                                    |
| **PVP_LEAGUE**          | League in negotiations (e.g. bronze or auto for automatic selection)                       |
| **PVP_UPGRADE_LEAGUE**  | Upgrade league if league specified in PVP_LEAGUE is unavailable (True / False)             |
| **PVP_STRATEGY**        | Strategy in negotiations (e.g. random)                                                     |
| **PVP_COUNT**           | Number of negotiations per cycle (e.g. 10)                                                 |
| **SKILLS_COUNT**        | Number of profit skills improved per cycle (e.g. 10)                                       |
| **SKILLS_MODE**         | Profit skill selection mode for improvement (e.g. profitness)                              |
| **IGNORED_SKILLS**      | Skills that the bot will not improve (e.g. ["agi", "voice_assistant", "translators"])      |
| **MINING_SKILLS_LEVEL** | Max level of mining skill improve (e.g. 10)                                                |
| **PROTECTED_BALANCE**   | Balance protected from spending on PvP, investments and skills (e.g. 100000000)            |
| **REF_CODE**            | Your code from the invite link (e.g., hero123456) *if not provided, mine will be used*     |
| **SLEEP_BETWEEN_START** | Sleep before start each session (e.g. [20, 360])                                           |
| **ERRORS_BEFORE_STOP**  | The number of failed requests after which the bot will stop                                |
| **USE_PROXY_FROM_FILE** | Whether to use proxy from the `proxies.txt` file (True / False)                            |

You can obtain the **API_ID** and **API_HASH** after creating an application at [my.telegram.org/apps](https://my.telegram.org/apps)

**PvP negotiations** are disabled by default. Enable at your own risk. Upgrade your negotiation and ethics skills to win in case of a tie. League names for the **PVP_LEAGUE** parameter: `bronze`, `silver`, `gold`, `platina`, `diamond`. You can also specify `auto` in the **PVP_LEAGUE** parameter, and the bot will automatically select the lowest available league for you. The default strategy is randomly selected for each negotiation. If you wish, you can specify your own strategy, which will be used **in all** negotiations. Strategy names for the **PVP_STRATEGY** parameter: `aggressive`, `flexible`, `protective`. The **PVP_COUNT** parameter determines the number of negotiations the bot will conduct in one cycle.

The answer to the **daily quiz** and the list of funds with guaranteed profits for **investing** are loaded from a [json file](https://alexell.pro/crypto/x-empire/data.json) on my website. I will try to update the data daily so that all your deployed bots can perform these actions and earn additional profit. When investing, the bet amount will always be the maximum, as the profit is guaranteed. If there is not enough money for the maximum bet, the bet amount will be reduced.

Each cycle, the bot will upgrade as many profit skills as specified in the **SKILLS_COUNT** parameter. The default is 10. You can specify the skill selection mode in the **SKILLS_MODE** parameter. There are 3 modes: `profitness` (the most profitable skills based on the profit/price ratio), `profit` (skills with the highest profit, regardless of price), and `price` (the cheapest skills, regardless of profit). The default mode is `profitness`. If possible, the bot will improve mining skills by 1 level each cycle until the level reaches the value specified in **MINING_SKILLS_LEVEL** parameter. Set it to 0 if you do not need to improve mining skills.

If you want to protect a certain amount of money in the balance, set the desired amount in the **PROTECTED_BALANCE** parameter. The bot will not allow the balance to fall below this amount.

**Intervals.** During the day, if `TAPS_ENABLED=True`, the bot performs taps continuously, with delays only for energy recovery. Other actions are performed approximately every hour. At night, taps and other actions are performed approximately every 3 hours.

## Quick start
### Windows
1. Ensure you have **Python 3.10** or a later version installed.

**Attention:** If you are using **Python 3.12**, before proceeding to the next step, you need to either remove the `TgCrypto` line from `requirements.txt` (TgCrypto is not critical) or install the [required software](https://visualstudio.microsoft.com/visual-cpp-build-tools/) for automatic compilation of this package during installation.

2. Use `INSTALL.bat` to install, then specify your API_ID and API_HASH in the .env file.
3. Use `START.bat` to launch the bot (or in the console: `python main.py`).

### Linux
1. Clone the repository: `git clone https://github.com/Alexell/XEmpireBot.git && cd XEmpireBot`

**Attention:** If you are using **Python 3.12**, before proceeding to the next step, you need to either remove the `TgCrypto` line from `requirements.txt` (TgCrypto is not critical) or install the required software for automatic compilation of this package during installation:
```shell
apt install build-essential python3-dev
```
2. Run the installation: `chmod +x INSTALL.sh START.sh && ./INSTALL.sh`, then specify your API_ID and API_HASH in the .env file.
3. Use `./START.sh` to run the bot (or in the console: `python3 main.py`).

## Running in Docker
```
$ git clone https://github.com/Alexell/XEmpireBot.git
$ cd XEmpireBot
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
$ docker build -t xempire_bot .
$ docker run --name XEmpireBot -v .:/app -it xempire_bot -a 1 # first run for authorization
$ docker rm XEmpireBot # remove container to recreate with default arguments
$ docker run -d --restart unless-stopped --name XEmpireBot -v .:/app xempire_bot # start in background mode (default arguments: -a 2)
```

## Manual installation
You can download [**Repository**](https://github.com/Alexell/XEmpireBot) by cloning it to your system and installing the necessary dependencies:
```
$ git clone https://github.com/Alexell/XEmpireBot.git
$ cd XEmpireBot

# Linux
# ATTENTION: If you have installed Python 3.12, before proceeding to the next step, you need to:
#    either remove the TgCrypto line from requirements.txt (TgCrypto is not critical)
#    or install the necessary software for automatic compilation of this package during installation with the command: apt install build-essential python3-dev
$ python3 -m venv venv
$ source venv/bin/activate
$ pip3 install -r requirements.txt
$ cp .env-example .env
$ nano .env # specify your API_ID and API_HASH, the rest can be left as default
$ python3 main.py

# Windows (first, install Python 3.10 or a later version)
# ATTENTION: If you have installed Python 3.12, before proceeding to the next step, you need to:
#    either remove the TgCrypto line from requirements.txt (TgCrypto is not critical)
#    or install the necessary software for automatic compilation of this package during installation, link: https://visualstudio.microsoft.com/visual-cpp-build-tools/
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

**## Running a bot in the background (Linux)**
```
$ cd XEmpireBot

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

## **Running the bot in Koyeb (Free)
<div class="markdown prose w-full break-words dark:prose-invert light"><h3>Steps to Deploy with Koyeb:</h3><ol><li><p><strong>Fork the Repo</strong></p><ul><li>Go to the repository you want to fork on GitHub.</li><li>Click on the "Fork" button in the top right corner to create a copy of the repository in your GitHub account.</li></ul></li><li><p><strong>Generate a <code>*.SESSION</code> File Locally</strong></p><ul><li>This step likely refers to generating a session file for an application. Follow the application's documentation to generate the session file locally. For instance, it could be done by running a script or command, depending on the specific setup.</li></ul></li><li><p><strong>Upload the <code>*.SESSION</code> File to <code>/sessions/yourname.SESSION</code></strong></p><ul><li>Upload the <code>.SESSION</code> file into the <code>sessions</code> folder of your repository.</li><li>Make sure the directory structure is correct, and replace <code>yourname</code> with your specific identifier or username.</li></ul></li><li><p><strong>Connect Your GitHub Account to Koyeb</strong></p><ul><li>Sign in or create an account on Koyeb (<a rel="noopener" target="_new" href="https://www.koyeb.com/">https://www.koyeb.com/</a>).</li><li>Go to the Koyeb dashboard and connect your GitHub account by selecting the "GitHub" option in the integration section.</li></ul></li><li><p><strong>Create a Web Service Using GitHub</strong></p><ul><li>In the Koyeb dashboard, go to the "Services" section and create a new service.</li><li>Select "GitHub" as the source for your service.</li></ul></li><li><p><strong>Select the Forked Repo</strong></p><ul><li>From the repository list, choose the repo you forked earlier to deploy.</li></ul></li><li><p><strong>Switch to the <code>Koyeb-Deployment</code> Branch</strong></p><ul><li>During the setup process, make sure to select the <code>Koyeb-Deployment</code> branch from the list of available branches.</li></ul></li><li><p><strong>Configure the <code>.env</code> or Environment Variables</strong></p><ul><li>If your application requires certain environment variables (like API keys or config settings), you can add them by:<ul><li>Uploading or editing the <code>.env</code> file directly in the forked repo.</li><li>Alternatively, in the Koyeb service dashboard, you can define the environment variables directly in the interface under the "Environment" section.</li></ul></li></ul></li><li><p><strong>Set Buildpack Run Command Override</strong></p><ul><li>Under the Buildpack section, you should override the default run command.</li><li>Enter the following command to start your Python application:<pre class="!overflow-visible"><div class="dark bg-gray-950 contain-inline-size rounded-md border-[0.5px] border-token-border-medium relative"><div class="flex items-center text-token-text-secondary bg-token-main-surface-secondary px-4 py-2 text-xs font-sans justify-between rounded-t-md h-9"></div><div class="sticky top-9 md:top-[5.75rem]"><div class="absolute bottom-0 right-2 flex h-9 items-center"><div class="flex items-center rounded bg-token-main-surface-secondary px-2 font-sans text-xs text-token-text-secondary"><span class="" data-state="closed"><button class="flex gap-1 items-center py-1"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" class="icon-sm"><path fill-rule="evenodd" clip-rule="evenodd" d="M7 5C7 3.34315 8.34315 2 10 2H19C20.6569 2 22 3.34315 22 5V14C22 15.6569 20.6569 17 19 17H17V19C17 20.6569 15.6569 22 14 22H5C3.34315 22 2 20.6569 2 19V10C2 8.34315 3.34315 7 5 7H7V5ZM9 7H14C15.6569 7 17 8.34315 17 10V15H19C19.5523 15 20 14.5523 20 14V5C20 4.44772 19.5523 4 19 4H10C9.44772 4 9 4.44772 9 5V7ZM5 9C4.44772 9 4 9.44772 4 10V19C4 19.5523 4.44772 20 5 20H14C14.5523 20 15 19.5523 15 19V10C15 9.44772 14.5523 9 14 9H5Z" fill="currentColor"></path><code>python3 main.py -a 2
</code></div></div></pre></li></ul></li></ol><p>These steps should help you deploy the application successfully with Koyeb and GitHub. Let me know if you'd like further assistance with any specific step!</p></div>
