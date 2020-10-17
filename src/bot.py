"""Main HavenBot Script"""
import logging
import os
import sys

import logger

from discord.ext import commands

from config import CONFIG

initial_extensions = ['channels', 'messages']
ADMIN_ID = int(CONFIG['Discord Info']['AdminRoleID'])
DISABLED_COMMANDS = CONFIG['Restrictions']['DisabledCommands'].split(',')

bot = commands.Bot(command_prefix='!', description='Haven Bot')


class DisabledCommandError(commands.CommandError):
    """Disabled command was attempted to be called."""

    def __str__(self):
        return 'This command is disabled.'


class AdminError(commands.CommandError):
    """Non-admin tries to use a command."""

    def __str__(self):
        return 'You do not have permission.'


@bot.check
async def globally_restrict_user(ctx):
    username = CONFIG['Restrictions']['Username']
    if username == '' or username == ctx.author.name:
        return True
    else:  # Maybe eventually raise specific error
        return False


@bot.check
async def globally_disabled_commands(ctx):
    if ctx.command.name in DISABLED_COMMANDS:
        raise DisabledCommandError()

    return True


@bot.check
async def globally_check_admin(ctx):
    for r in ctx.message.author.roles[1:]:
        if r.id == ADMIN_ID:
            return True

    raise AdminError()


@bot.event
async def on_command_error(ctx, error):
    logging.error(error)
    await ctx.send(error)


if __name__ == '__main__':
    sys.path.insert(1, os.getcwd() + '/cogs/')
    for extension in initial_extensions:
        bot.load_extension(extension)

    logging.info(f'Starting bot with config: {CONFIG}')
    bot.run(CONFIG['Discord Info']['Token'])
