import os

import discord

from discord.ext import commands

from systems.wishes_manager import WishesManager


manager = WishesManager()


# Канал для пожеланий
WISH_CHANNEL_ID = 1526072572817444964



class Wishes(commands.Cog):

    def __init__(self, bot):

        self.bot = bot



    # ==================================================
    # GIVE WISH
    # ==================================================

    @commands.command(
        name="wish",
        aliases=[
            "wishes",
            "пожелание"
        ]
    )
    async def wish(
        self,
        ctx
    ):


        result = manager.give_wish(
            ctx.author.id
        )


        if not result["success"]:


            minutes = result["cooldown"] // 60


            embed = discord.Embed(

                title="⏳ Пожелание отдыхает",

                description=(

                    "Ты уже получил пожелание.\n\n"

                    f"Попробуй снова через **{minutes} мин.**"

                ),

                color=0x555555

            )


            await ctx.send(
                embed=embed
            )

            return




        data = result["wish"]



        rarity = data.get(
            "rarity_name",
            "⚪ Обычное"
        )



        embed = discord.Embed(

            title="✨ Новое пожелание",

            description=f"**{data['text']}**",

            color=0x9b59b6

        )



        embed.add_field(

            name="📁 Категория",

            value=data.get(

                "category_name",

                data["category"]

            ),

            inline=True

        )



        embed.add_field(

            name="🎲 Редкость",

            value=rarity,

            inline=True

        )



        embed.set_author(

            name=ctx.author.display_name,

            icon_url=ctx.author.display_avatar.url

        )



        embed.set_footer(

            text="Pixel Companion ✨"

        )



        image_path = os.path.join(

            "assets",

            "wishes",

            data["image"]

        )



        file = None



        if os.path.exists(
            image_path
        ):


            file = discord.File(

                image_path,

                filename=data["image"]

            )


            embed.set_image(

                url=f"attachment://{data['image']}"

            )




        channel = self.bot.get_channel(

            WISH_CHANNEL_ID

        )



        if channel is None:


            await ctx.send(

                "❌ Канал пожеланий не найден."

            )

            return




        if file:


            await channel.send(

                embed=embed,

                file=file

            )


        else:


            await channel.send(

                embed=embed

            )




        await ctx.message.add_reaction(

            "✨"

        )





    # ==================================================
    # LIST
    # ==================================================

    @commands.command(
        name="wishlist"
    )
    @commands.has_permissions(
        administrator=True
    )
    async def wish_list(
        self,
        ctx
    ):


        text = ""



        for name, data in manager.categories.items():


            rarity = manager.get_rarity_info(

                data.get(

                    "rarity",

                    "common"

                )

            )


            text += (

                f"📁 **{manager.get_category_name(name)}**\n"

                f"💬 Пожеланий: **{len(data['wishes'])}**\n"

                f"🎲 Редкость: {rarity.get('name','⚪ Обычное')}\n"

                f"🖼 {data['image']}\n\n"

            )




        embed = discord.Embed(

            title="📜 Категории пожеланий",

            description=(

                text or "Нет категорий"

            ),

            color=0x3498db

        )



        embed.add_field(

            name="Всего пожеланий",

            value=str(

                manager.get_total_wishes()

            )

        )



        await ctx.send(

            embed=embed

        )





    # ==================================================
    # RELOAD
    # ==================================================

    @commands.command(
        name="wishreload"
    )
    @commands.has_permissions(
        administrator=True
    )
    async def wish_reload(
        self,
        ctx
    ):


        manager.load_wishes()



        embed = discord.Embed(

            title="🔄 Пожелания обновлены",

            description=(

                f"Категорий: **{len(manager.categories)}**\n"

                f"Пожеланий: **{manager.get_total_wishes()}**"

            ),

            color=0x2ecc71

        )



        await ctx.send(

            embed=embed

        )





    # ==================================================
    # STATS
    # ==================================================

    @commands.command(
        name="wishstats"
    )
    async def wish_stats(
        self,
        ctx
    ):


        stats = manager.get_user_stats(

            ctx.author.id

        )



        embed = discord.Embed(

            title="📊 Статистика пожеланий",

            color=0xf1c40f

        )



        embed.add_field(

            name="✨ Получено",

            value=f"{stats['count']} раз"

        )



        if stats["last_wish"]:


            embed.add_field(

                name="Последнее",

                value=stats["last_wish"]["text"],

                inline=False

            )



        await ctx.send(

            embed=embed

        )





    # ==================================================
    # INFO
    # ==================================================

    @commands.command(
        name="wishinfo"
    )
    async def wish_info(
        self,
        ctx
    ):


        embed = discord.Embed(

            title="✨ Система пожеланий",

            description=(

                "`!wish` — получить пожелание\n"

                "`!wishstats` — статистика\n"

                "`!wishlist` — категории\n"

                "`!wishreload` — обновить JSON"

            ),

            color=0x8e44ad

        )



        embed.add_field(

            name="📁 Категории",

            value=str(

                len(manager.categories)

            )

        )



        embed.add_field(

            name="💬 Пожеланий",

            value=str(

                manager.get_total_wishes()

            )

        )



        await ctx.send(

            embed=embed

        )





# ==================================================
# SETUP
# ==================================================

async def setup(bot):

    await bot.add_cog(
        Wishes(bot)
    )