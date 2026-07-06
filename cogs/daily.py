from discord.ext import commands

class Daily(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def daily(self, ctx):
        await ctx.send("Ты забрал daily 💰")

async def setup(bot):
    await bot.add_cog(Daily(bot))