import discord
from discord.enums import AppCommandOptionType
from discord import app_commands
from discord.ext import commands
from utils import *
from groq import Groq


from collections import deque
from prompt import prompt
class main_ai(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.message_queue = deque(maxlen=512)
        self.client = Groq(api_key=config['ai']['groq_token'])

    @commands.Cog.listener()
    async def on_ready(self):
        for channel_id in [config['server']['main'], config['server']['server-chat']]:
            channel = self.bot.get_channel(channel_id)
            if channel:
                async for message in channel.history(limit=512):
                    self.message_queue.append(message)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        self.message_queue.append(message.content)
        if message.channel.id == config['server']['main'] and self.bot.user in message.mentions:
            result = completion = self.client.chat.completions.create(
                model="llama-3.1-70b-versatile",
                messages=[
                    {"role": "system",
                    "content": prompt}
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