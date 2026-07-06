import time
import discord
from discord.ext import commands

from database.database import database


class Daily(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="daily")
    async def daily(self, ctx: commands.Context):

        user_id = ctx.author.id
        db = database.conn

        cursor = db.execute(
            "SELECT balance, daily_timestamp FROM users WHERE user_id = ?",
            (user_id,)
        )

        row = cursor.fetchone()

        if row is None:
            db.execute("INSERT INTO users(user_id) VALUES(?)", (user_id,))
            db.commit()
            balance, last_time = 500, 0
        else:
            balance, last_time = row

        now = int(time.time())
        cooldown = 86400

        if now - last_time < cooldown:
            remaining = cooldown - (now - last_time)
            h = remaining // 3600
            m = (remaining % 3600) // 60
            await ctx.send(f"⏳ Подожди {h}ч {m}м")
            return

        reward = 200
        xp_gain = 5

        new_balance = balance + reward

        db.execute(
            """
            UPDATE users
            SET balance = ?, daily_timestamp = ?, xp = xp + ?
            WHERE user_id = ?
            """,
            (new_balance, now, xp_gain, user_id)
        )

        db.commit()

        await ctx.send(f"💰 +{reward} монет | ⭐ +{xp_gain} XP")