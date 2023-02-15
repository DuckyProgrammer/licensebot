import discord
from discord.ext import commands
import logging

extensions = ["jishaku", "ext.createprod", "ext.createlicense", "ext.removelicense", "ext.getlicense", "ext.getowner"]

LOGGER = logging.getLogger("licensing.core")


intents = discord.Intents.all()
intents.members = True

bot = commands.Bot(command_prefix="=", intents=intents, slash_commands=True, message_commands=True, allowed_mentions=discord.AllowedMentions(everyone=True, users=True, roles=True))

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

class PersistentViewBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents().all()
        super().__init__(command_prefix="=", intents=intents)
    async def setup_hook(self) -> None:
        for extension in extensions:
            try:
                await bot.load_extension(extension)
                LOGGER.info(f"Loaded extension {extension}")

            except:
                LOGGER.exception(f"Failed loading extension {extension}")
        if jsk := bot.get_command("jsk"):
            jsk.hidden = True
bot = PersistentViewBot()
bot.run("MTA3NTQwNzAxOTQ3OTEzODM1Ng.Ged9cP.mqcPd9G6ltmRVIxukZ7mUdrLHABQdShEWj25hM")
