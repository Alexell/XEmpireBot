from pydantic_settings import BaseSettings, SettingsConfigDict

logo = """

███    ███ ██    ██ ███████ ██   ██     ███████ ███    ███ ██████  ██ ██████  ███████ 
████  ████ ██    ██ ██      ██  ██      ██      ████  ████ ██   ██ ██ ██   ██ ██      
██ ████ ██ ██    ██ ███████ █████       █████   ██ ████ ██ ██████  ██ ██████  █████   
██  ██  ██ ██    ██      ██ ██  ██      ██      ██  ██  ██ ██      ██ ██   ██ ██      
██      ██  ██████  ███████ ██   ██     ███████ ██      ██ ██      ██ ██   ██ ███████ 
                                                                                      
"""

class Settings(BaseSettings):
	model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True)

	API_ID: int
	API_HASH: str
	
	TAPS_PER_SECOND: list[int] = [20, 30] # tested with 4 fingers
	ERRORS_BEFORE_STOP: int = 3
	USE_PROXY_FROM_FILE: bool = False

try:
	config = Settings()
except:
	config = False