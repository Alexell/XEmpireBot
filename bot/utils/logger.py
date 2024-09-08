import sys
import requests
import time
from threading import Thread
from queue import Queue
from loguru import logger
from bot.utils.settings import config

# Define the Telegram API URL
TELEGRAM_API_URL = f"https://api.telegram.org/bot{config.BOT_TOKEN}/sendMessage"
message_queue = Queue()

def send_to_telegram(message, retries=3):
    delay = 2  # Start with a 2-second delay
    for attempt in range(retries):
        try:
            # Attempt to send the log message to Telegram
            response = requests.post(TELEGRAM_API_URL, data={'chat_id': config.CHAT_ID, 'text': message})
            if response.status_code == 200:
                return  # Message sent successfully
            else:
                log.error(f"Failed to send log to Telegram: {response.text}")
        except Exception as e:
            log.error(f"Failed to send log to Telegram: {e}")
        time.sleep(delay)  # Wait before retrying
        delay *= 2  # Exponential backoff for retries
    log.error(f"Failed to send log to Telegram after {retries} retries.")

def process_queue():
    """Process messages from the queue and send them to Telegram."""
    while True:
        message = message_queue.get()
        if message is None:  # Graceful exit
            break
        try:
            time.sleep(3)  # Simulate some delay before sending
            send_to_telegram(message)
        except Exception as e:
            log.error(f"Error in processing queue: {e}")
        finally:
            message_queue.task_done()

def stop_processing():
    """Stop the queue processing thread gracefully."""
    message_queue.put(None)  # Stop the thread by sending a sentinel value
    thread.join()  # Wait for the thread to finish

# Start the background thread to process the queue
thread = Thread(target=process_queue, daemon=True)
thread.start()

# Loguru logger configuration
logger.remove()  # Remove default Loguru configuration
logger.add(sink=sys.stdout, format="<white>{time:YYYY-MM-DD HH:mm:ss}</white>"
                                   " | <level>{level: <8}</level>"
                                   " | <cyan><b>{line}</b></cyan>"
                                   " | <white><b>{message}</b></white>")
log = logger.opt(colors=True)  # Define the colored log object

# Adding Telegram logging if enabled in config
if config.USE_TG_BOT:
    logger.add(lambda msg: message_queue.put(msg), format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {message}", level="INFO")

# Usage examples
log.info("This is a standard log message.")
log.error("This is an error log with line number.")
