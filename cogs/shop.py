import discord

from discord.ext import commands

from managers.shop_manager import shop_manager
from managers.item_manager import item_manager
from managers.inventory_manager import inventory_manager
from managers.player_manager import player_manager


class Shop(commands.Cog):

    def __init__(self, bot):

        self.bot = bot

    # ==================================================
    # SHOP
    # ==================================================

    @commands.command(name="shop")
    async def shop(
        self,
        ctx
    ):

        embed = discord.Embed(
            title="🛒 Pixel Shop",
            color=discord.Color.gold()
        )

        text = ""

        for item_id, data in shop_manager.get_shop().items():

            item = item_manager.get_item(
                item_id
            )

            if item:

                text += (
                    f"{item['name']}\n"
                    f"ID: `{item_id}`\n"
                    f"💰 Цена: `{data['price']}` coins\n\n"
                )

        if not text:

            text = "Магазин пока пуст."

        embed.add_field(
            name="Items",
            value=text,
            inline=False
        )

        embed.set_footer(
            text="Покупка: .buy item_id"
        )

        await ctx.send(
            embed=embed
        )

    # ==================================================
    # BUY
    # ==================================================

    @commands.command(name="buy")
    async def buy(
        self,
        ctx,
        item_id: str = None
    ):

        if not item_id:

            await ctx.send(
                "❌ Укажите предмет. Пример: `.buy potion`"
            )

            return

        user_id = ctx.author.id

        player = player_manager.get_player(
            user_id
        )

        if not player:

            player_manager.create_player(
                user_id,
                ctx.author.name
            )

            player = player_manager.get_player(
                user_id
            )

        if not player:

            await ctx.send(
                "❌ Не удалось создать персонажа. Попробуйте еще раз."
            )

            return

        item = item_manager.get_item(
            item_id
        )

        if not item:

            await ctx.send(
                "❌ Такого предмета нет."
            )

            return

        result = shop_manager.buy_item(
            user_id,
            item_id
        )

        if not result:

            await ctx.send(
                "❌ Недостаточно монет."
            )

            return

        inventory_manager.add_item(
            user_id,
            item_id,
            1
        )

        price = shop_manager.get_price(
            item_id
        )

        updated_player = player_manager.get_player(
            user_id
        )

        embed = discord.Embed(
            title="🛒 Покупка",
            description=f"{ctx.author.mention} купил предмет.",
            color=discord.Color.gold()
        )

        embed.add_field(
            name="🎁 Предмет",
            value=item["name"],
            inline=False
        )

        embed.add_field(
            name="💰 Потрачено",
            value=f"`{price}` coins",
            inline=True
        )

        embed.add_field(
            name="💰 Осталось",
            value=f"`{updated_player['coins']}` coins",
            inline=True
        )

        await ctx.send(
            embed=embed
        )


async def setup(bot):

    print("✅ SHOP COG LOADED")

    await bot.add_cog(
        Shop(bot)
    )