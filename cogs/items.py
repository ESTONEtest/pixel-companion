import discord

from discord.ext import commands

from managers.inventory_manager import inventory_manager
from managers.item_manager import item_manager
from managers.player_manager import player_manager



class Items(commands.Cog):


    def __init__(self, bot):

        self.bot = bot



    # ==================================================
    # GIVE ITEM
    # ==================================================

    @commands.command(name="giveitem")
    @commands.has_permissions(administrator=True)
    async def give_item(
        self,
        ctx,
        member: discord.Member,
        item_id: str,
        amount: int = 1
    ):


        if not item_manager.exists(
            item_id
        ):

            await ctx.send(
                "❌ Такого предмета нет!"
            )

            return



        player = player_manager.get_player(
            member.id
        )


        if not player:

            player_manager.create_player(
                member.id,
                member.name
            )



        inventory_manager.add_item(
            member.id,
            item_id,
            amount
        )


        item = item_manager.get_item(
            item_id
        )



        await ctx.send(
            f"🎁 {member.mention} получил "
            f"`{item['name']}` x`{amount}`"
        )



    # ==================================================
    # REMOVE ITEM
    # ==================================================

    @commands.command(name="removeitem")
    @commands.has_permissions(administrator=True)
    async def remove_item(
        self,
        ctx,
        member: discord.Member,
        item_id: str,
        amount: int = 1
    ):


        result = inventory_manager.remove_item(
            member.id,
            item_id,
            amount
        )


        if result:

            await ctx.send(
                "🗑 Предмет удалён"
            )

        else:

            await ctx.send(
                "❌ У игрока нет этого предмета"
            )



async def setup(bot):

    print("✅ ITEMS COG LOADED")


    await bot.add_cog(
        Items(bot)
    )