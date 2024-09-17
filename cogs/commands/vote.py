import discord
from discord.ext import commands
from discord import app_commands
from utils import *

class Vote(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active_votes = {}  # Словарь для хранения активных голосований

    @app_commands.command(name="vote")
    async def start_vote(self, interaction: discord.Interaction, *, question: str):
        """Команда для начала голосования"""
        if interaction.channel.id in self.active_votes:
            await interaction.channel.send("Голосование уже активно в этом канале!")
            return

        options = ["👍", "👎"]  # Используем реакции 👍 и 👎 для голосования
        embed = discord.Embed(title="Голосование", description=question, color=0x00ff00)
        embed.add_field(name="👍", value="За", inline=True)
        embed.add_field(name="👎", value="Против", inline=True)
        embed.set_footer(text="Голосуйте, реагируя на сообщение ниже!")
        
        message = await interaction.channel.send(embed=embed)

        for option in options:
            await message.add_reaction(option)

        # Сохраняем информацию о голосовании
        self.active_votes[interaction.channel.id] = {
            "message_id": message.id,
            "question": question,
            "reactions": {option: 0 for option in options}
        }
        print(self.active_votes)

    @app_commands.command(name="result")
    async def vote_result(self, interaction: discord.Interaction):
        """Команда для показа результатов голосования"""
        if interaction.channel.id not in self.active_votes:
            print(self.active_votes)
            await interaction.channel.send("Нет активного голосования в этом канале!")
            return

        vote_data = self.active_votes[interaction.channel.id]
        message = await interaction.channel.fetch_message(vote_data["message_id"])

        for reaction in message.reactions:
            if str(reaction.emoji) in vote_data["reactions"]:
                vote_data["reactions"][str(reaction.emoji)] = reaction.count - 1  # -1 чтобы убрать голос бота

        # Выводим результаты голосования
        result_embed = discord.Embed(
            title=f"Результаты голосования: {vote_data['question']}",
            color=0x00ff00
        )
        for emoji, count in vote_data["reactions"].items():
            result_embed.add_field(name=emoji, value=f"Голосов: {count}", inline=True)

        await interaction.channel.send(embed=result_embed)

        # Удаляем голосование
        del self.active_votes[interaction.channel.id]

async def setup(bot):
    await bot.add_cog(Vote(bot))
