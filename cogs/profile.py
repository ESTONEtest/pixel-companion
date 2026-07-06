import discord
from discord.ext import commands

from database.database import database


class Profile(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="me")
    async def me(self, ctx: commands.Context):

        user_id = ctx.author.id
        db = database.conn

        cursor = db.execute(
            """
            SELECT level, xp, balance, hp, max_hp, energy, max_energy, hunger, max_hunger
            FROM users
            WHERE user_id = ?
            """,
            (user_id,)
        )

        row = cursor.fetchone()

        if row is None:
            db.execute(
                "INSERT INTO users(user_id) VALUES(?)",
                (user_id,)
            )
            db.commit()

            row = (1, 0, 500, 100, 100, 100, 100, 100, 100)

        level, xp, balance, hp, max_hp, energy, max_energy, hunger, max_hunger = row

        embed = discord.Embed(
            title="👤 Твой профиль",
            color=discord.Color.blurple()
        )

        embed.add_field(name="⭐ Уровень", value=level, inline=True)
        embed.add_field(name="✨ XP", value=xp, inline=True)
        embed.add_field(name="💰 Баланс", value=balance, inline=True)

        embed.add_field(name="❤️ HP", value=f"{hp}/{max_hp}", inline=True)
        embed.add_field(name="⚡ Энергия", value=f"{energy}/{max_energy}", inline=True)
        embed.add_field(name="🍖 Голод", value=f"{hunger}/{max_hunger}", inline=True)

        await ctx.send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Profile(bot))