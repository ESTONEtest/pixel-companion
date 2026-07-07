import random

from discord.ext import commands

from managers.inventory_manager import inventory_manager
from managers.item_manager import item_manager
from managers.player_manager import player_manager
from utils.logger import logger



class LootSystem(commands.Cog):


    def __init__(self, bot):

        self.bot = bot



    # ==================================================
    # LOOT CHANCE
    # ==================================================

    @commands.Cog.listener()
    async def on_message(
        self,
        message
    ):


        if message.author.bot:

            return



        user_id = message.author.id



        player = player_manager.get_player(
            user_id
        )


        if not player:

            player_manager.create_player(
                user_id,
                message.author.name
            )



        # 5% шанс найти предмет

        chance = random.randint(
            1,
            100
        )



        if chance > 5:

            return



        loot_table = [

            "crystal",
            "wooden_sword",
            "leather_armor"

        ]



        item_id = random.choice(
            loot_table
        )



        inventory_manager.add_item(
            user_id,
            item_id,
            1
        )



        item = item_manager.get_item(
            item_id
        )



        await message.channel.send(
            f"🎁 {message.author.mention} нашёл предмет!\n"
            f"{item['name']} x1"
        )



        logger.info(
            f"Loot drop: {message.author.name} -> {item_id}"
        )



async def setup(bot):

    print("✅ LOOT COG LOADED")

    await bot.add_cog(
        LootSystem(bot)
    )