import discord
from discord.ext import commands

class NewsForwarder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.source_channel_id = 123456789012345678  # ID канала me-news
        self.target_channel_ids = [987654321098765432, 876543210987654321]  # ID каналов news-eng и news-ru

    @commands.Cog.listener()
    async def on_message(self, message):
        # Проверяем, что сообщение пришло из канала me-news и не от бота
        if message.channel.id == self.source_channel_id and not message.author.bot:
            for channel_id in self.target_channel_ids:
                target_channel = self.bot.get_channel(channel_id)
                if target_channel:
                    await target_channel.send(f"**{message.author}**: {message.content}")

    @commands.command(name="set_source")
    @commands.has_permissions(administrator=True)
    async def set_source_channel(self, ctx, channel: discord.TextChannel):
        """Установить канал-источник новостей"""
        self.source_channel_id = channel.id
        await ctx.send(f"Канал-источник установлен: {channel.mention}")

    @commands.command(name="add_target")
    @commands.has_permissions(administrator=True)
    async def add_target_channel(self, ctx, channel: discord.TextChannel):
        """Добавить канал, куда будут пересылаться новости"""
        if channel.id not in self.target_channel_ids:
            self.target_channel_ids.append(channel.id)
            await ctx.send(f"Канал {channel.mention} добавлен в список получателей новостей.")
        else:
            await ctx.send(f"Канал {channel.mention} уже в списке.")

    @commands.command(name="remove_target")
    @commands.has_permissions(administrator=True)
    async def remove_target_channel(self, ctx, channel: discord.TextChannel):
        """Удалить канал из списка получателей новостей"""
        if channel.id in self.target_channel_ids:
            self.target_channel_ids.remove(channel.id)
            await ctx.send(f"Канал {channel.mention} удалён из списка получателей новостей.")
        else:
            await ctx.send(f"Канал {channel.mention} не был в списке.")
            
async def setup(bot):
    await bot.add_cog(NewsForwarder(bot))
