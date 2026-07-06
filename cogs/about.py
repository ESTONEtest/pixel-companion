from discord.ext import commands

class About(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def test(self, ctx):
        await ctx.send("🎮 About cog работает!")

async def setup(bot):
    await bot.add_cog(About(bot))