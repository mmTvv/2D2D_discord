import discord
from discord.ext import commands
from utils import *

class ChannelTracker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        # Убедимся, что это текстовый или голосовой канал
        if isinstance(channel, (discord.TextChannel, discord.VoiceChannel)):
            category_name = "Tickets"  # Имя категории, которую отслеживаем
            category = discord.utils.get(channel.guild.categories, name=category_name)
            
            # Проверяем, что канал относится к нужной категории
            if category and channel.category_id == category.id:
                print(f"Новый канал создан в категории {category_name}: {channel.name}")

                await channel.send(f"Новый канал создан в категории {category_name}: {channel.name}")

async def setup(bot):
    await bot.add_cog(ChannelTracker(bot))
