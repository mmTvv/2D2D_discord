import discord
from discord.ext import commands
import requests
import json
from discord import app_commands

class StatsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='stats')
    async def server_stat(self, interaction: discord.Interaction):
        try:
            data = json.loads(requests.get('http://93.80.111.146:9090//api/stats/server').content.decode('utf-8'))

            embed = discord.Embed(title="Server stats",
                                  colour=discord.Color.purple())

            embed.add_field(name=f"Online: {len(data['list'])}",
                            value="```" +", ".join(data['list'])+"```",
                            inline=False)
            embed.add_field(name="TPS",
                            value=f"*Lowest Region TPS:  {data['low_tps']}\n*Median Region TPS:  {data['medium_tps']}\nHighest Region TPS:  {data['high_tps']}*",
                            inline=False)
            embed.add_field(name="Online stats",
                            value=f"*Player per day: {data['top_days']}\nPlayer per month: {data['top_months']}\nTotal players: {data['total_players']}*",
                            inline=False)
            embed.add_field(name="Server start time:",
                            value=f"<t:{data['start']}:f>",
                            inline=False)

            embed.set_thumbnail(url="https://cdn.discordapp.com/icons/1160613896286130287/8311e2b0d7d2edb5d3137826456f23c9.webp")

            embed.set_footer(text=f"Server size: {round(data['size'], 2)} GB")

            await interaction.response.send_message(embed=embed)
        except Exception as e:
            await interaction.response.send_message(f'Eroor: {str(e)}')

async def setup(bot):
    await bot.add_cog(StatsCog(bot))
