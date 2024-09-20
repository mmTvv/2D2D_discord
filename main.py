import discord
from discord.ext import commands
import os
from utils import *

# Инициализация бота
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=config['bot']['prefix'], intents=intents)

# Функция для рекурсивной загрузки cogs из файлов и папок
async def load_cogs():
    for root, dirs, files in os.walk('./cogs'):
        for file in files:
            if file.endswith('.py'):
                cog_path = os.path.join(root, file)
                cog_module = cog_path.replace('./', '').replace('/', '.').replace('\\', '.').replace('.py', '')
                await bot.load_extension(cog_module)
                print(f"Loaded {cog_module}")
                

# Событие при готовности бота
@bot.event
async def on_ready():
    print(f"Бот {bot.user} запущен и готов!")  # Простой вывод для проверки
    print(f"Подключен к {len(bot.guilds)} серверам.")  # Вывод количества серверов
    print(f"Подключен как {bot.user.name}")  # Имя пользователя бота
    await load_cogs()

    # Синхронизируем слэш-команды с Discord API
    try:
        await bot.tree.sync()
        print("Slash commands synced.")
    except Exception as e:
        print(f"Failed to sync slash commands: {e}")

# Токен бота
bot.run(config['bot']['token'])
