from functools import wraps

from discord.ext import commands

from config import CONFIG


def restrict_user(func):
    """Decorator function that specifies the command author
    username be equal to the configured name."""

    @wraps(func)
    async def wrapper(*args, **kwargs):
        ctx = args[1]
        assert isinstance(ctx, commands.Context)
        username = CONFIG['User Restrictions']['Username']
        if username == '' or username == ctx.author.name:
            return await func(*args, **kwargs)

    return wrapper
