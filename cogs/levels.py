import discord
from discord.ext import commands

from database.database import database


class Levels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author.bot:
            return

        user_id = message.author.id
        db = database.conn

        cursor = db.execute(
            "SELECT level, xp FROM users WHERE user_id = ?",
            (user_id,)
        )

        row = cursor.fetchone()

        if row is None:
            db.execute("INSERT INTO users(user_id) VALUES(?)", (user_id,))
            db.commit()
            return

        level, xp = row

        needed = level * 100

        if xp >= needed:

            level += 1
            xp = 0

            db.execute(
                "UPDATE users SET level = ?, xp = ? WHERE user_id = ?",
                (level, xp, user_id)
            )
            db.commit()

            await message.channel.send(
                f"🎉 {message.author.mention} уровень {level}!"
            )


async def setup(bot):
    await bot.add_cog(Levels(bot))