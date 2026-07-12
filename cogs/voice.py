import discord

from discord.ext import commands

from managers.database import database


VOICE_CATEGORY_NAME = "🎧 Pixel Voices"



class VoiceSystem(commands.Cog):


    def __init__(self, bot):

        self.bot = bot



    # ==================================================
    # CREATE / DELETE VOICE
    # ==================================================


    @commands.Cog.listener()
    async def on_voice_state_update(
        self,
        member,
        before,
        after
    ):


        # ==============================================
        # CREATE ROOM
        # ==============================================


        if after.channel:


            guild = member.guild


            if after.channel.name == "➕ create-voice":


                category = discord.utils.get(
                    guild.categories,
                    name=VOICE_CATEGORY_NAME
                )


                if category is None:

                    category = await guild.create_category(
                        VOICE_CATEGORY_NAME
                    )



                voice = await guild.create_voice_channel(

                    name=f"🎧 {member.name}",

                    category=category

                )



                # Текстовый чат скрыт от всех, кроме создателя комнаты
                overwrites = {

                    guild.default_role: discord.PermissionOverwrite(
                        view_channel=False
                    ),

                    member: discord.PermissionOverwrite(
                        view_channel=True,
                        send_messages=True,
                        read_message_history=True
                    )

                }


                # Бот сохраняет доступ к созданному текстовому каналу
                if guild.me:

                    overwrites[guild.me] = discord.PermissionOverwrite(
                        view_channel=True,
                        send_messages=True,
                        read_message_history=True
                    )



                text = await guild.create_text_channel(

                    name=f"💬-{member.name}",

                    category=category,

                    overwrites=overwrites

                )



                await member.move_to(
                    voice
                )



                database.execute(
                    """
                    INSERT OR REPLACE INTO voice_rooms

                    (
                        owner_id,
                        channel_id,
                        channel_name
                    )

                    VALUES (?, ?, ?)

                    """,
                    (
                        member.id,
                        voice.id,
                        voice.name
                    )
                )



                embed = discord.Embed(

                    title="🎧 Управление комнатой",

                    description=
                    """
👑 **Команды владельца**

`!vrename название`
✏ изменить название

`!vlimit число`
👥 изменить лимит

`!vlock`
🔒 закрыть комнату

`!vunlock`
🔓 открыть комнату

`!vkick @user`
👢 выгнать пользователя

`!vban @user`
🚫 запретить вход

`!vunban @user`
✅ снять запрет


ℹ️ Команды доступны только владельцу
и только в этом текстовом канале.
                    """,

                    color=discord.Color.blurple()

                )


                await text.send(
                    embed=embed
                )



        # ==============================================
        # DELETE EMPTY ROOM
        # ==============================================


        if before.channel:


            channel = before.channel



            room = database.fetchone(
                """
                SELECT *

                FROM voice_rooms

                WHERE channel_id = ?

                """,
                (
                    channel.id,
                )
            )



            if room:


                if len(channel.members) == 0:



                    database.execute(
                        """
                        DELETE FROM voice_rooms

                        WHERE channel_id = ?

                        """,
                        (
                            channel.id,
                        )
                    )


                    database.execute(
                        """
                        DELETE FROM voice_bans

                        WHERE channel_id = ?

                        """,
                        (
                            channel.id,
                        )
                    )


                    text = discord.utils.get(

                        channel.guild.text_channels,

                        name=f"💬-{room['channel_name'].replace('🎧 ', '')}"

                    )


                    if text:

                        await text.delete()



                    await channel.delete()



    # ==================================================
    # OWNER CHECK
    # ==================================================


    def get_owner_room(
        self,
        user_id
    ):


        return database.fetchone(

            """
            SELECT *

            FROM voice_rooms

            WHERE owner_id = ?

            """,

            (
                user_id,
            )

        )



    # Проверяет владельца и личный текстовый канал комнаты
    def get_owner_room_for_command(
        self,
        ctx
    ):


        room = self.get_owner_room(
            ctx.author.id
        )


        if not room:

            return None



        text_channel = discord.utils.get(

            ctx.guild.text_channels,

            name=f"💬-{room['channel_name'].replace('🎧 ', '')}"

        )


        if text_channel is None:

            return None



        if ctx.channel.id != text_channel.id:

            return None



        return room



    # ==================================================
    # RENAME
    # ==================================================


    @commands.command(
        name="vrename"
    )
    async def rename(
        self,
        ctx,
        *,
        name
    ):


        room = self.get_owner_room_for_command(
            ctx
        )


        if not room:

            return



        channel = ctx.guild.get_channel(
            room["channel_id"]
        )



        await channel.edit(
            name=f"🎧 {name}"
        )


        await ctx.send(
            "✏ Название комнаты изменено."
        )



    # ==================================================
    # LIMIT
    # ==================================================


    @commands.command(
        name="vlimit"
    )
    async def limit(
        self,
        ctx,
        amount:int
    ):


        room = self.get_owner_room_for_command(
            ctx
        )


        if not room:

            return



        if amount < 0 or amount > 99:

            await ctx.send(
                "❌ Лимит от 0 до 99."
            )

            return



        channel = ctx.guild.get_channel(
            room["channel_id"]
        )



        await channel.edit(
            user_limit=amount
        )



        database.execute(
            """
            UPDATE voice_rooms

            SET user_limit = ?

            WHERE channel_id = ?

            """,
            (
                amount,
                channel.id
            )
        )


        await ctx.send(
            f"👥 Лимит: {amount}"
        )



    # ==================================================
    # LOCK
    # ==================================================


    @commands.command(
        name="vlock"
    )
    async def lock(
        self,
        ctx
    ):


        room = self.get_owner_room_for_command(
            ctx
        )


        if not room:

            return



        channel = ctx.guild.get_channel(
            room["channel_id"]
        )



        await channel.set_permissions(

            ctx.guild.default_role,

            connect=False

        )


        await ctx.send(
            "🔒 Комната закрыта."
        )



    # ==================================================
    # UNLOCK
    # ==================================================


    @commands.command(
        name="vunlock"
    )
    async def unlock(
        self,
        ctx
    ):


        room = self.get_owner_room_for_command(
            ctx
        )


        if not room:

            return



        channel = ctx.guild.get_channel(
            room["channel_id"]
        )



        await channel.set_permissions(

            ctx.guild.default_role,

            connect=True

        )


        await ctx.send(
            "🔓 Комната открыта."
        )



    # ==================================================
    # KICK
    # ==================================================


    @commands.command(
        name="vkick"
    )
    async def kick(
        self,
        ctx,
        member: discord.Member
    ):


        room = self.get_owner_room_for_command(
            ctx
        )


        if not room:

            return



        channel = ctx.guild.get_channel(
            room["channel_id"]
        )



        if member.voice and member.voice.channel == channel:


            await member.move_to(
                None
            )


            await ctx.send(
                f"👢 {member.mention} удалён."
            )



    # ==================================================
    # BAN
    # ==================================================


    @commands.command(
        name="vban"
    )
    async def ban(
        self,
        ctx,
        member:discord.Member
    ):


        room = self.get_owner_room_for_command(
            ctx
        )


        if not room:

            return



        database.execute(
            """
            INSERT INTO voice_bans

            (
                channel_id,
                user_id
            )

            VALUES (?,?)

            """,
            (
                room["channel_id"],
                member.id
            )
        )


        await ctx.send(
            f"🚫 {member.mention} заблокирован."
        )



    # ==================================================
    # UNBAN
    # ==================================================


    @commands.command(
        name="vunban"
    )
    async def unban(
        self,
        ctx,
        member:discord.Member
    ):


        room = self.get_owner_room_for_command(
            ctx
        )


        if not room:

            return



        database.execute(
            """
            DELETE FROM voice_bans

            WHERE channel_id = ?

            AND user_id = ?

            """,
            (
                room["channel_id"],
                member.id
            )
        )


        await ctx.send(
            "✅ Пользователь разблокирован."
        )



async def setup(bot):

    print("✅ VOICE COG LOADED")

    await bot.add_cog(
        VoiceSystem(bot)
    )