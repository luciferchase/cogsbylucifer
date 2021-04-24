import discord
from redbot.core import commands
import requests
import json
from datetime import date
import calendar

BaseCog = getattr(commands, "Cog", object)

class IPL(BaseCog):
	def __init__(self, bot):
		self.bot = bot

		with open("C:/Users/udit2/Codes/Python Code/cogsbylucifer/ipl/config.json", "r+") as config:
			self.config_data = json.load(config)

		self.api = "https://cricapi.com/api/"
		self.api_endpoint = ["matches", ]
		self.api_key = self.config_data["api_key"]

		if (str(date.today()) > self.config_data["matches"]["last_requested"]):
			self.config_data["matches"]["last_requested"] = str(date.today())
			self.config_data["matches"]["last_match_id"] += 1

			with open("C:/Users/udit2/Codes/Python Code/cogsbylucifer/ipl/config.json", "w") as config:
				json.dump(self.config_data, config, indent = 4)

			response = requests.get(f"{api}{api_endpoint[0]}?apikey={api_key}")

			with open(\
				"C:/Users/udit2/Codes/Python Code/cogsbylucifer/ipl/matches.json", "w") as matches:
				json.dump(response.json(), matches, indent = 2)

		self.last_match_id = self.config_data["matches"]["last_match_id"]

		with open("C:/Users/udit2/Codes/Python Code/cogsbylucifer/ipl/matches.json", "r") as matches:
			data = json.load(matches)

			for match in data["matches"]:
				if (match["unique_id"] == self.last_match_id):
					self.last_match_details = match
				elif (match["unique_id"] == self.last_match_id + 1):
					self.upcoming_match_details = match
				elif (match["unique_id"] == self.last_match_id + 2):
					self.upcoming_match_details_2 = match

		self.image_url = {
			"Kolkata Knight Riders": "https://hdsportsnews.com/wp-content/uploads/2020/01/kolkata-knight-riders-kkr-2020-team-squad-players-live-score-time-table-point-table-schedule-auction-match-fixture-venue-highlight-1280x720.jpg",			
			"Rajasthan Royals": "https://cdn5.newsnationtv.com/images/2021/02/22/royal-rajasthan-logo-70.jpg",			
			"Royal Challengers Bangalore": "https://english.sakshi.com/sites/default/files/article_images/2020/11/8/RCB-Logo_571_855-1604821493.jpg",			
			"Mumbai Indians": "https://static.india.com/wp-content/uploads/2017/03/mumbai.jpg?impolicy=Medium_Resize&w=1200&h=800",			
			"Punjab Kings": "https://awaj.in/wp-content/uploads/2021/03/20210317_222651.jpg",			
			"Sunrisers Hyderabad": "https://2.bp.blogspot.com/-6cAZUQMFCqc/WwKFUZrPPmI/AAAAAAAACcM/TryzryihpEkoOMd6htpE8LjIH1r02FWSgCLcBGAs/s1600/SRH.jpg",			
			"Chennai Super Kings": "https://i.pinimg.com/originals/85/52/f8/8552f811e95b998d9505c43a9828c6d6.jpg",			
			"Delhi Capitals": "https://d3pc1xvrcw35tl.cloudfront.net/ln/images/686x514/teamsinnerintrodc534x432-resize-534x432-a7542dd51f-d979030f10e79596_202009106828.jpeg"
		}

		self.ipl_logo = "https://img.etimg.com/thumb/width-1200,height-900,imgsize-121113,resizemode-1,msid-81376248/ipl-2021-from-april-9-six-venues-no-home-games-no-spectators.jpg"

	@commands.bot_has_permissions(embed_links = True)
	@commands.command()
	async def ipl(self, ctx):
		""" Get details of last match played, winner and the next match
		"""

		embed = discord.Embed(
			color = 0x25dbf4,
			title = "Matches",
		)
		embed.add_field(
			name = "Next Match", 
			value = f'{self.upcoming_match_details["team-1"]} \nvs \
			\n{self.upcoming_match_details["team-2"]}',
			inline = False
		)
		if (calendar.day_name[date.today().weekday()] in ["Saturday", "Sunday"]):
			embed.add_field(
			name = "Match 2", 
			value = f'{upcoming_match_details_2["team-1"]} vs {upcoming_match_details_2["team-2"]}',
			inline = False
			)
		embed.add_field(
			name = "Last Match",
			value = f'{self.last_match_details["team-1"]} \nvs \n{self.last_match_details["team-2"]}',
			inline = True
		)
		embed.add_field(
			name = "Winner",
			value = f'{self.last_match_details["winner_team"]}',
			inline = True
		)
		embed.set_image(url = self.image_url[self.last_match_details["winner_team"]])
		embed.set_thumbnail(url = self.ipl_logo)
		await ctx.send(embed = embed)

	@commands.bot_has_permissions(embed_links = True)
	@commands.command(hidden = True)
	async def predict(self, ctx):
		""" Poll for today's match
		"""
		await ctx.send("@everyone")

		embed = discord.Embed(
			color = 0x19f0e2,
			title = "Sattebaaz Championship",
		)
		embed.add_field(
			name = "Who do you think will win today's match?",
			value = f':regional_indicator_a: {self.upcoming_match_details["team-1"]}\n\
			:regional_indicator_b: {self.upcoming_match_details["team-2"]}'
		)
		embed.set_thumbnail(url = self.ipl_logo)

		last_embed = await ctx.send(embed = embed)
		await last_embed.add_reaction("🇦")
		await last_embed.add_reaction("🇧")
		self.config_data["predict"]["embed_id"] = last_embed.id
		self.config_data["predict"]["channel_id"] = last_embed.channel.id

		with open("C:/Users/udit2/Codes/Python Code/cogsbylucifer/ipl/config.json", "w") as config:
			json.dump(self.config_data, config, indent = 4)

	@commands.bot_has_permissions(embed_links = True)
	@commands.command(hidden = True)
	async def points(self, ctx):
		""" Update Standings for Sattebaaz Championship
		"""

		channel = self.bot.get_channel(self.config_data["predict"]["channel_id"])
		last_embed = await channel.fetch_message(self.config_data["predict"]["embed_id"])
		emoji_a = []
		emoji_b = []
		winners = []
		for reaction in last_embed.reactions:
			async for user in reaction.users():
				if (reaction.emoji == "🇦" and user.id != 829537216224165888):
					emoji_a.append(str(user.id))
				elif (reaction.emoji == "🇧" and user.id != 829537216224165888):
					emoji_b.append(str(user.id))

		if (self.last_match_details["winner_team"] == self.last_match_details["team-1"]):
			for user in emoji_a:
				self.config_data["predict"]["users"][user] += 10
				winners.append(user)
		else:
			for user in emoji_b:
				self.config_data["predict"]["users"][user] += 10
				winners.append(user)

		with open("C:/Users/udit2/Codes/Python Code/cogsbylucifer/ipl/config.json", "w") as config:
			json.dump(self.config_data, config, indent = 4)

		embed = discord.Embed(
			color = 0x07f223,
			title = "Sattebaaz Championship",
		)
		embed.add_field(
			name = "Last match was won by ...",
			value = self.last_match_details["winner_team"],
			inline = False
		)

		for user in winners:
			embed.add_field(
				name = "Winning sattebaaz",
				value = f"`{await self.bot.fetch_user(user)}`",
				inline = False
			)

		embed.set_image(url = self.image_url[self.last_match_details["winner_team"]])
		embed.set_thumbnail(url = self.ipl_logo)
		await ctx.send(embed = embed)

		points = {}
		for user in self.config_data["predict"]["users"]:
			username = await self.bot.fetch_user(user)
			points[username] = self.config_data["predict"]["users"][user]

		embed_string_name = ""
		embed_string_points = ""
		for user in points:
			embed_string_name += f"\n{user}\n"
			embed_string_points += f"\n : \t {points[user]}\n"

		embed = discord.Embed(
			color = 0x07f223,
			title = "Sattebaaz Championship",
		)
		embed.add_field(
			name = "Current Standings",
			value = f"```\n{embed_string_name}```",
			inline = True
		)
		embed.add_field(
			name = "Points",
			value = f"```\n{embed_string_points}```",
			inline = True
		)
		embed.set_thumbnail(url = self.ipl_logo)
		await ctx.send(embed = embed)

	@commands.command()
	async def standings(self, ctx):
		""" See current standings of Sattebaaz Championship
		"""
		
		points = {}
		for user in self.config_data["predict"]["users"]:
			username = await self.bot.fetch_user(user)
			points[username] = self.config_data["predict"]["users"][user]

		embed_string_name = ""
		embed_string_points = ""
		for user in points:
			embed_string_name += f"\n{user}\n"
			embed_string_points += f"\n : \t {points[user]}\n"

		embed = discord.Embed(
			color = 0x07f223,
			title = "Sattebaaz Championship",
		)
		embed.add_field(
			name = "Current Standings",
			value = f"```\n{embed_string_name}```",
			inline = True
		)
		embed.add_field(
			name = "Points",
			value = f"```\n{embed_string_points}```",
			inline = True
		)
		embed.set_thumbnail(url = self.ipl_logo)
		await ctx.send(embed = embed)
