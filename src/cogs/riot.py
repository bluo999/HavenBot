"""Riot cogs (using riot API)"""

import logging

import sqlite3

from discord import utils
from discord.ext.commands import Cog, command
from riotwatcher import LolWatcher, ApiError

from common import restrict_user
from config import CONFIG

# Init database, riot API
REGION = CONFIG['Riot']['Region']

conn = sqlite3.connect(CONFIG['Database']['File'])
watcher = LolWatcher(CONFIG['Riot']['APIKey'])
current_champ_list = watcher.data_dragon.champions(
    watcher.data_dragon.versions_for_region(REGION)['n']['champion']
)


def setup(bot):
    """Load the Riot cog."""
    bot.add_cog(RiotCog(bot))


class RiotCog(Cog, name='Riot'):
    """Cog for Riot API."""

    def __init__(self, bot):
        self.bot = bot

    @command(name='set-username')
    async def set_username(self, ctx, username):
        """Associate Riot username with Discord user."""
        author_id = ctx.message.author.id
        sql = """
            SELECT riot_username
            FROM riot
            WHERE discord_id = ?
        """
        cursor = conn.cursor()
        cursor.execute(sql, (author_id,))
        row = cursor.fetchone()

        if row is None:
            # Insert new entry
            sql = """
                INSERT INTO
                    riot (riot_username, discord_id)
                VALUES
                    (?, ?)
            """
            cursor.execute(sql, (username, author_id))
        else:
            # Update existing entry
            sql = """
                UPDATE riot
                SET
                    riot_username = ?,
                    riot_id = ?
                WHERE discord_id = ?
            """
            cursor.execute(sql, (username, None, author_id))
        conn.commit()

        await ctx.send(f'Set {ctx.message.author}\'s Riot username to {username}')

    @command(name='lookup')
    async def lookup(self, ctx, riot_username=None):
        """
        Lookup Riot username. If not specified, lookup the username set by the
        discord user in the database.
        """
        cursor = conn.cursor()

        if riot_username is None:  # Retrieve riot info from discord id
            author_id = ctx.message.author.id
            sql = """
                SELECT riot_username, riot_id
                FROM riot
                WHERE discord_id = ?
            """
            cursor.execute(sql, (author_id,))
            row = cursor.fetchone()

            if row is None:
                await ctx.send(f'Set username first with !set-username')
                return

            riot_username, riot_id = row

        # Either username is specified or riot id hasn't been generated yet
        if riot_username is not None or riot_id is None:
            try:
                user_info = watcher.summoner.by_name(REGION, riot_username)
                riot_id = user_info['id']
            except ApiError as err:
                if err.response.status_code == 404:
                    await ctx.send(f'Summoner {riot_username} does not exist')
                    return
                else:
                    raise

            sql = """
                UPDATE riot
                SET riot_id = ?
                WHERE riot_username = ?
            """
            cursor.execute(sql, (riot_id, riot_username))
            conn.commit()

        try:
            live_info = watcher.spectator.by_summoner(REGION, riot_id)
        except ApiError as error:
            if error.response.status_code == 404:
                await ctx.send(f'{riot_username} is not in a live game')
                return
            else:
                raise

        game_mode = live_info['gameMode']
        summoner = next(i for i in live_info['participants'] if i['summonerId'] == riot_id)
        champion = next(
            v
            for v in current_champ_list['data'].values()
            if v['key'] == str(summoner['championId'])
        )
        champion_name = champion['id']

        await ctx.send(f'{riot_username} is playing {game_mode} as {champion_name}')
