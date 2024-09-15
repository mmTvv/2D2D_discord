import discord
from discord import app_commands
from discord.ext import commands
from utils import *

class roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @tasks.loop(seconds=20)
    async def check_status(self):
        guild = client.get_guild(GUILD_ID)
        if guild is None:
            print("Сервер не найден. Проверьте GUILD_ID.")
            return

        role = guild.get_role(ROLE_ID)
        if role is None:
            print("Роль не найдена. Проверьте ROLE_ID.")
            return
        for member in guild.members:
            if member.status == discord.Status.offline:
                continue  # Пропускаем пользователей, которые не онлайн
            # Ищем пользовательский статус среди активностей
            custom_status = next((activity for activity in member.activities if isinstance(activity, discord.CustomActivity)), None)

            if custom_status and custom_status.name and "2d2d.org" in custom_status.name:
                if custom_status and custom_status.name and "3b3t.org" not in custom_status.name:
                    if role not in member.roles:
                        await member.add_roles(role)
                        print(f'Роль {role.name} добавлена {member.name}')
            else:
                if role in member.roles:
                    await member.remove_roles(role)
                    print(f'Роль {role.name} удалена у {member.name}')



async def setup(bot):
    await bot.add_cog(roles(bot))
