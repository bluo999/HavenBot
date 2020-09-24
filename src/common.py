import sys

from functools import wraps

from discord.ext import commands


def restrict_channel(func):
    """Decorator function that specifies the command author username 
    be equal to the sys.argv[1]."""

    @wraps(func)
    async def wrapper(*args, **kwargs):
        ctx = args[1]
        assert isinstance(ctx, commands.Context)
        if len(sys.argv) == 1 or sys.argv[1] == ctx.author.name:
            return await func(*args, **kwargs)

    return wrapper
