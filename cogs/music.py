import os
import discord

from discord.ext import commands
from discord.ui import Button, View

from music.player import MusicPlayer


# ==================================================
# SETTINGS
# ==================================================

MUSIC_FOLDER = "music/songs"

COMMAND_CHANNEL_NAME = "🌙┃эхо-души"

MUSIC_VOICE_CHANNEL_ID = 1525683653999329423



# ==================================================
# MUSIC BUTTONS
# ==================================================

class MusicControls(View):

    def __init__(self, player):

        super().__init__(
            timeout=None
        )

        self.player = player



    @discord.ui.button(
        emoji="⏭️",
        style=discord.ButtonStyle.primary
    )
    async def skip(
        self,
        interaction: discord.Interaction,
        button: Button
    ):

        self.player.skip()

        await interaction.response.send_message(
            "⏭️ Следующий трек...",
            ephemeral=True
        )



    @discord.ui.button(
        emoji="⏸️",
        style=discord.ButtonStyle.secondary
    )
    async def pause(
        self,
        interaction: discord.Interaction,
        button: Button
    ):

        self.player.pause()

        await interaction.response.send_message(
            "⏸️ Музыка на паузе",
            ephemeral=True
        )



    @discord.ui.button(
        emoji="▶️",
        style=discord.ButtonStyle.success
    )
    async def resume(
        self,
        interaction: discord.Interaction,
        button: Button
    ):

        self.player.resume()

        await interaction.response.send_message(
            "▶️ Продолжаем",
            ephemeral=True
        )



    @discord.ui.button(
        emoji="🔉",
        style=discord.ButtonStyle.secondary
    )
    async def volume_down(
        self,
        interaction: discord.Interaction,
        button: Button
    ):

        self.player.change_volume(-0.1)

        await interaction.response.send_message(
            f"🔉 Громкость: {self.player.get_volume()}%",
            ephemeral=True
        )



    @discord.ui.button(
        emoji="🔊",
        style=discord.ButtonStyle.secondary
    )
    async def volume_up(
        self,
        interaction: discord.Interaction,
        button: Button
    ):

        self.player.change_volume(0.1)

        await interaction.response.send_message(
            f"🔊 Громкость: {self.player.get_volume()}%",
            ephemeral=True
        )



    @discord.ui.button(
        emoji="⏹️",
        style=discord.ButtonStyle.danger
    )
    async def stop(
        self,
        interaction: discord.Interaction,
        button: Button
    ):

        await self.player.stop()

        await interaction.response.send_message(
            "⏹️ Кассета остановлена",
            ephemeral=True
        )



# ==================================================
# MUSIC COG
# ==================================================

class Music(commands.Cog):

    def __init__(self, bot):

        self.bot = bot

        self.player = MusicPlayer()



    def check_command_channel(self, ctx):

        return ctx.channel.name == COMMAND_CHANNEL_NAME



    def get_songs(self):

        if not os.path.exists(MUSIC_FOLDER):

            return []


        songs = []


        for file in os.listdir(MUSIC_FOLDER):

            if file.endswith(
                (
                    ".mp3",
                    ".wav",
                    ".ogg"
                )
            ):

                songs.append(file)



        songs.sort()

        return songs



    # ==================================================
    # ALBUM
    # ==================================================

    @commands.command(name="album")
    async def album(self, ctx):


        if not self.check_command_channel(ctx):

            await ctx.send(
                "🎧 Команды музыки доступны только в 🌙┃эхо-души"
            )

            return



        songs = self.get_songs()



        if not songs:

            await ctx.send(
                "📼 Кассета пустая..."
            )

            return



        await self.player.play_album(
            ctx,
            songs,
            MUSIC_VOICE_CHANNEL_ID
        )



        embed = discord.Embed(

            title="📼 PIXEL CASSETTE",

            description=(

                f"🎶 Загружено песен: **{len(songs)}**\n\n"

                f"🎵 Сейчас играет:\n"
                f"`{self.player.get_current()}`\n\n"

                f"🔊 Громкость:\n"
                f"`{self.player.get_volume()}%`"

            ),

            color=discord.Color.blurple()

        )



        embed.set_footer(
            text="Pixel Companion Music System"
        )



        if self.player.panel_message:


            try:

                await self.player.panel_message.delete()

            except:

                pass



        message = await ctx.send(

            embed=embed,

            view=MusicControls(
                self.player
            )

        )


        self.player.panel_message = message



    # ==================================================
    # COMMANDS
    # ==================================================

    @commands.command(name="skip")
    async def skip(self, ctx):

        if not self.check_command_channel(ctx):

            return


        self.player.skip()


        await ctx.send(
            "⏭️ Следующий трек"
        )



    @commands.command(name="pause")
    async def pause(self, ctx):

        if not self.check_command_channel(ctx):

            return


        self.player.pause()


        await ctx.send(
            "⏸️ Пауза"
        )



    @commands.command(name="resume")
    async def resume(self, ctx):

        if not self.check_command_channel(ctx):

            return


        self.player.resume()


        await ctx.send(
            "▶️ Продолжено"
        )



    @commands.command(name="stop")
    async def stop(self, ctx):

        if not self.check_command_channel(ctx):

            return


        await self.player.stop()


        await ctx.send(
            "⏹️ Музыка остановлена"
        )



# ==================================================
# LOAD COG
# ==================================================

async def setup(bot):

    await bot.add_cog(
        Music(bot)
    )