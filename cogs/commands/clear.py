import discord
from discord import app_commands
from discord.ext import commands

class Clear(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="clear", description="Clear a specific amount of messages from the channel.")
    async def clear(self, interaction: discord.Interaction, amount: int):
        # Проверяем, что пользователь является администратором
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("У вас нет прав администратора для использования этой команды.", ephemeral=True)
            return

        # Делаем отложенный ответ, чтобы избежать ошибки взаимодействия
        await interaction.response.defer(ephemeral=True)

        # Проверяем, что команда вызывается в текстовом канале
        if interaction.channel is None:
            await interaction.followup.send("Эту команду можно использовать только в текстовых каналах!", ephemeral=True)
            return

        # Очищаем сообщения
        deleted = await interaction.channel.purge(limit=amount + 1)
        await interaction.followup.send(f"Удалено {len(deleted) - 1} сообщений.", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(Clear(bot))
