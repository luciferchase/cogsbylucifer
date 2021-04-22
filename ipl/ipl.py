import discord
from redbot.core import commands, Config
import requests
import json
from datetime import date
import calendar

BaseCog = getattr(commands, "Cog", object)


class IPL(BaseCog):
	"""IPL"""
	def __init__(self, bot):
		with open("C:/Users/udit2/Codes/Python Code/cogsbylucifer/ipl/settings.json", "r+") as settings:
			self.settings_data = json.load(settings)

		self.config = Config.get_conf(self)

		self.api = "https://cricapi.com/api/"
		self.api_endpoint = ["matches"]
		self.api_key = settings_data["api_key"]
		self.api_hits = settings_data["api_hits"]

	@commands.group(invoke_without_command = True)
	@commands.bot_has_permissions(embed_links = True)
	async def ipl(self, ctx):
		
		if (date.today() > settings_data["matches"]["last_requested"]):
			settings_data["api_limit"] = 0
			settings_data["matches"]["last_requested"] = date.today()
			settings_data["matches"]["last_match_id"] += 1

			with open("settings.json", "w") as settings:
				json.dump(settings_data, settings)

			response = requests.get(f"{api}{api_endpoint}?{api_key}")

			with open("matches.json", "w") as matches:
				json_object = json.dumps(response.json(), indent = 2)
				matches.write(json_object)

		with open("settings.json", "r") as settings:
			settings_data = json.load(settings)

		last_match_id = settings_data["last_match_id"]
		with open("matches.json", "r") as matches:
			data = json.load(matches)

			for i in data["matches"]:
				if (i["unique_id"] == last_match_id):
					last_match_details = i
				elif (i["unique_id"] == last_match_id + 1):
					upcoming_match_details = i

		embed = discord.Embed(
			color = await self.bot.get_embed_color(ctx.channel),
			title = "Matches",
			timestamp = date.today(),
		)
		embed.add_field(
			name = "Last Match",
			value = f'{last_match_details["team-1"]} vs {last_match_details["team-2"]}',
			inline = True
		)
		embed.add_field(
			name = "Winner",
			value = f'{last_match_details["winner_team"]}',
			inline = True
		)
		embed.add_field(
			name = "Next Match", 
			value = f'{["team-1"]} vs {["team-2"]}',
			inline = False
		)

		if (calendar.day_name[date.today().weekday()] in ["Saturday", "Sunday"]):
			embed.add_field(
			name = "Match 2", 
			value = f'{["team-1"]} vs {["team-2"]}',
			inline = False
			)

		embed.set_image(url = "https://i.pinimg.com/originals/a2/20/30/a220301dbfa84edd4ffc6ce9bb528841.png")
		await ctx.send(embed = embed)

