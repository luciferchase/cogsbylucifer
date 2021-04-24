import discord
from redbot.core import commands
import requests
import json
from datetime import date

BaseCog = getattr(commands, "Cog", object)

class Wallpaper(BaseCog):
	
	@commands.command()
	async def wallpaper(self, ctx, *query):
		""" Get a wallpaper from Unsplash. To fetch a specific wallpaper, append the query to the last
			For eg. ```luci walllpaper minimal```
		"""
		api = "https://api.unsplash.com"
		endpoint = "/search/photos"
		params = {
			"client_id": "ZMAa9VvX1-tnTAYej4bU7vdxiJPcEAb-YH70iBL7V20",
			"query": "wallpapers",
			"page": "1",
		}

		query_params = [f"{param}={params[param]}" for param in params]
		if (len(query) != 0):
			query_params[1] = f"query={'%20'.join(query)}%20{params['query']}"

		response = requests.get(f"{api}{endpoint}?{'&'.join(query_params)}")

		json.dump(data, f, indent = 2)

		likes = {}
		for photo in data["results"]:
			likes[photo["id"]] = photo["likes"]
		photo_info = [photo for photo in data["results"] if photo["id"] == max(likes)][0]
		if (photo_info["description"] == None):
			photo_info["description"] = photo_info["alt_description"]
		
		embed = discord.Embed(
			title = str(date.today()),
			description = f'{photo_info["description"][:50]}...',
			url = photo_info["urls"]["regular"],
			color = 0xf5009b
		)
		embed.set_author(
			name = photo_info["user"]["name"],
			url = f'https://unsplash.com/@{photo_info["user"]["username"]}',
			icon_url = photo_info["user"]["profile_image"]["large"]
		)
		embed.set_thumbnail(url = photo_info["user"]["profile_image"]["large"])
		embed.set_image(url = photo_info["urls"]["full"])
		embed.set_footer(text = f"❤️ {photo_info['likes']}")

		await ctx.send(embed = embed)

	@commands.command()
	async def bingwallpaper(self, ctx):
		""" Get Bing's daily wallpaper of the day
		"""
		api = "https://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=en-IN"

		response = requests.get(api)
		data = response.json()

		await ctx.send(data["images"][0]["title"])
		await ctx.send(f'http://bing.com{data["images"][0]["url"]}')