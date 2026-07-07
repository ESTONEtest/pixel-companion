import discord
from discord.ext import commands

from managers.player_manager import player_manager
from managers.role_manager import role_manager, LEVEL_ROLES
from utils.logger import logger



class TestLevel(commands.Cog):


    def __init__(
        self,
        bot
    ):

        self.bot = bot



    @commands.command(
        name="leveltest"
    )
    @commands.has_permissions(
        administrator=True
    )
    async def leveltest(
        self,
        ctx,
        level: int
    ):


        user_id = ctx.author.id


        # ==========================================
        # CREATE PLAYER IF NOT EXISTS
        # ==========================================

        player = player_manager.get_player(
            user_id
        )


        if not player:

            player_manager.create_player(
                user_id,
                ctx.author.name
            )



        # ==========================================
        # SET LEVEL
        # ==========================================

        player_manager.set_level(
            user_id,
            level
        )



        member = ctx.author
        guild = ctx.guild



        # ==========================================
        # FIND ROLE
        # ==========================================

        role_data = role_manager.get_role(
            level
        )


        if not role_data:

            await ctx.send(
                "❌ Для этого уровня нет роли"
            )

            return



        role = guild.get_role(
            role_data["role_id"]
        )


        if not role:

            await ctx.send(
                "❌ Роль не найдена. Проверь ID"
            )

            return



        # ==========================================
        # REMOVE OLD RPG ROLES
        # ==========================================

        rank_role_ids = [

            data["role_id"]

            for data in LEVEL_ROLES.values()

        ]


        old_roles = [

            r

            for r in member.roles

            if r.id in rank_role_ids

        ]


        if old_roles:

            await member.remove_roles(
                *old_roles
            )



        # ==========================================
        # ADD NEW ROLE
        # ==========================================

        await member.add_roles(
            role
        )


        logger.info(
            f"{member.name} received rank role: {role.name}"
        )



        # ==========================================
        # RESPONSE
        # ==========================================

        embed = discord.Embed(
            title="🎮 LEVEL TEST",
            color=0x5865F2
        )


        embed.add_field(
            name="Игрок",
            value=member.mention,
            inline=False
        )


        embed.add_field(
            name="Уровень",
            value=f"⭐ {level}",
            inline=True
        )


        embed.add_field(
            name="Роль",
            value=role.mention,
            inline=True
        )


        await ctx.send(
            embed=embed
        )



async def setup(bot):

    print(
        "✅ TEST LEVEL COG LOADED"
    )


    await bot.add_cog(
        TestLevel(bot)
    )