"""
===========================================
Pixel Companion RPG v2.0
Events Cog
===========================================
"""

import discord
from discord.ext import commands

from managers.player_manager import player_manager
from managers.rank_manager import rank_manager


class Events(commands.Cog):

    def __init__(self, bot):

        self.bot = bot



    @commands.Cog.listener()
    async def on_member_join(self, member):

        # создаём игрока при входе

        player_manager.create_player(
            member.id,
            member.name
        )


        # выдаём стартовую роль

        await rank_manager.update_rank(
            member
        )



async def setup(bot):

    await bot.add_cog(
        Events(bot)
    )