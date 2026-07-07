import discord

from discord.ext import commands

from managers.inventory_manager import inventory_manager
from managers.player_manager import player_manager



class Inventory(commands.Cog):


    def __init__(self, bot):

        self.bot = bot



    # ==================================================
    # INVENTORY COMMAND
    # ==================================================

    @commands.command(
        name="inventory",
        aliases=["inv"]
    )
    async def inventory(
        self,
        ctx
    ):


        user_id = ctx.author.id



        # Проверяем игрока

        player = player_manager.get_player(
            user_id
        )


        if not player:

            player_manager.create_player(
                user_id,
                ctx.author.name
            )



        items = inventory_manager.get_inventory(
            user_id
        )



        embed = discord.Embed(
            title="🎒 Inventory",
            color=discord.Color.dark_purple()
        )



        if not items:


            embed.add_field(
                name="📦 Empty",
                value="Инвентарь пуст",
                inline=False
            )


        else:


            text = ""


            for item in items:

                text += (
                    f"🎁 `{item['item_id']}` "
                    f"x{item['quantity']}\n"
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



async def setup(bot):

    print("✅ INVENTORY COG LOADED")


    await bot.add_cog(
        Inventory(bot)
    )