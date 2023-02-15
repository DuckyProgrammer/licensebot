import discord
from discord.ext import commands, tasks
from discord.utils import get
from discord import app_commands
from discord import DMChannel, Embed
from typing import Union
import requests
import json
from datetime import datetime

class LicenseCreation(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot
        self.description = "Licensing system"
        self.db = False
    @app_commands.describe(user="Create a license key for a product")
    @commands.hybrid_command(name="createlicense", description="Create a license key for a product")
    async def _createlicense(self, ctx: commands.Context, *, product: commands.clean_content, owner: discord.Member):
        if (ctx.guild.get_role(1075407711333785700) not in ctx.message.author.roles):
            return await ctx.channel.send("No permission.")
        url = f"https://ducky-license.meliniumc.workers.dev/products/{product}"
        querystring = {"type":"name"}
        headers = {"Content-Type": "application/json"}
        one_response = requests.request("GET", url, headers=headers, params=querystring)
        one_response_json = json.loads(one_response.text)
        if not one_response_json["success"]:
            return await ctx.reply(f"The product {product} does not exist.", ephemeral=False)
        else:
            one_product_id = one_response_json["id"]
            url = "https://ducky-license.meliniumc.workers.dev/licenses"
            payload = {
                "productId": f"{one_product_id}",
                "ownerId": f"{owner.id}"
            }
            headers = {
                "Content-Type": "application/json",
                "x-ducky-key": "SuperSpeak3714!"
            }
            response = requests.request("POST", url, json=payload, headers=headers)
            response_json = json.loads(response.text)
            licenseKey = response_json["license"]
            productid = response_json["productId"]
            url = f"https://ducky-license.meliniumc.workers.dev/products/{productid}"
            querystring = {"type":"id"}
            headers = {"Content-Type": "application/json"}
            product_response = requests.request("GET", url, headers=headers, params=querystring)
            product_response_json = json.loads(product_response.text)
            product = product_response_json["name"]
            embed = Embed(title = f"", description= f"You have received a License Key for Ducky Licensing", timestamp=datetime.now(), color = discord.Color.green())
            embed.add_field(name="Product Name", value=f"```{product}```", inline=False)
            embed.add_field(name="License Key", value=f"```{licenseKey}```", inline=False)
            embed.set_author(name = "Ducky Licensing")
            await DMChannel.send(owner, embed=embed)
            return await ctx.reply(f"Created license for {owner.display_name}#{owner.discriminator} ({owner.id})")
async def setup(bot: commands.Bot):
    await bot.add_cog(LicenseCreation(bot))