import discord
from discord.ext import tasks, commands
from utils import *
from requests import get

class roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.check_status.start()
        self.check_role_task.start()

    @tasks.loop(minutes=5)
    async def check_role_task(self):
        try:
            data = json.loads(get('http://93.80.111.146:9090/api/discord/id/').content.decode('utf-8'))
        except:
            print('error get ids')
        guild = self.bot.get_guild(config['server']['guild_id'])  # ID сервера (гильдии)
        if guild is None:
            print("Сервер не найден.")
            return

        # Задайте ID пользователей и ID роли для проверки
        user_ids = data['ds_ids']  # Список ID пользователей
        role_id = config['roles']['verify_role_id']  # ID роли

        # Ищем роль по её ID
        role = guild.get_role(role_id)
        if role is None:
            print(f"Роль с ID '{role_id}' не найдена на сервере.")
            return

        for user_id in user_ids:
            member = guild.get_member(user_id)
            if member is None:
                continue

            # Проверяем, есть ли у пользователя эта роль
            if role not in member.roles:
                try:
                    await member.add_roles(role)
                except discord.Forbidden:
                    pass
                except discord.HTTPException:
                    pass
            else:
                pass


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
