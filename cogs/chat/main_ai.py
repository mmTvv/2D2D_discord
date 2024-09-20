import discord
from discord.enums import AppCommandOptionType
from discord import app_commands
from discord.ext import commands, tasks
from utils import *
from groq import Groq

from prompt import main_prompt
class main_ai(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.message_queue = []
        self.client = Groq(api_key=config['ai']['groq_token'])

    async def get_msg(self):
        channel = self.bot.get_channel(config['server']['main'])
        if channel:
            async for message in channel.history(limit=64):
                self.message_queue.append(f"{message.created_at.strftime('%Y-%m-%d %H:%M:%S %Z%z')} [{str(message.author).replace('[2D2D.ORG]#4833', 'AI(YOU)')}]: {message.content}")
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        
        if message.channel.id == config['server']['main'] and self.bot.user in message.mentions:
            await self.get_msg()
            result = completion = self.client.chat.completions.create(
                model="llama-3.1-70b-versatile",
                messages=[
                    {
                        "role": "system",
                        "content": f"{main_prompt}"
                    },
                    {
                        "role": "user",
                        "content": f"{message.created_at.strftime('%Y-%m-%d %H:%M:%S %Z%z')} [{message.author}]: {message.content}+\n\nИстория чата: {self.message_queue}"
                    }
                    ],
                    temperature=1.0,
                    max_tokens=256,
                    top_p=0.5,
                    stream=False,
                    stop=None,
                    )
            await message.reply(result.choices[0].message.content.replace('everyone', 'пошел нахуй').replace('here', 'тоже нахуй'))

async def setup(bot):
    await bot.add_cog(main_ai(bot))