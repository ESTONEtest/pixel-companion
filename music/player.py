import asyncio
import os
import shutil

import discord


# ==================================================
# FFMPEG
# ==================================================

def get_ffmpeg_path():

    # Linux / Railway / Nixpacks
    ffmpeg = shutil.which("ffmpeg")

    if ffmpeg:
        return ffmpeg


    # Linux fallback
    linux_path = "/usr/bin/ffmpeg"

    if os.path.exists(linux_path):
        return linux_path


    # Windows local
    windows_ffmpeg = r"D:\ffmpeg-8.1.2-essentials_build\bin\ffmpeg.exe"

    if os.path.exists(windows_ffmpeg):
        return windows_ffmpeg


    return None



FFMPEG_PATH = get_ffmpeg_path()

print(f"🎵 FFmpeg path: {FFMPEG_PATH}")


# ==================================================
# MUSIC FOLDER
# ==================================================

MUSIC_FOLDER = "music/songs"



# ==================================================
# MUSIC PLAYER
# ==================================================

class MusicPlayer:


    def __init__(self):

        self.voice_client = None

        self.current_song = None

        self.queue = []

        self.ctx = None

        self.volume = 0.5

        self.panel_message = None



    # ==================================================
    # CONNECT
    # ==================================================

    async def connect(self, ctx, channel_id):


        channel = ctx.guild.get_channel(channel_id)


        if channel is None:

            await ctx.send(
                "❌ Не найден голосовой канал музыки"
            )

            return False



        if not isinstance(channel, discord.VoiceChannel):

            await ctx.send(
                "❌ ID не является голосовым каналом"
            )

            return False



        if self.voice_client:


            if self.voice_client.channel != channel:

                await self.voice_client.move_to(
                    channel
                )


            return True



        if ctx.guild.voice_client:


            self.voice_client = ctx.guild.voice_client


            if self.voice_client.channel != channel:

                await self.voice_client.move_to(
                    channel
                )


        else:


            self.voice_client = await channel.connect(
                reconnect=True
            )



        return True




    # ==================================================
    # PLAY ALBUM
    # ==================================================

    async def play_album(
        self,
        ctx,
        songs,
        channel_id
    ):


        self.ctx = ctx


        if not await self.connect(
            ctx,
            channel_id
        ):

            return False



        self.queue.clear()


        self.queue.extend(
            songs
        )


        await self.play_next()


        return True




    # ==================================================
    # PLAY NEXT
    # ==================================================

    async def play_next(self):


        if not self.queue:


            self.current_song = None

            await self.update_panel()

            return



        song = self.queue.pop(0)



        path = os.path.join(
            MUSIC_FOLDER,
            song
        )



        if not os.path.exists(path):


            print(
                f"❌ Song not found: {path}"
            )


            await self.play_next()

            return




        if not FFMPEG_PATH:


            print(
                "❌ FFmpeg не найден"
            )

            return




        try:


            audio = discord.FFmpegPCMAudio(

                executable=FFMPEG_PATH,

                source=path,

                options="-vn"

            )


            source = discord.PCMVolumeTransformer(

                audio,

                volume=self.volume

            )


        except Exception as e:


            print(
                f"❌ FFmpeg error: {e}"
            )

            return





        def after(error):


            if error:

                print(
                    f"Music error: {error}"
                )


            if self.ctx:

                asyncio.run_coroutine_threadsafe(

                    self.play_next(),

                    self.ctx.bot.loop

                )





        if self.voice_client.is_playing():

            self.voice_client.stop()



        self.voice_client.play(

            source,

            after=after

        )



        self.current_song = song



        print(
            f"🎶 Playing: {song}"
        )


        await self.update_panel()





    # ==================================================
    # CONTROLS
    # ==================================================

    def pause(self):

        if self.voice_client:

            if self.voice_client.is_playing():

                self.voice_client.pause()




    def resume(self):

        if self.voice_client:

            if self.voice_client.is_paused():

                self.voice_client.resume()




    def skip(self):

        if self.voice_client:

            if self.voice_client.is_playing():

                self.voice_client.stop()





    async def stop(self):


        self.queue.clear()



        if self.voice_client:


            self.voice_client.stop()


            await self.voice_client.disconnect()


            self.voice_client = None




        self.current_song = None



        await self.update_panel()





    # ==================================================
    # VOLUME
    # ==================================================

    def change_volume(
        self,
        value
    ):


        self.volume += value



        self.volume = max(
            0,
            min(
                1,
                self.volume
            )
        )



        if self.voice_client:


            if isinstance(

                self.voice_client.source,

                discord.PCMVolumeTransformer

            ):

                self.voice_client.source.volume = self.volume




        asyncio.create_task(
            self.update_panel()
        )




    def get_volume(self):

        return int(
            self.volume * 100
        )





    # ==================================================
    # INFO
    # ==================================================

    def get_current(self):

        return (
            self.current_song
            if self.current_song
            else "Ничего не играет"
        )




    def get_queue(self):

        return self.queue





    # ==================================================
    # PANEL
    # ==================================================

    async def update_panel(self):


        if not self.panel_message:

            return



        embed = discord.Embed(

            title="📼 PIXEL CASSETTE",

            description=(

                f"🎵 Сейчас играет:\n"
                f"`{self.current_song or 'Нет трека'}`\n\n"

                f"📀 Осталось:\n"
                f"`{len(self.queue)}`\n\n"

                f"🔊 Громкость:\n"
                f"`{self.get_volume()}%`"

            ),

            color=discord.Color.blurple()

        )


        embed.set_footer(

            text="Pixel Companion Music System"

        )



        try:

            await self.panel_message.edit(
                embed=embed
            )


        except Exception:

            pass