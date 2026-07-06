import random
import time
import discord
from discord.ext import commands

from database.database import database


class Work(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="work")
    async def work(self, ctx: commands.Context):

        user_id = ctx.author.id
        db = database.conn

        cursor = db.execute(
            "SELECT balance, energy, work_timestamp FROM users WHERE user_id = ?",
            (user_id,)
        )

        row = cursor.fetchone()

        if row is None:
            db.execute("INSERT INTO users(user_id) VALUES(?)", (user_id,))
            db.commit()
            balance, energy, last_time = 500, 100, 0
        else:
            balance, energy, last_time = row

        now = int(time.time())
        cooldown = 1800

        if now - last_time < cooldown:
            await ctx.send("⏳ Отдохни 30 минут")
            return

        if energy < 10:
            await ctx.send("⚠️ Мало энергии")
            return

        reward = random.randint(80, 200)
        xp_gain = 10

        new_balance = balance + reward
        new_energy = energy - 10

        db.execute(
            """
            UPDATE users
            SET balance = ?, energy = ?, work_timestamp = ?, xp = xp + ?
            WHERE user_id = ?
            """,
            (new_balance, new_energy, now, xp_gain, user_id)
        )

        db.commit()

        await ctx.send(f"🛠 +{reward} монет | ⭐ +{xp_gain} XP")