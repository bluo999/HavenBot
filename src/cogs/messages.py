"""Messages cog (logs new messages, edits, and deletes)"""

import logging

from discord import AuditLogAction
from discord.ext.commands import Cog


def setup(bot):
    """Load the message cog"""
    bot.add_cog(MessageCog(bot))


class MessageCog(Cog, name='Message'):
    """Cog to log new messages, edits, and deletes"""

    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_message(self, message):
        logging.info(
            f'Message ({message.author.name} in {message.channel.name}): '
            f'"{message.content}"'
        )

    @Cog.listener()
    async def on_message_delete(self, message):
        logging.info(
            f'Deleted ({message.author.name} in {message.channel.name}): '
            f'"{message.content}"'
        )

    @Cog.listener()
    async def on_message_edit(self, before_message, after_message):
        logging.info(
            f'Edited ({before_message.author.name} in {before_message.channel.name}): '
            f'"{before_message.content}" > "{after_message.content}"'
        )
