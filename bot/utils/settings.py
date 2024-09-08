from pydantic_settings import BaseSettings, SettingsConfigDict

logo = """

██   ██     ███████ ███    ███ ██████  ██ ██████  ███████     ██████   ██████  ████████ 
 ██ ██      ██      ████  ████ ██   ██ ██ ██   ██ ██          ██   ██ ██    ██    ██    
  ███       █████   ██ ████ ██ ██████  ██ ██████  █████       ██████  ██    ██    ██    
 ██ ██      ██      ██  ██  ██ ██      ██ ██   ██ ██          ██   ██ ██    ██    ██    
██   ██     ███████ ██      ██ ██      ██ ██   ██ ███████     ██████   ██████     ██    

"""

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True)

    API_ID: int
    API_HASH: str

    BOT_TOKEN: str
    CHAT_ID: str
    USE_TG_BOT: bool
    TAPS_ENABLED: bool = True
    TAPS_PER_SECOND: list[int] = [20, 30]  # Tested with 4 fingers
    INVEST_ENABLED: bool = True
    PVP_ENABLED: bool = False
    PVP_LEAGUE: str = 'auto'
    PVP_UPGRADE_LEAGUE: bool = False
    PVP_STRATEGY: str = 'random'
    PVP_COUNT: int = 10
    SKILLS_COUNT: int = 10
    SKILLS_MODE: str = 'profitness'
    IGNORED_SKILLS: list[str] = []
    MINING_SKILLS_LEVEL: int = 10
    PROTECTED_BALANCE: int = 0
    DAY_MAIN_DELAY: int = 3600
    NIGHT_MAIN_DELAY: int = 10800
    REF_CODE: str = 'hero5726822287'

    SLEEP_BETWEEN_START: list[int] = [20, 360]
    ERRORS_BEFORE_STOP: int = 3
    USE_PROXY_FROM_FILE: bool = False
    DEBUG_MODE: bool = False

try:
    config = Settings()
except Exception as error:
    # Import the logger here to avoid circular import
    from bot.utils.logger import log
    log.error(error)
    config = False
