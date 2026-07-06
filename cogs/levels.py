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

        database.create_user(user_id)

        database.cursor.execute(
            "UPDATE users SET xp = xp + 5, money = money + 1 WHERE user_id = ?",
            (user_id,)
        )
        database.conn.commit()

        database.cursor.execute(
            "SELECT level, xp FROM users WHERE user_id = ?",
            (user_id,)
        )

        row = database.cursor.fetchone()

        if row is None:
            return

        level, xp = row

        needed = 100 + (level * 50)

        if xp >= needed:
            level += 1
            xp = 0

            database.cursor.execute(
                "UPDATE users SET level = ?, xp = ? WHERE user_id = ?",
                (level, xp, user_id)
            )
            database.conn.commit()

            await message.channel.send(
                f"🎉 {message.author.mention} получил новый уровень: **{level}**!"
            )


async def setup(bot):
    await bot.add_cog(Levels(bot))