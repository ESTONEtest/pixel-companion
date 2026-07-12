import discord

from discord.ext import commands
from discord.ui import Button, View


WELCOME_CHANNEL_ID = 1466499385411109090

ACCESS_CHANNEL_ID = 1466501867663130664

ACCESS_ROLE_ID = 1525832322598047764



# ==================================================
# ACCESS BUTTON
# ==================================================

class AccessControls(View):


    def __init__(self):

        super().__init__(
            timeout=None
        )



    @discord.ui.button(
        label="ОТКРЫТЬ ДОСТУП",
        emoji="🔓",
        style=discord.ButtonStyle.success,
        custom_id="pixel_companion:open_access"
    )
    async def open_access(
        self,
        interaction: discord.Interaction,
        button: Button
    ):


        if interaction.guild is None:

            return



        member = interaction.guild.get_member(
            interaction.user.id
        )


        if member is None:

            await interaction.response.send_message(
                "❌ Игрок не найден в системе сервера.",
                ephemeral=True
            )

            return



        role = interaction.guild.get_role(
            ACCESS_ROLE_ID
        )


        if role is None:

            await interaction.response.send_message(
                "❌ Роль доступа не найдена.",
                ephemeral=True
            )

            return



        if role in member.roles:

            await interaction.response.send_message(
                "📼 Доступ уже активирован. Все системы открыты.",
                ephemeral=True
            )

            return



        try:

            await member.add_roles(
                role,
                reason="Pixel Companion: доступ выдан кнопкой"
            )



        except discord.Forbidden:

            await interaction.response.send_message(
                "❌ Боту не хватает права на выдачу роли.",
                ephemeral=True
            )

            return



        await interaction.response.send_message(

            "✅ **ДОСТУП ОТКРЫТ**\n\n"
            "```"
            "STATUS: PLAYER VERIFIED\n"
            "CHAT MODULES: ONLINE\n"
            "```",

            ephemeral=True

        )



# ==================================================
# WELCOME
# ==================================================

class Welcome(commands.Cog):


    def __init__(self, bot):

        self.bot = bot



    async def cog_load(self):

        # Кнопка продолжит работать даже после перезапуска бота
        self.bot.add_view(
            AccessControls()
        )



    # ==================================================
    # ACCESS PANEL
    # ==================================================

    async def send_access_panel(self):


        channel = self.bot.get_channel(
            ACCESS_CHANNEL_ID
        )


        if not channel:

            return



        # Не создаём вторую такую же панель после перезапуска
        async for message in channel.history(limit=50):


            if message.author != self.bot.user:

                continue



            for row in message.components:


                for component in row.children:


                    if component.custom_id == "pixel_companion:open_access":

                        return



        embed = discord.Embed(

            title="📼 PIXEL COMPANION // ACCESS TERMINAL",

            description=(

                "```"
                "SYSTEM BOOT: COMPLETE\n"
                "ACCESS TERMINAL: ONLINE"
                "```\n\n"

                "👾 Вас приветствует **Pixel Companion**.\n\n"

                "📜 Надеемся, ты уже прочитал правила станции.\n\n"

                "🔓 Нажми кнопку ниже, чтобы система "
                "загрузила полный доступ к чатам и модулям сервера.\n\n"

                "```"
                "STATUS: WAITING FOR PLAYER"
                "```"

            ),

            color=discord.Color.dark_purple()

        )



        embed.set_footer(

            text="Pixel Companion RPG • Access System"

        )



        await channel.send(

            embed=embed,

            view=AccessControls()

        )



    # ==================================================
    # BOT READY
    # ==================================================

    @commands.Cog.listener()
    async def on_ready(self):

        await self.send_access_panel()



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
                "👾 сражайся с монстрами,\n"
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