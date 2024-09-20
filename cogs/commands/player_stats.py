import discord
from discord.ext import commands
from discord import app_commands
import requests
import json
import traceback

def get_player_stats(stats):
    return {
        'playtime': stats.get('stats', {}).get('stats', {}).get('minecraft:custom', {}).get('minecraft:play_time', 0) // 20 // 60 //60,  # минуты
        'kills': stats.get('stats', {}).get('stats', {}).get('minecraft:custom', {}).get('minecraft:player_kills', 0),
        'deaths': stats.get('stats', {}).get('stats', {}).get('minecraft:custom', {}).get('minecraft:deaths', 0),
        'blocks_placed': stats.get('stats', {}).get('stats', {}).get('minecraft:custom', {}).get('minecraft:blocks_placed', 0),
        'blocks_mined': stats.get('stats', {}).get('stats', {}).get('minecraft:custom', {}).get('minecraft:blocks_mined', 0),
        'obsidian_placed': stats.get('stats', {}).get('stats', {}).get('minecraft:used', {}).get('minecraft:obsidian', 0),
        'enderchests_placed': stats.get('stats', {}).get('stats', {}).get('minecraft:used', {}).get('minecraft:ender_chest', 0),
        'carpets_placed': stats.get('stats', {}).get('stats', {}).get('minecraft:used', {}).get('minecraft:carpet', 0),
        'crystals_used': stats.get('stats', {}).get('stats', {}).get('minecraft:used', {}).get('minecraft:end_crystal', 0),
        'totems_used': stats.get('stats', {}).get('stats', {}).get('minecraft:used', {}).get('minecraft:totem_of_undying', 0),
        'exp_bottles_used': stats.get('stats', {}).get('stats', {}).get('minecraft:used', {}).get('minecraft:experience_bottle', 0),
    }

class PlayerStatsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='playerstats')
    async def player_stats(self, interaction: discord.Interaction, username: str):
        try:
            clock_2d = discord.utils.get(interaction.guild.emojis, name="clock_2d")
            sword = discord.utils.get(interaction.guild.emojis, name="sword")
            pickaxe = discord.utils.get(interaction.guild.emojis, name="pickaxe")
            xp = discord.utils.get(interaction.guild.emojis, name="xp")
            crystal = discord.utils.get(interaction.guild.emojis, name="crystal")
            bone = discord.utils.get(interaction.guild.emojis, name="bone")
            box = discord.utils.get(interaction.guild.emojis, name="box")
            heart = discord.utils.get(interaction.guild.emojis, name="heart")
            totem = discord.utils.get(interaction.guild.emojis, name="totem")
            dirt = discord.utils.get(interaction.guild.emojis, name="dirt")
            d2d = discord.utils.get(interaction.guild.emojis, name="2d2d")
            player = requests.get(f'http://93.80.111.146:9090/api/stats/player/{username}').content.decode('utf-8')

            if player['error'] != 'None':
                player = json.loads(player)
                uuid = player["uuid"]
                login_date = player["logindate"]
                reg_date = player["regdate"]
                avatar_url = f"https://crafthead.net/avatar/{username}"

                player_stats = get_player_stats(player)
                if player_stats:
                    stats_text = (
                        f"{clock_2d} **Playtime** — {player_stats['playtime']} часов\n"
                        f"{sword} **Kills** — {player_stats['kills']}\n"
                        f"{bone} **Deaths** — {player_stats['deaths']}\n"
                        f"{dirt} **Total Blocks Placed** — {player_stats['blocks_placed']}\n"
                        f"{pickaxe} **Total Blocks Mined** — {player_stats['blocks_mined']}\n"
                        f"{dirt} bsidian Placed** — {player_stats['obsidian_placed']}\n"
                        f"{dirt} Enderchests Placed — {player_stats['enderchests_placed']}\n"
                        f"{crystal} Crystals Used — {player_stats['crystals_used']}\n"
                        f"{totem} Totems Used — {player_stats['totems_used']}\n"
                        f"{xp} EXP Bottles Used — {player_stats['exp_bottles_used']}\n"
                        f"🧶 Carpets Placed — {player_stats['carpets_placed']}\n"
                    )
                else:
                    stats_text = "Статистика игры не найдена."

                embed = discord.Embed(title=f"{username} stats", color=discord.Color.purple())
                embed.add_field(name="Last Join", value=f"<t:{round(int(login_date)/1000)}:f> - <t:{round(int(login_date)/1000)}:R>", inline=False)
                embed.add_field(name="First Join", value=f"<t:{round(int(reg_date)/1000)}:f> - <t:{round(int(reg_date)/1000)}:R>", inline=False)
                embed.add_field(name="Stats", value=stats_text, inline=False)
                embed.set_thumbnail(url=avatar_url)

                await interaction.response.send_message(embed=embed)
            else:
                await interaction.response.send_message(f"**Player `{username}` not found.**")

        except json.JSONDecodeError:
            await interaction.response.send_message("Error reading api.")
        except Exception as e:
            error_details = traceback.format_exc()
            await interaction.response.send_message(f"Error: {str(e)}\n{error_details}")

async def setup(bot):
    await bot.add_cog(PlayerStatsCog(bot))
