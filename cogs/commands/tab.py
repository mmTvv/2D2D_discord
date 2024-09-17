import discord
from discord import app_commands
from discord.ext import commands
import random
import asyncio
from utils import *

class TabCog(commands.Cog):
    def __init__(self, bot):
        #self.tab = Tab()
        self.bot = bot

    @app_commands.command(name="tab", description="Get tab data")
    async def tab(self, interaction: discord.Interaction):
        # Деферируем ответ для указания, что работа в процессе
        await interaction.response.defer()

        # Обрабатываем данные и создаем изображение
        header, players, footer = self.tab.get_tab_data()
        header = self.tab.format_text(header)
        footer = self.tab.format_text(footer)
        players = self.tab.format_nick(players)
        self.tab.draw_colored_text(
            header, footer, players, "minecraft.ttf", "fonts/tab.png",
            background_image_path=f'fonts/{random.randint(1,76)}.png'
        )

        # Ждем завершения обработки изображения
        await asyncio.sleep(1.5)

        # Отправляем изображение в followup
        with open("fonts/tab.png", "rb") as f:
            await interaction.followup.send( file=discord.File(f, filename="tab.png"))

async def setup(bot):
    await bot.add_cog(TabCog(bot))
