"""Main HavenBot Script"""

import sys
import os

from config import CONFIG

from discord.ext import commands

initial_extensions = ['channels']

bot = commands.Bot(command_prefix='!', description='Haven Bot')


@bot.event
async def on_command_error(ctx, error):
    """Send the error to Discord chat."""
    await ctx.send(error)


if __name__ == '__main__':
    sys.path.insert(1, os.getcwd() + '/cogs/')
    for extension in initial_extensions:
        bot.load_extension(extension)

    print(CONFIG)
    bot.run(CONFIG['Discord Info']['Token'])
