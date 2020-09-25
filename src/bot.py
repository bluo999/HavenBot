"""Main HavenBot Script"""
import logging
import os
import sys

import logger

from discord.ext import commands

from config import CONFIG

initial_extensions = ['channels', 'messages']

bot = commands.Bot(command_prefix='!', description='Haven Bot')


@bot.event
async def on_command_error(ctx, error):
    """Send the error to Discord chat."""
    logging.error(error)
    await ctx.send(error)


if __name__ == '__main__':
    sys.path.insert(1, os.getcwd() + '/cogs/')
    for extension in initial_extensions:
        bot.load_extension(extension)

    logging.info(f'Starting bot with config: {CONFIG}')
    bot.run(CONFIG['Discord Info']['Token'])
