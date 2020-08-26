import os

import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')
    else:
        print(error)

@bot.command(name='create-channel')
@commands.has_role('admin')
async def create_channel(ctx, channel_name):
    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels, name=channel_name)
    if not existing_channel:
        print(f'Creating new channel: {channel_name}')
        await guild.create_text_channel(channel_name)


bot.run(TOKEN)
