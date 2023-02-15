from discord.ext import commands, tasks
from discord.utils import get
from discord import app_commands
from typing import Union
import requests
import json

class LicenseDeletion(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot
        self.description = "Licensing system"
        self.db = False
    @app_commands.describe(user="Delete a license from the licensing system")
    @commands.hybrid_command(name="deletelicense", description="Delete a license from the licensing system")
    async def _deletelicense(self, ctx: commands.Context, *, license: commands.clean_content):
        if (ctx.guild.get_role(1075407711333785700) not in ctx.message.author.roles):
            return await ctx.channel.send("No permission.")

        url = f"https://ducky-license.meliniumc.workers.dev/licenses/{license}"
        querystring = {"type":"name"}
        headers = {"Content-Type": "application/json"}
        response = requests.request("GET", url, headers=headers, params=querystring)
        response_json = json.loads(response.text)
        if not response_json["success"]:
            return await ctx.reply(f"The license {license} does not exist.", ephemeral=True)
        else:
            url = f"https://ducky-license.meliniumc.workers.dev/licenses/{license}"
            payload = ""
            headers = {"x-ducky-key": "SuperSpeak3714!"}
            two_response = requests.request("DELETE", url, data=payload, headers=headers)
            two_response_json = json.loads(two_response.text)
            if two_response_json["success"]:
                return await ctx.reply(f"Successfully deleted license {license}.", ephemeral=True)
            else:
                return await ctx.reply(f"An error occurred while deleting the license {license}.", ephemeral=True)
async def setup(bot: commands.Bot):
    await bot.add_cog(LicenseDeletion(bot))