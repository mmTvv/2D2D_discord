import discord
from discord.enums import AppCommandOptionType
from discord import app_commands
from discord.ext import commands
from utils import *

class tickets_ai(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


async def setup(bot):
    await bot.add_cog(tickets_ai(bot))
