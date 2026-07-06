import random
from discord.ext import commands

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hello(self, ctx):
        await ctx.send("👾 Привет, игрок!")

    @commands.command()
    async def roll(self, ctx):
        await ctx.send(f"🎲 {random.randint(1, 100)}")

    @commands.command()
    async def glitch(self, ctx):
        messages = [
            "▓▒░ SYSTEM ERROR ░▒▓",
            "⚠️ PIXEL CORRUPTION",
            "🧠 REALITY SHIFT",
            "⛓️ SIGNAL LOST"
        ]
        await ctx.send(random.choice(messages))


async def setup(bot):
    await bot.add_cog(Fun(bot))