"""Channels cog (general channel management)"""

import logging

from discord import utils
from discord.ext.commands import Cog, command, has_role


def setup(bot):
    """Load the Channel cog"""
    bot.add_cog(ChannelCog(bot))


class ChannelCog(Cog, name='Channel'):
    """Cog for general channel magement"""

    def __init__(self, bot):
        self.bot = bot

    @command(name='create-text')
    async def create_channel(self, ctx, channel_name):
        """Create a new text channel"""
        await ctx.guild.create_text_channel(channel_name)
        await ctx.send(f'Created text channel {channel_name}')

    @command(name='create-voice')
    async def create_voice_channel(self, ctx, channel_name):
        """Create a new voice channel"""
        await ctx.guild.create_voice_channel(channel_name)
        await ctx.send(f'Created voice channel {channel_name}')

    @command(name='rename-channel')
    async def rename_channel(self, ctx, channel_name, new_channel_name):
        """Rename a text or voice channel"""
        channel = utils.get(ctx.guild.channels, name=channel_name)
        if channel is not None:
            await channel.edit(name=new_channel_name)
            await ctx.send(f'Renamed channel {channel_name} to {new_channel_name}')
        else:
            await ctx.send(f'Channel {channel_name} does not exist')

    @command(name='delete-channel')
    async def delete_channel(self, ctx, channel_name):
        """Delete a text or voice channel"""
        channel = utils.get(ctx.guild.channels, name=channel_name)
        if channel is not None:
            await channel.delete()
            await ctx.send(f'Deleted channel {channel_name}')
        else:
            await ctx.send(f'Channel {channel_name} does not exist')
