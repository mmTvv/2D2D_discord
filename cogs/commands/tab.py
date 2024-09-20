import discord
from discord import app_commands
from discord.ext import commands
import random
import asyncio
from utils import Tab

class TabCog(commands.Cog):
    def __init__(self, bot):
        #self.tab = Tab()
        self.bot = bot

    @app_commands.command(name="tab", description="Get tab data")
    async def tab(self, interaction: discord.Interaction):
        # Отправляем первоначальное сообщение и сохраняем объект сообщения
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

        with open('fonts/tab.png', 'rb') as f:
            picture = discord.File(f)

        # Редактируем первоначальное сообщение и добавляем фото
        await interaction.followup.send( file=picture)

async def setup(bot):
    await bot.add_cog(TabCog(bot))
