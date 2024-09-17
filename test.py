import discord
from discord.ext import commands
from discord import app_commands, Locale
from utils import *
# Словарь локализаций
localizations = {
    "en-US": {
        "command_hello": "Hello!",
        "command_hello_description": "Says hello to the user."
    },
    "ru": {
        "command_hello": "Привет!",
        "command_hello_description": "Приветствует пользователя."
    }
}

class MyBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def setup_hook(self):
        # Синхронизация команд с гильдией или глобально
        await self.tree.sync()

# Задаем intents, чтобы бот мог правильно взаимодействовать с событиями
intents = discord.Intents.default()
intents.message_content = True  # Включаем необходимые intents

bot = MyBot(command_prefix="!", intents=intents)

# Локализованная команда
@bot.tree.command(name="hello", description=app_commands.locale_str("command_hello_description", default="Says hello"))
async def hello(interaction: discord.Interaction):
    # Получаем локаль пользователя
    locale = interaction.locale.value
    # Получаем локализованное сообщение
    localized_message = localizations.get(locale, localizations["en-US"])["command_hello"]
    await interaction.response.send_message(localized_message)

bot.run(config['bot']['token'])
