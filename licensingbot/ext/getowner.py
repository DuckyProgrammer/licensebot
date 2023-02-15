from discord.ext import commands, tasks
from discord.utils import get
from discord import app_commands, Embed
from typing import Union
import requests
import json
from datetime import datetime
import discord

class OwnerCheck(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot
        self.description = "Licensing system"
        self.db = False
    @app_commands.describe(user="Gets the information of a license")
    @commands.hybrid_command(name="getowner", description="Gets the information of a license")
    async def _getowner(self, ctx: commands.Context, ownerId: commands.clean_content):
        if (ctx.guild.get_role(1075407711333785700) not in ctx.message.author.roles):
            return await ctx.reply("No permission.")
        
        url = f"https://ducky-license.meliniumc.workers.dev/licenses/{ownerId}?type=ownerId"
        payload = ""
        headers = {
                        "Content-Type": "application/json",
                        "x-ducky-key": "SuperSpeak3714!"
                    }
        response = requests.request("GET", url, data=payload, headers=headers)
        response_json = json.loads(response.text)
        if response_json["success"]:
            licenses = str(response_json["licenses"]).replace("[", "").replace("]", "").replace("'", "").replace(", ", "\n")
            ownerIdres = response_json["ownerId"]
            embed = Embed(title = f"", description= f"User information", timestamp=datetime.now(), color = discord.Color.green())
            embed.add_field(name="Owner ID", value=f"```{ownerIdres}```", inline=False)
            embed.add_field(name="License keys", value=f"```{licenses}```", inline=False)
            embed.set_author(name = "Ducky Licensing")
            return await ctx.reply(embed=embed, ephemeral=True)
        else:
            return await ctx.reply(f"An error occurred.", ephemeral=True)
        

async def setup(bot: commands.Bot):
    await bot.add_cog(OwnerCheck(bot))