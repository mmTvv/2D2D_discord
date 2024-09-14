import discord
from discord import app_commands
from discord.ext import commands
from utils import *

class tab(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        login()

    @app_commands.command(name="tab", description="get tab data")
    async def util(self, interaction: discord.Interaction):
        try:
            header, players, footer = get_tab_data()

            header = format_text(header)
            footer = format_text(footer)
            players = format_nick(players)

            draw_colored_text(header, footer, players, "minecraft.ttf", "output_image.png", background_image_path="1.png")
        except:
            login()
            header, players, footer = get_tab_data()

            header = format_text(header)
            footer = format_text(footer)
            players = format_nick(players)
            
            draw_colored_text(header, footer, players, "minecraft.ttf", "output_image.png", background_image_path="1.png")

# Регистрация Cog
async def setup(bot):
    await bot.add_cog(tab(bot))
