import discord
from discord.ext import commands


WELCOME_CHANNEL_ID = 1466499385411109090



class Welcome(commands.Cog):

    def __init__(self, bot):

        self.bot = bot



    # ==================================================
    # NEW MEMBER JOIN
    # ==================================================

    @commands.Cog.listener()
    async def on_member_join(
        self,
        member
    ):


        channel = self.bot.get_channel(
            WELCOME_CHANNEL_ID
        )


        if not channel:

            return



        embed = discord.Embed(

            title="🌟 NEW PLAYER DETECTED",

            description=(

                "```diff\n"
                "+ PLAYER CONNECTED\n"
                "```\n\n"

                f"👋 Добро пожаловать, {member.mention}!\n\n"

                "🎮 Ты вошёл в мир **Pixel Companion**.\n\n"

                "⚔ Твой путь только начинается...\n\n"

                "✨ Исследуй сервер,\n"
                "🎒 собирай предметы,\n"
                "👹 сражайся с монстрами,\n"
                "🏆 получай новые ранги!\n\n"

                "```"
                "STATUS: PLAYER REGISTERED\n"
                "CLASS: UNKNOWN\n"
                "LEVEL: 1\n"
                "```\n\n"

                "🔥 Приготовься к приключению!"

            ),

            color=discord.Color.dark_purple()

        )



        embed.set_thumbnail(

            url=member.display_avatar.url

        )


        embed.set_footer(

            text=
            "Pixel Companion RPG • Welcome System"

        )



        await channel.send(

            embed=embed

        )





async def setup(bot):


    print(
        "✅ WELCOME COG LOADED"
    )


    await bot.add_cog(
        Welcome(bot)
    )