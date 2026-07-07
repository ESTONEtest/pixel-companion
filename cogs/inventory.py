import discord

from discord.ext import commands

from managers.inventory_manager import inventory_manager
from managers.player_manager import player_manager
from managers.item_manager import item_manager

from systems.healing import healing_system


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

        items = inventory_manager.get_inventory(
            user_id
        )

        embed = discord.Embed(
            title="🎒 Инвентарь",
            color=discord.Color.dark_purple()
        )

        if not items:

            embed.add_field(
                name="📦 Пусто",
                value="Инвентарь пуст.",
                inline=False
            )

        else:

            text = ""

            for item in items:

                item_data = item_manager.get_item(
                    item["item_id"]
                )

                item_name = item["item_id"]

                if item_data:

                    item_name = item_data["name"]

                text += (
                    f"{item_name} "
                    f"`x{item['quantity']}`\n"
                )

            embed.add_field(
                name="Предметы",
                value=text,
                inline=False
            )

        embed.set_footer(
            text="Использовать предмет: .use potion"
        )

        await ctx.send(
            embed=embed
        )

    # ==================================================
    # USE ITEM
    # ==================================================

    @commands.command(
        name="use"
    )
    async def use_item(
        self,
        ctx,
        item_id: str = None
    ):

        if not item_id:

            await ctx.send(
                "❌ Укажите предмет. Пример: `.use potion`"
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

        item = item_manager.get_item(
            item_id
        )

        if not item:

            await ctx.send(
                "❌ Такого предмета нет."
            )

            return

        inventory = inventory_manager.get_inventory(
            user_id
        )

        has_item = False

        for inventory_item in inventory:

            if inventory_item["item_id"] == item_id and inventory_item["quantity"] > 0:

                has_item = True

                break

        if not has_item:

            await ctx.send(
                "❌ У вас нет этого предмета."
            )

            return

        if item["type"] == "consumable":

            if item_id == "potion":

                if player["hp"] >= player["max_hp"]:

                    await ctx.send(
                        "❤️ Ваше здоровье уже полностью восстановлено."
                    )

                    return

                new_hp = healing_system.heal(
                    current_hp=player["hp"],
                    amount=item["heal"],
                    max_hp=player["max_hp"]
                )

                healed = new_hp - player["hp"]

                player_manager.set_hp(
                    user_id,
                    new_hp
                )

                inventory_manager.remove_item(
                    user_id,
                    item_id,
                    1
                )

                embed = discord.Embed(
                    title="🧪 Зелье использовано",
                    description=f"Вы восстановили **{healed} HP**.",
                    color=discord.Color.green()
                )

                embed.add_field(
                    name="❤️ HP",
                    value=f"`{new_hp} / {player['max_hp']}`",
                    inline=False
                )

                await ctx.send(
                    embed=embed
                )

                return

        await ctx.send(
            "❌ Этот предмет нельзя использовать."
        )


async def setup(bot):

    print("✅ INVENTORY COG LOADED")

    await bot.add_cog(
        Inventory(bot)
    )