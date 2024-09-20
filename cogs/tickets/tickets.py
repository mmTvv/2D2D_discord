import discord
from discord.enums import AppCommandOptionType
from discord import app_commands
from discord.ext import commands, tasks
from utils import *
from discord.ui import Button, View, Select


class CloseTicketButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="Close Ticket", style=discord.ButtonStyle.red)

    async def callback(self, interaction: discord.Interaction):
        channel = interaction.channel
        # Проверка, является ли канал тикетом
        if "ticket" in channel.name:
            await channel.delete(reason="Тикет закрыт")
        else:
            await interaction.response.send_message("Это не тикет-канал.", ephemeral=True)


class TicketSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label='Bug', description='found a bug', emoji='🐛'),
            discord.SelectOption(label='Improvement', description='Suggestion for Improvement server', emoji='🔧'),
            discord.SelectOption(label='Other', description='Any other questions', emoji='❓')
        ]
        super().__init__(placeholder="Select a ticket category", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        category = self.values[0]
        channel_name = f"ticket-{category.replace(' ', '-').lower()}-{interaction.user.name}"
        
        existing_channel = discord.utils.get(interaction.guild.channels, name=channel_name)
        if existing_channel:
            await interaction.response.send_message(f"You already have an open ticket: {existing_channel.mention}, close it first to create a new one", ephemeral=True)
            return

        ticket_category = discord.utils.get(interaction.guild.categories, name="Tickets")
        if not ticket_category:
            ticket_category = await interaction.guild.create_category("Tickets")

        ticket_channel = await interaction.guild.create_text_channel(
            channel_name,
            category=ticket_category,
            topic=f"Ticket from {interaction.user.display_name} ({category})",
        )

        await ticket_channel.set_permissions(interaction.user, read_messages=True, send_messages=True)
        

        embed = discord.Embed(
                title="Your ticket",
                description="Сlick on the button below to create a ticket.",
                color=discord.Color.blue()
            )
        button = CloseTicketButton()
        view = View(timeout=None)
        view.add_item(button)
        
        await ticket_channel.send(embed=embed, view=view)
        await interaction.response.send_message(f"The ticket has been created: {ticket_channel.mention}", ephemeral=True)

class TicketButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="Create a Ticket", style=discord.ButtonStyle.primary)

    async def callback(self, interaction: discord.Interaction):
        select = TicketSelect()
        view = View(timeout=None)
        view.add_item(select)
        
        await interaction.response.send_message("Select a category for the ticket:", view=view, ephemeral=True)

class Ticket(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.on_ready.start()

    @tasks.loop(minutes=60)
    async def on_ready(self):
        """Этот метод вызывается при запуске бота"""
        # Получаем канал, в котором будет отображаться кнопка для тикетов
        channel = self.bot.get_channel(config['server']['tickets'])
        if channel:
            embed = discord.Embed(
                title="Ticket System",
                description="Сlick on the button below to create a ticket.",
                color=discord.Color.blue()
            )
            button = TicketButton()
            view = View(timeout=None)
            view.add_item(button)

            # Очищаем предыдущие сообщения в канале (если нужно)
            await channel.purge(limit=10)
            
            # Отправляем сообщение с эмбедом и кнопкой
            await channel.send(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(Ticket(bot))