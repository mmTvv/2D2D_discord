import discord
from discord.ext import commands
from utils import *
from groq import Groq

client = Groq(api_key=config['ai']['groq_token'])

class NewsForwarder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        # Проверяем, что сообщение пришло из канала me-news и не от бота
        if message.channel.id == config['server']['me-news'] and not message.author.bot:
            for channel_id in [config['server']['news-ru'], config['server']['news-en']]:
                target_channel = self.bot.get_channel(channel_id)
                if target_channel.name.replace('news-', '') == 'ru':
                    prompt = f'''без перевода на другой язык, оставляй пост русским,сам пост: "{message.content}"'''
                else:
                    prompt = f'''переведи с ru на язык: {target_channel.name.replace('news-', '')} сам пост: "{message.content}"'''
                if target_channel:
                    completion = client.chat.completions.create(
                            model="llama-3.1-70b-versatile",
                            messages=[
                                {
                                    "role": "system",
                                    "content": "Ты редактор сообщества,не трогай жаргонные выражения, можешь использовать иструменты стилизации Mardown,сообщения в квадратных скобочках оставляй как есть, твоя задача редактировать мои посты переписывая их и при запросе переводить их на другой язык, но нужно сохранять мысль сообщения. При необходимости исправлять ошибки. ВАЖНО ОТПРАВЛЯЙ ТОЛЬКО САМ ПОСТ, БОЛЬШЕ НИЧЕГО НЕ ПИШИ"
                                },
                                {
                                    "role": "user",
                                    "content": prompt
                                }
                            ],
                            temperature=1,
                            max_tokens=1024,
                            top_p=1,
                            stream=False,
                            stop=None,
                        )
                    await target_channel.send(completion.choices[0].message.content)
            
async def setup(bot):
    await bot.add_cog(NewsForwarder(bot))
