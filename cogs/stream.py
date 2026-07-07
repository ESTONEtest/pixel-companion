import discord
from discord.ext import commands, tasks

import aiohttp


TWITCH_CHANNEL = "captain_icecream"

STREAM_CHANNEL_ID = 1523449588709855372  # ID канала 🔴│стрим-оповещения

CHECK_INTERVAL = 60



class Stream(commands.Cog):

    def __init__(self, bot):

        self.bot = bot

        self.live_status = False

        self.stream_check.start()



    def cog_unload(self):

        self.stream_check.cancel()



    # ==================================================
    # TWITCH CHECK
    # ==================================================

    @tasks.loop(seconds=CHECK_INTERVAL)
    async def stream_check(self):


        if not self.bot.is_ready():

            return



        live = await self.check_twitch()



        if live and not self.live_status:


            self.live_status = True


            await self.send_stream_alert()



        elif not live:


            self.live_status = False





    async def check_twitch(self):


        url = (
            f"https://www.twitch.tv/"
            f"{TWITCH_CHANNEL}"
        )


        headers = {

            "User-Agent":
            "Mozilla/5.0"

        }



        try:

            async with aiohttp.ClientSession() as session:

                async with session.get(
                    url,
                    headers=headers
                ) as response:


                    text = await response.text()



                    if '"isLive":true' in text:

                        return True



        except Exception as error:


            print(
                f"Twitch error: {error}"
            )



        return False





    # ==================================================
    # SEND ALERT
    # ==================================================

    async def send_stream_alert(self):


        channel = self.bot.get_channel(
            STREAM_CHANNEL_ID
        )



        if not channel:

            return



        embed = discord.Embed(

            title="🎮 PIXEL STREAM ONLINE",

            description=(

                "```diff\n"
                "+ NEW ADVENTURE STARTED\n"
                "```\n\n"

                "🔥 **Стример вышел в эфир!**\n\n"

                "👤 **@fakeevilmvp** "
                "открыл новый игровой портал.\n\n"

                "⚔ Заходи поддержать героя!\n\n"

                "🕹 Возможны легендарные моменты.\n\n"

                "🌐 "
                "https://www.twitch.tv/captain_icecream"

            ),

            color=discord.Color.purple()

        )



        embed.set_footer(

            text=
            "Pixel Companion RPG • Stream System"

        )



        await channel.send(

            content="@everyone",

            embed=embed

        )





    # ==================================================
    # TEST COMMAND
    # ==================================================

    @commands.command(
        name="streamtest"
    )
    async def streamtest(
        self,
        ctx
    ):


        channel = self.bot.get_channel(
            STREAM_CHANNEL_ID
        )



        if not channel:


            await ctx.send(

                "❌ Канал стримов не найден"

            )

            return





        embed = discord.Embed(

            title="🎮 PIXEL STREAM ONLINE",

            description=(

                "```diff\n"
                "+ TEST SIGNAL RECEIVED\n"
                "```\n\n"

                "🔥 **Стример вышел в эфир!**\n\n"

                "👤 **@fakeevilmvp** "
                "зовёт всех игроков.\n\n"

                "⚔ Присоединяйся к приключению!\n\n"

                "🌐 "
                "https://www.twitch.tv/captain_icecream"

            ),

            color=discord.Color.purple()

        )


        embed.set_footer(

            text=
            "Pixel Companion RPG • Test"

        )



        await channel.send(

            content="@everyone",

            embed=embed

        )



        await ctx.send(

            "✅ Stream test отправлен"

        )





async def setup(bot):


    print(
        "✅ STREAM COG LOADED"
    )


    await bot.add_cog(
        Stream(bot)
    )