import discord
from discord.ext import commands
from discord import app_commands
from gradio_client import Client

from utils import *

class Image(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.client = Client("KingNish/Realtime-FLUX")

    @app_commands.command(name="gen_image", description="Create your image")
    async def img_gen(self, interaction: discord.Interaction, img_prompt: str):
        await interaction.response.defer()
        result = self.client.predict(
                prompt=img_prompt,
                seed=42,
                width=1024,
                height=1024,
                api_name="/generate_image"
        )
        with open(result[0], 'rb') as f:
            picture = discord.File(f)

        # Отправляем изображение
        await interaction.followup.send(content=f'***prompt***: {img_prompt.replace("@", "")}', file=picture)
            
async def setup(bot):
    await bot.add_cog(Image(bot))
