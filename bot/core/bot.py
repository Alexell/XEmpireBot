import asyncio, aiohttp, random, math
from time import time
from urllib.parse import unquote
from typing import Any, Dict
from aiohttp_proxy import ProxyConnector
from better_proxy import Proxy
from pyrogram import Client
from pyrogram.errors import Unauthorized, UserDeactivated, AuthKeyUnregistered
from pyrogram.raw.functions.messages import RequestWebView

from bot.utils.logger import log
from bot.utils.settings import config
from .headers import headers

class CryptoBot:
	def __init__(self, tg_client: Client):
		self.session_name = tg_client.name
		self.tg_client = tg_client
		self.api_url = 'https://api.muskempire.io'
		self.errors = 0

	async def get_tg_web_data(self, proxy: str | None) -> Dict[str, Any]:
		if proxy:
			proxy = Proxy.from_str(proxy)
			proxy_dict = dict(
				scheme=proxy.protocol,
				hostname=proxy.host,
				port=proxy.port,
				username=proxy.login,
				password=proxy.password
			)
		else:
			proxy_dict = None

		self.tg_client.proxy = proxy_dict

		try:
			if not self.tg_client.is_connected:
				try:
					await self.tg_client.connect()
				except (Unauthorized, UserDeactivated, AuthKeyUnregistered) as error:
					raise RuntimeError(str(error)) from error
			web_view = await self.tg_client.invoke(RequestWebView(
				peer=await self.tg_client.resolve_peer('muskempire_bot'),
				bot=await self.tg_client.resolve_peer('muskempire_bot'),
				platform='android',
				from_bot_menu=False,
				url='https://game.muskempire.io/'
			))
			auth_url = web_view.url
			tg_web_data = unquote(
				string=auth_url.split('tgWebAppData=', maxsplit=1)[1].split('&tgWebAppVersion', maxsplit=1)[0])
			
			user_hash = tg_web_data[tg_web_data.find('hash=') + 5:]
			self.api_key = user_hash
			if self.tg_client.is_connected:
				await self.tg_client.disconnect()
			
			login_data = {'data': {
					'initData' : tg_web_data,
					'platform' : 'android',
					'chatId' : ''
				}
			}
			return login_data

		except RuntimeError as error:
			raise error

		except Exception as error:
			log.error(f"{self.session_name} | Authorization error: {error}")
			await asyncio.sleep(delay=3)

	async def login(self, json_data: str) -> bool:
		url = self.api_url + '/telegram/auth'
		try:
			log.info(f"{self.session_name} | Trying to login...")
			self.http_client.headers.pop('Api-Key', None)
			response = await self.http_client.post(url, json=json_data)
			response.raise_for_status()
			response_json = await response.json()
			success = response_json.get('success', False)
			if success: return True
			else: return False
		except Exception as error:
			log.error(f"{self.session_name} | Login error: {error}")
			self.errors += 1
			await asyncio.sleep(delay=3)
			return False
	
	async def get_dbs(self) -> Dict[str, Any]:
		url = self.api_url + '/dbs'
		try:
			json_data = {'data': {'dbs': ['all']}}
			response = await self.http_client.post(url, json=json_data)
			response.raise_for_status()
			response_json = await response.json()
			success = response_json.get('success', False)
			if success: return response_json
			else: return {}
		except Exception as error:
			self.errors += 1
			log.error(f"{self.session_name} | Database error: {error}")
			await asyncio.sleep(delay=3)
			return {}

	async def get_profile(self, full: bool) -> Dict[str, Any]:
		url = self.api_url + '/user/data/all' if full else self.api_url + '/hero/balance/sync'
		try:
			json_data = {'data': {}} if full else {}
			response = await self.http_client.post(url, json=json_data)
			response.raise_for_status()
			response_json = await response.json()
			return response_json
		except Exception as error:
			self.errors += 1
			log.error(f"{self.session_name} | Profile data error: {error}")
			await asyncio.sleep(delay=3)
			return {}

	async def get_offline_bonus(self) -> bool:
		url = self.api_url + '/hero/bonus/offline/claim'
		try:
			response = await self.http_client.post(url, json={})
			response.raise_for_status()
			response_json = await response.json()
			success = response_json.get('success', False)
			if success: return True
			else: return False
		except Exception as error:
			self.errors += 1
			log.error(f"{self.session_name} | Offline bonus error: {error}")
			await asyncio.sleep(delay=3)
			return False

	async def daily_reward(self, index: int) -> bool:
		url = self.api_url + '/quests/daily/claim'
		try:
			json_data = {'data': f"{index}"}
			response = await self.http_client.post(url, json=json_data)
			response.raise_for_status()
			response_json = await response.json()
			success = response_json.get('success', False)
			if success: return True
			else: return False
		except Exception as error:
			log.error(f"{self.session_name} | Daily reward error: {str(error)}")
			return False
			
	async def quest_reward(self, quest: str) -> bool:
		url = self.api_url + '/quests/claim'
		try:
			json_data = {'data': [quest, None]}
			response = await self.http_client.post(url, json=json_data)
			response.raise_for_status()
			response_json = await response.json()
			success = response_json.get('success', False)
			if success: return True
			else: return False
		except Exception as error:
			log.error(f"{self.session_name} | Daily reward error: {str(error)}")
			return False
	
	async def friend_reward(self, friend: int) -> bool:
		url = self.api_url + '/friends/claim'
		try:
			json_data = {'data': friend}
			response = await self.http_client.post(url, json=json_data)
			response.raise_for_status()
			response_json = await response.json()
			success = response_json.get('success', False)
			if success: return True
			else: return False
		except Exception as error:
			log.error(f"{self.session_name} | Friend reward error: {str(error)}")
			return False
	
	async def perform_taps(self, per_tap: int, energy: int) -> None:
		url = self.api_url + '/hero/action/tap'
		log.info(f"{self.session_name} | Taps started")
		while True:
			taps_per_second = random.randint(*config.TAPS_PER_SECOND)
			seconds = random.randint(4, 6)
			earned_money = per_tap * taps_per_second * seconds
			energy_spent = math.ceil(earned_money / 2)
			energy -= energy_spent
			if energy < 0:
				log.info(f"{self.session_name} | Taps stopped (not enough energy)")
				break
			await asyncio.sleep(delay=seconds)
			try:
				json_data = {'data': {'data':{'task': {'amount': earned_money, 'currentEnergy': energy}}, 'seconds': seconds}}
				response = await self.http_client.post(url, json=json_data)
				response.raise_for_status()
				response_json = await response.json()
				success = response_json.get('success', False)
				if success:
					energy = int(response_json['data']['hero']['earns']['task']['energy'])
					log.success(f"{self.session_name} | Earned money: +{earned_money} | Energy left: {energy}")
			except Exception as error:
				log.error(f"{self.session_name} | Taps error: {str(error)}")
				self.errors += 1
				break

	async def check_proxy(self, proxy: Proxy) -> None:
		try:
			response = await self.http_client.get(url='https://httpbin.org/ip', timeout=aiohttp.ClientTimeout(5))
			ip = (await response.json()).get('origin')
			log.info(f"{self.session_name} | Proxy IP: {ip}")
		except Exception as error:
			log.error(f"{self.session_name} | Proxy: {proxy} | Error: {error}")

	async def run(self, proxy: str | None) -> None:
		proxy_conn = ProxyConnector().from_url(proxy) if proxy else None

		async with aiohttp.ClientSession(headers=headers, connector=proxy_conn) as http_client:
			self.http_client = http_client
			if proxy:
				await self.check_proxy(proxy=proxy)

			self.authorized = False
			while True:
				if self.errors >= config.ERRORS_BEFORE_STOP:
					log.error(f"{self.session_name} | Bot stopped (too many errors)")
					break
				try:
					if not self.authorized:
						login_data = await self.get_tg_web_data(proxy=proxy)
						if await self.login(json_data=login_data):
							log.success(f"{self.session_name} | Login successful")
							self.authorized = True
							self.http_client.headers['Api-Key'] = self.api_key
							#self.dbs = await self.get_dbs()
							full_profile = await self.get_profile(full=True)
							offline_bonus = int(full_profile['data']['hero']['offlineBonus'])
							if offline_bonus > 0:
								if await self.get_offline_bonus():
									log.success(f"{self.session_name} | Offline bonus claimed: +{offline_bonus}")
							else:
								log.info(f"{self.session_name} | Offline bonus not available")
						else: continue
						
					profile = await self.get_profile(full=False)					
					log.info(f"{self.session_name} | Level: {profile['data']['hero']['level']} | "
								f"Balance: {profile['data']['hero']['money']} | "
								f"Money per hour: {profile['data']['hero']['moneyPerHour']}")
					
					daily_rewards = full_profile['data']['dailyRewards']
					daily_index = None
					for day, status in daily_rewards.items():
						if status == 'canTake':
							daily_index = day
							break
					if daily_index is not None:
						log.info(f"{self.session_name} | Daily reward available")
						daily_claimed = await self.daily_reward(index=daily_index)
						if daily_claimed:
							log.success(f"{self.session_name} | Daily reward claimed")
							self.errors = 0
					else:
						log.info(f"{self.session_name} | Daily reward not available")
					
					unrewarded_quests = [quest['key'] for quest in full_profile['data']['quests'] if not quest['isRewarded']]
					if unrewarded_quests:
						log.info(f"{self.session_name} | Quest rewards available")
						for quest in unrewarded_quests:
							if await self.quest_reward(quest=quest):
								log.success(f"{self.session_name} | Reward for quest {quest} claimed")
					
					unrewarded_friends = [int(friend['id']) for friend in full_profile['data']['friends'] if friend['bonusToTake'] > 0]
					if unrewarded_friends:
						log.info(f"{self.session_name} | Reward for friends available")
						for friend in unrewarded_friends:
							if await self.friend_reward(friend=friend):
								log.success(f"{self.session_name} | Reward for friend {friend} claimed")
					
					per_tap = profile['data']['hero']['earns']['task']['moneyPerTap']
					max_energy = profile['data']['hero']['earns']['task']['limit']
					energy = profile['data']['hero']['earns']['task']['energy']
					if energy == max_energy:
						await self.perform_taps(per_tap=per_tap, energy=energy)

					profile = await self.get_profile(full=False)
					log.info(f"{self.session_name} | Level: {profile['data']['hero']['level']} | "
								f"Balance: {profile['data']['hero']['money']} | "
								f"Money per hour: {profile['data']['hero']['moneyPerHour']}")
					
					log.info(f"{self.session_name} | Sleep 1 hour")
					await asyncio.sleep(3600)
					self.authorized = False
					
				except RuntimeError as error:
					raise error
				except Exception as error:
					log.error(f"{self.session_name} | Unknown error: {error}")
					await asyncio.sleep(delay=3)
				else:
					log.info(f"Sleep 1 min")
					await asyncio.sleep(delay=60)

async def run_bot(tg_client: Client, proxy: str | None):
	try:
		await CryptoBot(tg_client=tg_client).run(proxy=proxy)
	except RuntimeError as error:
		log.error(f"{tg_client.name} | Session error: {str(error)}")
