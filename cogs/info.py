import discord
from discord.ext import tasks, commands
from utils import *
from mcstatus import JavaServer


class info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.info.start()
        self.server = JavaServer.lookup("msk.2d2d.org:25565")

    @tasks.loop(seconds=30)
    async def info(self): #uptime
        online = self.bot.get_channel(config['server']['online_view_channel'])
        members = self.bot.get_channel(config['server']['members_view_channel'])

        status = self.server.status()

        await members.edit(name = f"Members: {len(set(self.bot.get_all_members()))}")
        await online.edit(name = f"Online: {status.players.online}/512")

async def setup(bot):
    await bot.add_cog(info(bot))
