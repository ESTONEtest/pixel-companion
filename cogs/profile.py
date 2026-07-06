import discord
from discord.ext import commands

from database.database import database


class Profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="me")
    async def me(self, ctx):

        user_id = ctx.author.id

        database.create_user(user_id)

        database.cursor.execute(
            "SELECT level, xp, money FROM users WHERE user_id = ?",
            (user_id,)
        )

        row = database.cursor.fetchone()

        if not row:
            level, xp, money = 0, 0, 0
        else:
            level, xp, money = row

        embed = discord.Embed(
            title=f"📊 Профиль {ctx.author.name}",
            color=discord.Color.green()
        )

        embed.add_field(name="Level", value=level, inline=True)
        embed.add_field(name="XP", value=xp, inline=True)
        embed.add_field(name="Money", value=money, inline=True)

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Profile(bot))