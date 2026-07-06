from discord.ext import commands

class Work(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # пример команды (если у тебя уже есть логика — вставишь обратно)
    @commands.command()
    async def work(self, ctx):
        await ctx.send("Ты поработал 💼")

async def setup(bot):
    await bot.add_cog(Work(bot))