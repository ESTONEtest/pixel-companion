import discord
from discord.ext import commands

from database.database import database


class Leaderboard(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="top")
    async def top(self, ctx: commands.Context):

        cursor = database.conn.execute(
            """
            SELECT user_id, level, xp, money
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

        for i, (user_id, level, xp, money) in enumerate(rows, start=1):

            user = self.bot.get_user(user_id)

            if user is None:
                try:
                    user = await self.bot.fetch_user(user_id)
                except Exception:
                    user = None

            name = user.name if user else f"User {user_id}"

            description += (
                f"**{i}. {name}**\n"
                f"⭐ Level: {level} | XP: {xp} | 💰 {money}\n\n"
            )

        embed.description = description

        await ctx.send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Leaderboard(bot))