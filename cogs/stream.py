import discord
import aiohttp

from discord.ext import commands, tasks

from config import STREAM_CHANNEL_ID
from config import TWITCH_CHANNEL
from config import TWITCH_CLIENT_ID
from config import TWITCH_CLIENT_SECRET


CHECK_INTERVAL = 60


class Stream(commands.Cog):

    def __init__(self, bot):

        self.bot = bot
        self.live_status = False
        self.access_token = None

        self.stream_check.start()

    def cog_unload(self):

        self.stream_check.cancel()

    # ==================================================
    # SETTINGS
    # ==================================================

    def twitch_configured(self):

        return (
            bool(STREAM_CHANNEL_ID)
            and bool(TWITCH_CHANNEL)
            and bool(TWITCH_CLIENT_ID)
            and bool(TWITCH_CLIENT_SECRET)
        )

    # ==================================================
    # TOKEN
    # ==================================================

    async def get_access_token(self):

        if not TWITCH_CLIENT_ID or not TWITCH_CLIENT_SECRET:

            print(
                "❌ Twitch API keys not found. Check TWITCH_CLIENT_ID and TWITCH_CLIENT_SECRET."
            )

            return None

        url = "https://id.twitch.tv/oauth2/token"

        params = {
            "client_id": TWITCH_CLIENT_ID,
            "client_secret": TWITCH_CLIENT_SECRET,
            "grant_type": "client_credentials"
        }

        try:

            async with aiohttp.ClientSession() as session:

                async with session.post(
                    url,
                    params=params
                ) as response:

                    data = await response.json()

                    if response.status != 200:

                        print(
                            f"❌ Twitch token error: {data}"
                        )

                        return None

                    self.access_token = data["access_token"]

                    return self.access_token

        except Exception as error:

            print(
                f"❌ Twitch token request error: {error}"
            )

            return None

    # ==================================================
    # TWITCH API
    # ==================================================

    async def get_stream_data(self):

        if not self.twitch_configured():

            print(
                "❌ Twitch stream system is not configured."
            )

            return None

        if not self.access_token:

            await self.get_access_token()

        if not self.access_token:

            return None

        url = "https://api.twitch.tv/helix/streams"

        headers = {
            "Client-ID": TWITCH_CLIENT_ID,
            "Authorization": f"Bearer {self.access_token}"
        }

        params = {
            "user_login": TWITCH_CHANNEL
        }

        try:

            async with aiohttp.ClientSession() as session:

                async with session.get(
                    url,
                    headers=headers,
                    params=params
                ) as response:

                    data = await response.json()

                    if response.status == 401:

                        self.access_token = None

                        await self.get_access_token()

                        if not self.access_token:
                            return None

                        return await self.get_stream_data()

                    if response.status != 200:

                        print(
                            f"❌ Twitch API error: {data}"
                        )

                        return None

                    streams = data.get(
                        "data",
                        []
                    )

                    if not streams:

                        return None

                    return streams[0]

        except Exception as error:

            print(
                f"❌ Twitch check error: {error}"
            )

            return None

    # ==================================================
    # LOOP
    # ==================================================

    @tasks.loop(seconds=CHECK_INTERVAL)
    async def stream_check(self):

        stream_data = await self.get_stream_data()

        if stream_data and not self.live_status:

            self.live_status = True

            await self.send_stream_alert(
                stream_data
            )

        elif not stream_data:

            self.live_status = False

    @stream_check.before_loop
    async def before_stream_check(self):

        await self.bot.wait_until_ready()

    # ==================================================
    # SEND ALERT
    # ==================================================

    async def send_stream_alert(
        self,
        stream_data: dict
    ):

        channel = self.bot.get_channel(
            STREAM_CHANNEL_ID
        )

        if not channel:

            print(
                "❌ Stream channel not found."
            )

            return

        title = stream_data.get(
            "title",
            "Стрим начался!"
        )

        game_name = stream_data.get(
            "game_name",
            "Неизвестная игра"
        )

        viewer_count = stream_data.get(
            "viewer_count",
            0
        )

        thumbnail = stream_data.get(
            "thumbnail_url"
        )

        stream_url = f"https://www.twitch.tv/{TWITCH_CHANNEL}"

        embed = discord.Embed(
            title="🔴 PIXEL STREAM ONLINE",
            description=(
                "```diff\n"
                "+ NEW ADVENTURE STARTED\n"
                "```\n\n"
                "🔥 **Стример вышел в эфир!**\n\n"
                f"👤 **{TWITCH_CHANNEL}** открыл новый игровой портал.\n\n"
                f"🎬 **Название:** {title}\n"
                f"🎮 **Игра:** {game_name}\n"
                f"👀 **Зрителей:** `{viewer_count}`\n\n"
                "⚔ Заходи поддержать героя!\n\n"
                f"🌐 {stream_url}"
            ),
            color=discord.Color.purple(),
            url=stream_url
        )

        if thumbnail:

            thumbnail = thumbnail.replace(
                "{width}",
                "1280"
            ).replace(
                "{height}",
                "720"
            )

            embed.set_image(
                url=thumbnail
            )

        embed.set_footer(
            text="Pixel Companion RPG • Twitch API"
        )

        await channel.send(
            content="@everyone",
            embed=embed
        )

    # ==================================================
    # STATUS COMMAND
    # ==================================================

    @commands.command(name="streamstatus")
    async def streamstatus(self, ctx):

        stream_data = await self.get_stream_data()

        if not stream_data:

            await ctx.send(
                "⚫ Сейчас стрим не идет."
            )

            return

        await ctx.send(
            f"🔴 Стрим онлайн: https://www.twitch.tv/{TWITCH_CHANNEL}"
        )

    # ==================================================
    # TEST COMMAND
    # ==================================================

    @commands.command(name="streamtest")
    @commands.has_permissions(administrator=True)
    async def streamtest(self, ctx):

        test_data = {
            "title": "Тестовое оповещение",
            "game_name": "Pixel Companion",
            "viewer_count": 1,
            "thumbnail_url": None
        }

        await self.send_stream_alert(
            test_data
        )

        await ctx.send(
            "✅ Stream test отправлен."
        )


async def setup(bot):

    print(
        "✅ STREAM COG LOADED"
    )

    await bot.add_cog(
        Stream(bot)
    )