from discord.ext import commands, tasks
from discord.utils import get
from discord import app_commands
from typing import Union
import requests
import json

class ProductCreation(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot
        self.description = "Licensing system"
        self.db = False
    @app_commands.describe(user="Create a product for the licensing system")
    @commands.hybrid_command(name="createproduct", description="Create a product for the licensing system")
    async def _createproduct(self, ctx: commands.Context, *, product: commands.clean_content):
        if (ctx.guild.get_role(1075407711333785700) not in ctx.message.author.roles):
            return await ctx.channel.send("No permission.")

        url = f"https://ducky-license.meliniumc.workers.dev/products/{product}"
        querystring = {"type":"name"}
        headers = {"Content-Type": "application/json"}
        response = requests.request("GET", url, headers=headers, params=querystring)
        response_json = json.loads(response.text)
        if response_json["success"]:
            return await ctx.reply(f"The product {product} already exists.", ephemeral=False)
        else:
            url = "https://ducky-license.meliniumc.workers.dev/products"
            payload = {"name": f"{product}"}
            headers = {
                "Content-Type": "application/json",
                "x-ducky-key": "SuperSpeak3714!"
            }
            response = requests.request("POST", url, json=payload, headers=headers)
            response_json = json.loads(response.text)
            if response_json["success"]:
                return await ctx.reply(f"Successfully created product {product}.", ephemeral=False)
            else:
                return await ctx.reply(f"An error occurred while creating the product {product}.", ephemeral=False)
async def setup(bot: commands.Bot):
    await bot.add_cog(ProductCreation(bot))