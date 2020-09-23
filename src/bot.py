"""Main HavenBot script"""

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


def restrict_channel(func):
    """Decorator function that specifies the channel name must
    be equal to the username of the command author."""

    @wraps(func)
    async def wrapper(*args, **kwargs):
        ctx = args[1]
        assert isinstance(ctx, commands.Context)
        if ctx.channel.name == ctx.author.name:
            return await func(*args, **kwargs)

    return wrapper


@bot.event
async def on_command_error(ctx, error):
    """Send the error to Discord chat."""
    await ctx.send(error)


if __name__ == '__main__':
    sys.path.insert(1, os.getcwd() + '/cogs/')
    for extension in initial_extensions:
        bot.load_extension(extension)

    bot.run(TOKEN)
