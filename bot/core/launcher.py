import os, asyncio, random, json
from argparse import ArgumentParser
from pathlib import Path
from itertools import cycle
from pyrogram import Client
from better_proxy import Proxy
from fake_useragent import UserAgent
from bot.utils.logger import log
from bot.utils.settings import config, logo
from bot.core.bot import run_bot

start_text = logo + """
Select an action:
    1. Create session
    2. Run bot
"""

def get_session_names() -> list[str]:
	session_path = Path('sessions')
	session_files = session_path.glob('*.session')
	session_names = sorted([file.stem for file in session_files])
	return session_names

async def register_sessions() -> None:
	session_name = input('\nEnter the session name (press Enter to exit): ')
	if not session_name: return None
	
	if not os.path.exists('sessions'): os.mkdir('sessions')

	session = Client(
		name=session_name,
		api_id=config.API_ID,
		api_hash=config.API_HASH,
		workdir="sessions/"
	)

	async with session: user_data = await session.get_me()
	log.success(f"Session added successfully: {user_data.username or user_data.id} | "
                   f"{user_data.first_name or ''} {user_data.last_name or ''}")

def get_proxies() -> list[Proxy]:
	if config.USE_PROXY_FROM_FILE:
		with open(file='proxies.txt', encoding='utf-8') as file:
			proxies = sorted([Proxy.from_str(proxy=row.strip()).as_url for row in file if row.strip()])
	else:
		proxies = []

	return proxies

def get_session_data(sessions: list) -> dict:
	data_file = 'session_data.json'
	data = {}
	if os.path.exists(data_file):
		try:
			with open(file=data_file, encoding='utf-8') as file:
				data = json.load(file)
		except Exception as error:
			log.error(f"Error when loading session data: {error}")
	
	all_data_exists = True if all(session in data for session in sessions) else False
	if not all_data_exists:
		ua = UserAgent(os=['android'])
		proxies = get_proxies()
		proxies_cycle = cycle(proxies) if proxies else cycle([None])
		for session in sessions:
			if not session in data:
				useragent = ua.random
				proxy = next(proxies_cycle)
				data[session] = {'ua': useragent, 'proxy': proxy}
		
		with open(data_file, 'w', encoding='utf-8') as file:
			json.dump(data, file, ensure_ascii=False, indent=4)
	
	return data

async def get_tg_clients() -> tuple[list[Client], dict]:
	session_names = get_session_names()

	if not session_names:
		raise FileNotFoundError("Not found session files")

	session_data = get_session_data(session_names)
	tg_clients = [Client(
		name=session_name,
		api_id=config.API_ID,
		api_hash=config.API_HASH,
		workdir='sessions/',
		plugins=dict(root='bot/plugins')
	) for session_name in session_names]

	return tg_clients, session_data

async def run_bot_with_delay(tg_client: Client, data: dict, delay: int) -> None:
	if delay > 0:
		log.info(f"{tg_client.name} | Wait {delay} seconds before start")
		await asyncio.sleep(delay)
	await run_bot(tg_client=tg_client, sess_data=data)

async def run_clients(tg_clients: list[Client], session_data: dict) -> None:
	tasks = []
	delay = 0
	for index, tg_client in enumerate(tg_clients):
		if index > 0:
			delay = random.randint(*config.SLEEP_BETWEEN_START)

		task = asyncio.create_task(run_bot_with_delay(tg_client=tg_client, data=session_data[tg_client.name], delay=delay))
		tasks.append(task)
	await asyncio.gather(*tasks)

async def start() -> None:
	if not config:
		log.warning(f"Please fix the above errors in the .env file")
		return
	parser = ArgumentParser()
	parser.add_argument('-a', '--action', type=int, choices=[1, 2], help='Action to perform  (1 or 2)')
	log.info(f"Detected {len(get_session_names())} sessions | {len(get_proxies())} proxies")
	action = parser.parse_args().action

	if not action:
		print(start_text)
		while True:
			action = input('> ').strip()
			if action.isdigit() and action in ['1', '2']:
				action = int(action)
				break
			log.warning("Action must be a number (1 or 2)")

	if action == 1:
		await register_sessions()
	elif action == 2:
		tg_clients, session_data = await get_tg_clients()
		await run_clients(tg_clients=tg_clients, session_data=session_data)