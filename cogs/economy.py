import discord
from discord.ext import commands
import json
import os
import time

DB_PATH = "database/economy.json"


class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ─────────────────────────────
    # SAFE DB LOAD
    # ─────────────────────────────
    def load_db(self):
        if not os.path.exists(DB_PATH):
            return {}

        try:
            with open(DB_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}

    # ─────────────────────────────
    # SAVE DB
    # ─────────────────────────────
    def save_db(self, db):
        with open(DB_PATH, "w", encoding="utf-8") as f:
            json.dump(db, f, indent=4)

    # ─────────────────────────────
    # ENSURE USER EXISTS
    # ─────────────────────────────
    def ensure_user(self, db, user_id):
        if str(user_id) not in db:
            db[str(user_id)] = {
                "coins": 0,
                "xp": 0,
                "last_voice": 0
            }

    # ─────────────────────────────
    # VOICE REWARD SYSTEM
    # ─────────────────────────────
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):

        db = self.load_db()
        self.ensure_user(db, member.id)

        user = db[str(member.id)]
        now = int(time.time())

        # вошёл в голос
        if after.channel and not before.channel:
            user["last_voice"] = now

        # вышел из голоса
        if before.channel and not after.channel:
            if user["last_voice"] != 0:
                duration = now - user["last_voice"]

                coins = duration // 10   # 1 coin за 10 сек
                xp = duration // 5       # XP быстрее

                user["coins"] += coins
                user["xp"] += xp
                user["last_voice"] = 0

        self.save_db(db)

    # ─────────────────────────────
    # PROFILE COMMAND
    # ─────────────────────────────
    @commands.command()
    async def profile(self, ctx):

        db = self.load_db()
        self.ensure_user(db, ctx.author.id)

        user = db[str(ctx.author.id)]

        embed = discord.Embed(
            title=f"👤 {ctx.author.name}",
            description="📊 Pixel Profile",
            color=0x8A2BE2
        )

        embed.add_field(name="💰 Coins", value=user["coins"])
        embed.add_field(name="⭐ XP", value=user["xp"])

        await ctx.send(embed=embed)

    # ─────────────────────────────
    # OPTIONAL: ADD COINS TEST
    # ─────────────────────────────
    @commands.command()
    async def daily(self, ctx):

        db = self.load_db()
        self.ensure_user(db, ctx.author.id)

        db[str(ctx.author.id)]["coins"] += 50
        self.save_db(db)

        await ctx.send("💰 +50 coins (daily reward)")


async def setup(bot):
    await bot.add_cog(Economy(bot))