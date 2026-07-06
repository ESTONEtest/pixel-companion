import discord
from discord.ext import commands

from database.database import database


class Leaderboard(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="top")
    async def top(self, ctx: commands.Context):

        db = database.conn

        cursor = db.execute(
            """
            SELECT user_id, level, xp, balance
            FROM users
            ORDER BY level DESC, xp DESC
            LIMIT 10
            """
        )

        rows = cursor.fetchall()

        embed = discord.Embed(
            title="🏆 Топ игроков",
            color=discord.Color.gold()
        )

        if not rows:
            await ctx.send("Нет данных.")
            return

        description = ""

        for i, row in enumerate(rows, start=1):
            user_id, level, xp, balance = row

            user = self.bot.get_user(user_id)
            name = user.name if user else f"User {user_id}"

            description += (
                f"**{i}. {name}**\n"
                f"⭐ lvl: {level} | XP: {xp} | 💰 {balance}\n\n"
            )

        embed.description = description

        await ctx.send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Leaderboard(bot))