import discord
from redbot.core import commands
import requests
import json

BaseCog = getattr(commands, "Cog", object)

class Meme(BaseCog):
	def __init__(self):
		self.api = "https://meme-api.herokuapp.com/gimme"

	@commands.command()
	async def meme(self, ctx, endpoint = ""):
		""" Get a meme from reddit
		"""
		if (endpoint != ""):
			response = requests.get(self.api + "/" + endpoint).json()
		else:
			response = requests.get(self.api + "/" + "dankmemes").json()


		if ("code" in response.keys()):
			embed = discord.Embed(
				title = response["message"],
				color = 0xea1010
			)
			embed.set_image(url = f"https://http.cat/{response['code']}")
			await ctx.send(embed = embed)
			return
		elif (response["nsfw"]):
			response = requests.get(self.api)
		
		embed = discord.Embed(
			color = 0x06f9f5,
			title = response["title"],
			url = response["postLink"]
		)
		embed.set_image(url = response["url"])
		embed.set_footer(text = f'👍 {response["ups"]}')
		await ctx.send(embed = embed)