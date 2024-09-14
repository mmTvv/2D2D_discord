import discord
from discord.ext import commands
import os

# Инициализация бота с использованием слэш-команд
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

# Событие при готовности бота
async def load_cogs():
    for root, dirs, files in os.walk('./cogs'):
        for file in files:
            if file.endswith('.py'):
                cog_path = os.path.join(root, file)
                cog_module = cog_path.replace('./', '').replace('/', '.').replace('\\', '.').replace('.py', '')
                try:
                    await bot.load_extension(cog_module)
                    print(f"Loaded {cog_module}")
                except Exception as e:
                    print(f"Failed to load {cog_module}: {e}")

@bot.event
async def on_ready():
    print(f'Bot {bot.user} is ready!')

# Синхронизация слэш-команд
@bot.event
async def on_connect():
    await bot.tree.sync()
    print("Slash commands synced.")

# Запуск загрузки cogs при старте бота
@bot.event
async def on_ready():
    await load_cogs()


bot.run('MTI3NzQ0MzczODMxNDA4NDQ1Ng.G8ieaI.VevEyQ-5HGeSIsPCOhmVzotnCXe_i5dqPKMmPo')
