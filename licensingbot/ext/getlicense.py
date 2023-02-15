from discord.ext import commands, tasks
from discord.utils import get
from discord import app_commands, Embed
from typing import Union
import requests
import json
from datetime import datetime
import discord

class LicenseCheck(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot
        self.description = "Licensing system"
        self.db = False
    @app_commands.describe(user="Gets the information of a license")
    @commands.hybrid_command(name="getlicense", description="Gets the information of a license")
    async def _getlicense(self, ctx: commands.Context, *, license: commands.clean_content):
        if (ctx.guild.get_role(1075407711333785700) not in ctx.message.author.roles):
            return await ctx.reply("No permission.")
        url = "https://ducky-license.meliniumc.workers.dev/licenses/DUCKY-_GYdWS1SBG9SjiRRuUocqz6I?type=license"
        payload = ""
        headers = ""
        response = requests.request("GET", url, data=payload, headers=headers)
        response_json = json.loads(response.text)
        if not response_json["success"]:
            return await ctx.reply(f"The license doesn't exists=.", ephemeral=True)
        else:
            ownerId = response_json["owner"]
            productId = response_json["productId"]
            productName = response_json["productName"]
            embed = Embed(title = f"", description= f"License key information", timestamp=datetime.now(), color = discord.Color.green())
            embed.add_field(name="Owner ID", value=f"```{ownerId}```", inline=False)
            embed.add_field(name="Product ID", value=f"```{productId}```", inline=False)
            embed.add_field(name="Product Name", value=f"```{productName}```", inline=False)
            embed.add_field(name="License key", value=f"```{license}```", inline=False)
            embed.set_author(name = "Ducky Licensing")
            return await ctx.reply(embed=embed, ephemeral=True)
async def setup(bot: commands.Bot):
    await bot.add_cog(LicenseCheck(bot))