"""Commands cog (general channel management)"""

from discord import utils
from discord.ext.commands import Cog, command, has_role

from bot import restrict_channel


def setup(bot):
    """Load the Command cog."""
    bot.add_cog(CommandCog(bot))


class CommandCog(Cog, name='Command'):
    """Cog for basic commands."""

    def __init__(self, bot):
        self.bot = bot

    @command(name='create')
    @has_role('ADMIN')
    @restrict_channel
    async def create_channel(self, ctx, channel_name):
        """Create a new text channel."""
        print(f'Creating new channel: {channel_name}')
        await ctx.guild.create_text_channel(channel_name)
        await ctx.send(f'Created text channel {channel_name}')

    @command(name='create-voice')
    @has_role('ADMIN')
    async def create_voice_channel(self, ctx, channel_name):
        """Create a new voice channel."""
        print(f'Creating new voice channel {channel_name}')
        await ctx.guild.create_voice_channel(channel_name)
        await ctx.send(f'Created voice channel {channel_name}')

    @command(name='rename')
    @has_role('ADMIN')
    async def rename_channel(self, ctx, channel_name, new_channel_name):
        """Rename a text or voice channel."""
        channel = utils.get(ctx.guild.channels, name=channel_name)
        if channel is not None:
            await channel.edit(name=new_channel_name)
            await ctx.send(f'Renamed channel {channel_name} to {new_channel_name}')
        else:
            await ctx.send(f'Channel {channel_name} does not exist')
