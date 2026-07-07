import discord

from discord.ext import commands

from managers.equipment_manager import equipment_manager
from managers.inventory_manager import inventory_manager
from managers.item_manager import item_manager
from managers.player_manager import player_manager



class Equipment(commands.Cog):


    def __init__(self, bot):

        self.bot = bot



    # ==================================================
    # EQUIP ITEM
    # ==================================================

    @commands.command(name="equip")
    async def equip(
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



        # Проверяем наличие предмета

        inventory = inventory_manager.get_inventory(
            user_id
        )


        has_item = False


        for item in inventory:

            if item["item_id"] == item_id:

                has_item = True
                break



        if not has_item:

            await ctx.send(
                "❌ У тебя нет этого предмета в инвентаре"
            )

            return



        item = item_manager.get_item(
            item_id
        )



        if item["type"] not in [
            "weapon",
            "armor"
        ]:

            await ctx.send(
                "❌ Этот предмет нельзя экипировать"
            )

            return



        equipment_manager.equip_item(
            user_id,
            item_id
        )



        await ctx.send(
            f"⚔ {ctx.author.mention} экипировал:\n"
            f"{item['name']}"
        )



    # ==================================================
    # SHOW EQUIPMENT
    # ==================================================

    @commands.command(
        name="equipment",
        aliases=["eq"]
    )
    async def equipment(
        self,
        ctx
    ):


        user_id = ctx.author.id


        data = equipment_manager.get_equipment(
            user_id
        )



        embed = discord.Embed(
            title="⚔ Equipment",
            color=discord.Color.dark_purple()
        )



        if not data:

            embed.add_field(
                name="Empty",
                value="Экипировка отсутствует",
                inline=False
            )


        else:

            weapon = data["weapon"] or "Нет"
            armor = data["armor"] or "Нет"


            embed.add_field(
                name="🗡 Weapon",
                value=f"`{weapon}`",
                inline=True
            )


            embed.add_field(
                name="🛡 Armor",
                value=f"`{armor}`",
                inline=True
            )



        embed.set_footer(
            text="Pixel Companion RPG v2.0"
        )


        await ctx.send(
            embed=embed
        )



async def setup(bot):

    print("✅ EQUIPMENT COG LOADED")


    await bot.add_cog(
        Equipment(bot)
    )