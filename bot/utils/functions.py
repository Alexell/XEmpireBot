from time import time
from datetime import datetime, timezone
from typing import Any, Dict

########## SKILLS ##########

# functions from game js
def get_price(e, t):
	return calculate(e['priceFormula'], t, e['priceBasic'], e['priceFormulaK']) if t else 0

def get_profit(e, t):
	return calculate(e['profitFormula'], t, e['profitBasic'], e['profitFormulaK'], e) if t else 0

def calculate(e, t, s, c, r=None):
	i = s
	if e == "fnCompound":
		i = fn_compound(t, s, c)
	elif e == "fnLogarithmic":
		i = fn_logarithmic(t, s)
	elif e == "fnLinear":
		i = fn_linear(t, s)
	elif e == "fnQuadratic":
		i = fn_quadratic(t, s)
	elif e == "fnCubic":
		i = fn_cubic(t, s)
	elif e == "fnExponential":
		i = fn_exponential(t, s, c)
	elif e == "fnPayback":
		i = fn_payback(t, r)

	return smart_round(i)

def tr(s, c=100):
	return round(s / c) * c

def smart_round(e):
	if e < 50:
		return round(e)
	elif e < 100:
		return tr(e, 5)
	elif e < 500:
		return tr(e, 25)
	elif e < 1000:
		return tr(e, 50)
	elif e < 5000:
		return tr(e, 100)
	elif e < 10000:
		return tr(e, 200)
	elif e < 100000:
		return tr(e, 500)
	elif e < 500000:
		return tr(e, 1000)
	elif e < 1000000:
		return tr(e, 5000)
	elif e < 50000000:
		return tr(e, 10000)
	elif e < 100000000:
		return tr(e, 50000)
	else:
		return tr(e, 100000)

def fn_linear(e, t):
	return t * e

def fn_quadratic(e, t):
	return t * e * e

def fn_cubic(e, t):
	return t * e * e * e

def fn_exponential(e, t, s):
	return t * (s / 10) ** e

def fn_logarithmic(e, t):
	import math
	return t * math.log2(e + 1)

def fn_compound(e, t, s):
	c = s / 100
	return t * (1 + c) ** (e - 1)

def fn_payback(e, t):
	s = [0]
	for c in range(1, e + 1):
		r = s[c - 1]
		i = get_price(t, c)
		S = t['profitBasic'] + t['profitFormulaK'] * (c - 1)
		L = smart_round(r + i / S)
		s.append(L)
	return s[e]

# main function for calculating the most profitable skill
def calculate_best_skill(skills: list, profile: Dict[str, Any], level: int, balance: int, improve: Dict[str, Any] | None) -> Dict[str, Any] | None:
	friends = profile["data"]["profile"]["friends"]
	if improve is not None:
		my_skills = improve["data"]["skill"]
	else:
		my_skills = profile["data"]["skills"]
	
	for my_skill, my_limit in my_skills.items():
		if type(my_limit["finishUpgradeDate"]) is str:
			my_skills[my_skill]["finishUpgradeDate"] = datetime.strptime(my_limit["finishUpgradeDate"], "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc).timestamp()
	
	qualified_skills = []
	for skill in skills:
		qualified = False
		if skill['key'] in my_skills: # skill found, check for improve
			my_skill = my_skills[skill['key']]
			skill_price = get_price(skill, my_skill['level'] + 1)
			current_profit = get_profit(skill, my_skill['level'])
			next_profit = get_profit(skill, my_skill['level'] + 1)
			skill_profit = next_profit - current_profit
			if skill['maxLevel'] <= my_skill['level']: continue
			if (0 if my_skill['finishUpgradeDate'] is None else my_skill['finishUpgradeDate']) < time() and balance > skill_price:
				if not skill['levels']: qualified = True
				else:
					matched_skill_limit = None
					for skill_limit in skill['levels']:
						if my_skill['level'] == skill_limit['level'] - 1:
							matched_skill_limit = skill_limit
							break
					if matched_skill_limit is None: qualified = True
					elif matched_skill_limit['requiredHeroLevel'] <= level and matched_skill_limit['requiredFriends'] <= friends:
						if not matched_skill_limit['requiredSkills']: qualified = True
						else:
							for req_skill, req_level in matched_skill_limit['requiredSkills'].items():
								if my_skills.get(req_skill, {}).get('level', 0) >= req_level: qualified = True
		else: # skill not found, check for buy
			skill_price = get_price(skill, 1)
			skill_profit = get_profit(skill, 1)
			if balance > skill_price and not skill['levels']: qualified = True
			else:
				skill_limit = skill['levels'][0]
				if skill_limit['requiredHeroLevel'] <= level and skill_limit['requiredFriends'] <= friends:
					if not skill_limit['requiredSkills']: qualified = True
					else:
						for req_skill, req_level in skill_limit['requiredSkills'].items():
							if my_skills.get(req_skill, {}).get("level", 0) >= req_level: qualified = True

		if qualified:
			skill['ratio'] = skill_profit / skill_price
			skill['price'] = skill_price
			skill['profit'] = skill_profit
			skill['newlevel'] = my_skills.get(skill['key'], {}).get('level', 0) + 1 # new level for improve or 1 level for buy
			qualified_skills.append(skill)
	
	best_skill = sorted(qualified_skills, key=lambda x: x["ratio"])[-1]
	if len(best_skill) > 0: return best_skill
	else: return None


########## MATH ##########

def calculate_bet(level: int, mph: int, balance: int) -> int:
	bet_steps_count = 7 # from game js, may be changed in the future
	def smart_zero_round(amount):
		def round_to_nearest(value, base=100):
			return round(value / base) * base

		if amount < 100:
			return round_to_nearest(amount, 50)
		elif amount < 1000:
			return round_to_nearest(amount, 100)
		elif amount < 10000:
			return round_to_nearest(amount, 1000)
		elif amount < 100000:
			return round_to_nearest(amount, 10000)
		elif amount < 1000000:
			return round_to_nearest(amount, 100000)
		elif amount < 10000000:
			return round_to_nearest(amount, 1000000)
		elif amount < 100000000:
			return round_to_nearest(amount, 10000000)
		else:
			return round_to_nearest(amount, 1000)

	def min_bet():
		multiplier = 2
		if level < 3:
			multiplier = 5
		elif level < 6:
			multiplier = 4
		elif level < 10:
			multiplier = 3

		calculated_bet = smart_zero_round(mph * multiplier / (bet_steps_count * 3))
		return calculated_bet or 100

	def max_bet():
		return min_bet() * bet_steps_count
	
	avail_bet = 0
	max_bet = max_bet()
	if max_bet < balance:
		avail_bet = max_bet
	else: # reduce the bet if there is not enough money
		min_bet = min_bet()
		while max_bet > balance and max_bet - min_bet >= min_bet:
			max_bet -= min_bet
		avail_bet = max(max_bet, min_bet)
	
	return avail_bet
	
def number_short(value: int, round_value: bool = False) -> str:
	n = 1 if value >= 0 else -1
	
	if abs(value) < 1e3:
		return round(value)
	
	if abs(value) >= 1e3 and abs(value) < 1e6:
		result = value / 1e3
		return f"{(round(result) if round_value or result % 1 == 0 else int(result * 10) / 10)}K"
	
	if abs(value) >= 1e6 and abs(value) < 1e9:
		result = value / 1e6
		return f"{(round(result) if round_value or result % 1 == 0 else int(result * 10) / 10)}M"
	
	if abs(value) >= 1e9 and abs(value) < 1e12:
		result = value / 1e9
		return f"{(round(result) if round_value or result % 1 == 0 else int(result * 10) / 10)}B"
	
	if abs(value) >= 1e12:
		result = value / 1e12
		return f"{(round(result) if round_value or result % 1 == 0 else int(result * 10) / 10)}T"