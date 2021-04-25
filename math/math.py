import discord
from redbot.core import commands
import requests
import json
import logging

BaseCog = getattr(commands, "Cog", object)

class Math(BaseCog):
	
	@commands.command()
	async def math(self, ctx, *expression):
		""" Solve a math expression. Supports very complex problems too.
			For eg. `luci math sin(pi/4)`
		"""
		log = logging.getLogger("red.cogsbylucifer.math")

		if (expression == ""):
			embed = discord.Embed(
			color = 0xea1010,
			title = "Input Expression"
			)
			await ctx.send(embed = embed)
			return
		
		api = "http://api.mathjs.org/v4/"
		params = {
			"expr": "".join(expression) 
		}
		response = requests.get(url = api, params = params)

		if (str(response.status_code)[:2] == "40"):
			color = 0xea1010					# Red
			log.info(expression)
			log.error(response.text)
		else:
			color = 0xb32cf2					# Purple-ish

		embed = discord.Embed(
			color = color,					
			title = response.text
		)
		embed.add_field(
			name = "Your Input:",
			value = f'`{"".join(expression)}`',
			inline = True
		)
		embed.add_field(
			name = "Answer:",
			value = response.text,
			inline = True
		)
		await ctx.send(embed = embed)