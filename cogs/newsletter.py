import discord
from discord.ext import tasks, commands
from utils import *
from requests import get
from datetime import datetime

class newsletter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.verify_news.start()

    @tasks.loop(hours=24)  # Проверяем раз в день
    async def verify_news(self):
        today = datetime.utcnow().date()

        # Проверяем, если это первый день месяца
        if today.day == 31:
            try:
                data = json.loads(get('http://93.80.111.146:9090/api/discord/id/').content.decode('utf-8'))
            except:
                print('error get ids')
            guild = self.bot.get_guild(config['server']['guild_id'])  # Замените на ID вашего сервера
            if guild:
                for member in guild.members:  # Перебираем всех участников сервера
                    if member not in data['ds_ids']:  # Проверяем, что участник не администратор
                        if member.bot:  # Исключаем ботов
                            continue
                        try:
                            await member.send("""***ТЕБЯ МОГУТ ВЗЛОМАТЬ***
Привет, это `2d2d.org` ,мы пишем тебе не просто так. Ежемесячно на сервере взламывают больше 100 аккаунтов из за легких паролей.
Есть способ защиты ,который к тому же даст крутую роль!
Напиши мне прямо сейчас `!account link <твой ник> <твой пароль>`, вот пример `!account link GGuPP 123123`

Так ты защитишь свой аккуант от взлома и получишь полный контроль наш доступом к серверу с твоего аккаунта!
Спасибо, что вы с нами :purple_heart: """)
                        except discord.Forbidden:
                            print(f"Не удалось отправить сообщение {member.name}, возможно ЛС закрыты.")
                        except AttributeError:
                            print(f"Ошибка с пользователем {member.name}: невозможность создать ЛС.")

async def setup(bot):
    await bot.add_cog(newsletter(bot))
