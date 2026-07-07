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
                    f"💰 Цена: `{data['price']}` coins\n\n"
                )



        embed.add_field(
            name="Items",
            value=text,
            inline=False
        )


        embed.set_footer(
            text="Pixel Companion RPG v2.0"
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
        item_id: str
    ):


        user_id = ctx.author.id



        player = player_manager.get_player(
            user_id
        )


        if not player:

            player_manager.create_player(
                user_id,
                ctx.author.name
            )



        item = item_manager.get_item(
            item_id
        )


        if not item:

            await ctx.send(
                "❌ Такого предмета нет"
            )

            return



        result = shop_manager.buy_item(
            user_id,
            item_id
        )


        if not result:

            await ctx.send(
                "❌ Недостаточно монет"
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


        await ctx.send(
            f"🛒 {ctx.author.mention} купил:\n"
            f"{item['name']}\n"
            f"💰 Потрачено: `{price}` coins\n"
            f"💰 Осталось: `{updated_player['coins']}` coins"
        )



async def setup(bot):

    print("✅ SHOP COG LOADED")

    await bot.add_cog(
        Shop(bot)
    )