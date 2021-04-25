import discord
from redbot.core import commands
from TagScriptEngine import Interpreter, adapter, block

import requests
import json
import logging
import time

BaseCog = getattr(commands, "Cog", object)

class Math(BaseCog):

	def __init__(self, bot):
		self.bot = bot
		blocks = [
			block.MathBlock(),
			block.RandomBlock(),
			block.RangeBlock(),
		]
		self.engine = Interpreter(blocks)

	async def red_delete_data_for_user(self, **kwargs):
		return

	
	@commands.command()
	async def math(self, ctx, *expression):
		""" Solve a math expression. Supports very complex problems too.
			For eg. `luci math sin(pi/4)`
		"""
		log = logging.getLogger("red.cogsbylucifer.math")

		if (expression == ""):
			embed = discord.Embed(
			color = 0xea1010,
			title = "Input A Expression"
			)
			await ctx.send(embed = embed)
			return

		start = time.monotonic()

		api = "http://api.mathjs.org/v4/"
		params = {
			"expr": "".join(expression) 
		}
		response = requests.get(url = api, params = params)
		end = time.monotonic()

		if (str(response.status_code)[:2] == "40"):
			log.info(expression)
			log.error(response.text)

		embed = discord.Embed(
			color = await ctx.embed_color(),					
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
		embed.set_footer(text = f"Calculated in {round((end - start) * 1000, 3)} ms")
		await ctx.send(embed = embed)

	@commands.command(aliases=["calc"])
	async def calculate(self, ctx, *, query):
		""" Faster but sometimes does not work.
		"""
		
		query = query.replace(",", "")
		engine_input = "{m:" + query + "}"
		start = time.monotonic()
		output = self.engine.process(engine_input)
		end = time.monotonic()

		output_string = output.body.replace("{m:", "").replace("}", "")
		embed = discord.Embed(
			color = await ctx.embed_color(),
			title = f"Input: `{query}`",
			description = f"Output: `{output_string}`",
		)
		embed.set_footer(text = f"Calculated in {round((end - start) * 1000, 3)} ms")
		await ctx.send(embed = embed)
