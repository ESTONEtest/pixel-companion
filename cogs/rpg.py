import discord
from discord.ext import commands

from managers.player_manager import player_manager
from managers.rank_manager import rank_manager


class RPG(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.command(name="addhp")
    @commands.has_permissions(administrator=True)
    async def add_hp(
        self,
        ctx,
        member: discord.Member,
        amount: int
    ):


        player = player_manager.get_player(
            member.id
        )


        if not player:

            player_manager.create_player(
                member.id,
                member.name
            )

            player = player_manager.get_player(
                member.id
            )


        # Получаем ранг игрока
        rank = rank_manager.get_rank(
            player["level"]
        )


        # Максимальный HP по рангу
        max_hp = rank_manager.get_max_hp(
            rank
        )


        current_hp = player["hp"]


        new_hp = current_hp + amount


        # Ограничение HP
        if new_hp > max_hp:

            new_hp = max_hp



        # Сохраняем HP
        database = player_manager

        database.add_hp(
            member.id,
            new_hp - current_hp
        )


        await rank_manager.update_rank(
            member
        )


        await ctx.send(
            f"❤️ {member.mention} получил `{amount}` HP!\n"
            f"🏆 Rank: `{rank}`\n"
            f"❤️ HP: `{new_hp}/{max_hp}`"
        )



async def setup(bot):

    print("✅ RPG COG LOADED")

    await bot.add_cog(
        RPG(bot)
    )