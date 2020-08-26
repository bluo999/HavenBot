import functools
import os

import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix='!')

def restrict_channel(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        ctx = args[0]
        if ctx.channel.name == ctx.author.name:
            return await func(*args, **kwargs)
    return wrapper


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command')
    else:
        print(error)


@bot.command(name='create')
@commands.has_role('ADMIN')
@restrict_channel
async def create_channel(ctx, channel_name):
    print(f'Creating new channel: {channel_name}')
    await ctx.guild.create_text_channel(channel_name)
    await ctx.send(f'Created text channel {channel_name}')


@bot.command(name='create-voice')
@commands.has_role('ADMIN')
@restrict_channel
async def create_voice_channel(ctx, channel_name):
    print(f'Creating new voice channel: {channel_name}')
    await ctx.guild.create_voice_channel(channel_name)
    await ctx.send(f'Created voice channel {channel_name}')
    

@bot.command(name='rename')
@commands.has_role('ADMIN')
@restrict_channel
async def rename_channel(ctx, channel_name, new_channel_name):
    guild = ctx.guild
    channel = discord.utils.get(guild.channels, name=channel_name)
    if channel is not None:
        await channel.edit(name=new_channel_name)
        await ctx.send(f'Renamed channel {channel_name} to {new_channel_name}')
    else:
        await ctx.send(f'Channel {channel_name} does not exist')


bot.run(TOKEN)
