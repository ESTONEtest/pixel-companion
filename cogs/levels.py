import discord
from discord.ext import commands

LEVELS = [
    (0, "🟫 Rookie"),
    (100, "🟩 Player"),
    (500, "🟦 Gamer"),
    (1500, "🟪 Veteran"),
    (3000, "🟨 Elite"),
    (6000, "🟥 Pro Player"),
    (10000, "💎 Legend")
]


class Levels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ─────────────────────────────
    # GET ROLE BY XP
    # ─────────────────────────────
    def get_role_name(self, xp):
        role_name = LEVELS[0][1]

        for req_xp, name in LEVELS:
            if xp >= req_xp:
                role_name = name

        return role_name

    # ─────────────────────────────
    # AUTO ROLE UPDATE
    # ─────────────────────────────
    async def update_role(self, member, xp):

        role_name = self.get_role_name(xp)
        guild = member.guild

        # ищем роль
        role = discord.utils.get(guild.roles, name=role_name)

        # если нет — создаём
        if role is None:
            role = await guild.create_role(name=role_name)

        # убираем старые роли системы
        for _, name in LEVELS:
            old_role = discord.utils.get(guild.roles, name=name)
            if old_role in member.roles:
                await member.remove_roles(old_role)

        # выдаём новую
        await member.add_roles(role)

    # ─────────────────────────────
    # HOOK (XP UPDATE)
    # ─────────────────────────────
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):

        # чтобы не дублировать — работаем только на выходе
        if before.channel and not after.channel:

            # импорт базы
            import json
            import os

            path = "database/economy.json"

            if not os.path.exists(path):
                return

            with open(path, "r", encoding="utf-8") as f:
                db = json.load(f)

            user_id = str(member.id)

            if user_id not in db:
                return

            xp = db[user_id].get("xp", 0)

            await self.update_role(member, xp)


async def setup(bot):
    await bot.add_cog(Levels(bot))