import discord

from discord.ext import commands

from managers.player_manager import player_manager
from managers.rank_manager import rank_manager
from systems.healing import healing_system


class Profile(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # ==================================================
    # PROFILE
    # ==================================================

    @commands.command(name="profile", aliases=["me"])
    async def profile(self, ctx):

        user = player_manager.get_player(
            ctx.author.id
        )

        if not user:

            player_manager.create_player(
                ctx.author.id,
                ctx.author.name
            )

            user = player_manager.get_player(
                ctx.author.id
            )

        if not user:

            await ctx.send(
                "❌ Не удалось создать профиль. Попробуйте еще раз."
            )

            return

        rank = rank_manager.get_rank(
            user["level"]
        )

        embed = discord.Embed(
            title="🎮 Pixel Profile",
            color=discord.Color.dark_purple()
        )

        embed.add_field(
            name="👤 Player",
            value=ctx.author.mention,
            inline=False
        )

        embed.add_field(
            name="❤️ HP",
            value=f"`{user['hp']} / {user['max_hp']}`",
            inline=True
        )

        embed.add_field(
            name="⭐ Level",
            value=f"`{user['level']}`",
            inline=True
        )

        embed.add_field(
            name="✨ XP",
            value=f"`{user['xp']}`",
            inline=True
        )

        embed.add_field(
            name="💰 Coins",
            value=f"`{user['coins']}`",
            inline=True
        )

        embed.add_field(
            name="⚔ Stats",
            value=(
                f"⚔ Attack: `{user['attack']}`\n"
                f"🛡 Defense: `{user['defense']}`\n"
                f"🍀 Luck: `{user['luck']}`"
            ),
            inline=False
        )

        embed.add_field(
            name="🏆 Rank",
            value=rank,
            inline=False
        )

        embed.set_footer(
            text="Pixel Companion RPG v2.0"
        )

        await ctx.send(
            embed=embed
        )

    # ==================================================
    # HEAL
    # ==================================================

    @commands.command(name="heal")
    async def heal(self, ctx):

        user_id = ctx.author.id

        user = player_manager.get_player(
            user_id
        )

        if not user:

            player_manager.create_player(
                user_id,
                ctx.author.name
            )

            user = player_manager.get_player(
                user_id
            )

        if not user:

            await ctx.send(
                "❌ Не удалось создать профиль. Попробуйте еще раз."
            )

            return

        if user["hp"] >= user["max_hp"]:

            await ctx.send(
                "❤️ Ваше здоровье уже полностью восстановлено."
            )

            return

        new_hp = healing_system.heal(
            current_hp=user["hp"],
            amount=30,
            max_hp=user["max_hp"]
        )

        healed = new_hp - user["hp"]

        player_manager.set_hp(
            user_id,
            new_hp
        )

        embed = discord.Embed(
            title="🧪 Восстановление",
            description=f"Вы восстановили **{healed} HP**.",
            color=discord.Color.green()
        )

        embed.add_field(
            name="❤️ HP",
            value=f"`{new_hp} / {user['max_hp']}`",
            inline=False
        )

        embed.set_footer(
            text="Здоровье восстановлено."
        )

        await ctx.send(
            embed=embed
        )


async def setup(bot):

    await bot.add_cog(
        Profile(bot)
    )