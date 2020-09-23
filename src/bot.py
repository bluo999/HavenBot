"""Main HavenBot Script"""

import sys
import os

from functools import wraps

from discord.ext import commands
from dotenv import load_dotenv

initial_extensions = ['cmd']

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix='!', description='Haven Bot')


@bot.event
async def on_command_error(ctx, error):
    """Send the error to Discord chat."""
    await ctx.send(error)


if __name__ == '__main__':
    sys.path.insert(1, os.getcwd() + '/cogs/')
    for extension in initial_extensions:
        bot.load_extension(extension)

    bot.run(TOKEN)
