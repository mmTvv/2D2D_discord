import discord
from discord.ext import tasks, commands
from utils import *

class roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.check_status.start()

    @tasks.loop(seconds=20)
    async def check_status(self):
        guild = self.bot.get_guild(config['server']['guild_id'])
        if guild is None:
            print("Сервер не найден. Проверьте GUILD_ID.")
            return

        role = guild.get_role(config['roles']['adept_role_id'])
        if role is None:
            print("Роль не найдена. Проверьте ROLE_ID.")
            return
        for member in guild.members:
            custom_status = next((activity for activity in member.activities if isinstance(activity, discord.CustomActivity)), None)

            if custom_status and custom_status.name and "2d2d.org" in custom_status.name:
                if custom_status and custom_status.name and "3b3t.org" not in custom_status.name:
                    if role not in member.roles:
                        await member.add_roles(role)
            else:
                if role in member.roles:
                    await member.remove_roles(role)

async def setup(bot):
    await bot.add_cog(roles(bot))
