import discord
from redbot.core import commands, Config
import requests
import json
from datetime import date
import calendar

BaseCog = getattr(commands, "Cog", object)


class IPL(BaseCog):
	"""IPL"""
	@commands.bot_has_permissions(embed_links = True)
	@commands.command()
	async def ipl(self, ctx):

		with open("C:/Users/udit2/Codes/Python Code/cogsbylucifer/ipl/config.json", "r+") as config:
			global config_data
			config_data = json.load(config)
		print(config_data)

		api = "https://cricapi.com/api/"
		api_endpoint = ["matches"]
		api_key = config_data["api_key"]
		api_hits = config_data["api_hits"]

		if (str(date.today()) > config_data["matches"]["last_requested"]):
			config_data["api_limit"] = 0
			config_data["matches"]["last_requested"] = str(date.today())
			config_data["matches"]["last_match_id"] += 1

			with open("config.json", "w") as config:
				json.dump(config_data, config)

			response = requests.get(f"{api}{api_endpoint}?{api_key}")

			with open("matches.json", "w") as matches:
				json_object = json.dumps(response.json(), indent = 2)
				matches.write(json_object)

		last_match_id = config_data["matches"]["last_match_id"]
		with open("C:/Users/udit2/Codes/Python Code/cogsbylucifer/ipl/matches.json", "r") as matches:
			data = json.load(matches)

			for i in data["matches"]:
				if (i["unique_id"] == last_match_id):
					last_match_details = i
				elif (i["unique_id"] == last_match_id + 1):
					upcoming_match_details = i
		image_url = {
			"Kolkata Knight Riders": "https://hdsportsnews.com/wp-content/uploads/2020/01/kolkata-knight-riders-kkr-2020-team-squad-players-live-score-time-table-point-table-schedule-auction-match-fixture-venue-highlight-1280x720.jpg",
			"Rajasthan Royals": "https://cdn5.newsnationtv.com/images/2021/02/22/royal-rajasthan-logo-70.jpg",
			"Royal Challengers Bangalore": "https://english.sakshi.com/sites/default/files/article_images/2020/11/8/RCB-Logo_571_855-1604821493.jpg",
			"Mumbai Indians": "https://static.india.com/wp-content/uploads/2017/03/mumbai.jpg?impolicy=Medium_Resize&w=1200&h=800",
			"Punjab Kings": "https://awaj.in/wp-content/uploads/2021/03/20210317_222651.jpg",
			"Sunrisers Hyderabad": "https://2.bp.blogspot.com/-6cAZUQMFCqc/WwKFUZrPPmI/AAAAAAAACcM/TryzryihpEkoOMd6htpE8LjIH1r02FWSgCLcBGAs/s1600/SRH.jpg",
			"Chennai Super Kings": "https://i.pinimg.com/originals/85/52/f8/8552f811e95b998d9505c43a9828c6d6.jpg",
			"Delhi Capitals": "https://d3pc1xvrcw35tl.cloudfront.net/ln/images/686x514/teamsinnerintrodc534x432-resize-534x432-a7542dd51f-d979030f10e79596_202009106828.jpeg"
		}
		embed = discord.Embed(
			color = 0x25dbf4,
			title = "Matches",
		)

		embed.add_field(
			name = "Next Match", 
			value = f'{upcoming_match_details["team-1"]} \nvs \n{upcoming_match_details["team-2"]}',
			inline = False
		)
		if (calendar.day_name[date.today().weekday()] in ["Saturday", "Sunday"]):
			embed.add_field(
			name = "Match 2", 
			value = f'{["team-1"]} vs {["team-2"]}',
			inline = False
			)
		embed.add_field(
			name = "Last Match",
			value = f'{last_match_details["team-1"]} \nvs \n{last_match_details["team-2"]}',
			inline = True
		)
		embed.add_field(
			name = "Winner",
			value = f'{last_match_details["winner_team"]}',
			inline = True
		)
		embed.set_image(url = image_url[last_match_details["winner_team"]])
		await ctx.send(embed = embed)

