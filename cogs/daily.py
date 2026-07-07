import random

from discord.ext import commands

from managers.cooldown_manager import cooldown_manager
from managers.player_manager import player_manager
from managers.inventory_manager import inventory_manager



class Daily(commands.Cog):


    def __init__(self, bot):

        self.bot = bot



    # ==================================================
    # DAILY REWARD
    # ==================================================

    @commands.command(name="daily")
    async def daily(
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



        # Проверяем кулдаун

        if not cooldown_manager.check_daily(
            user_id
        ):


            await ctx.send(
                "⏳ Ты уже получил награду сегодня!"
            )

            return



        # Награды

        coins = random.randint(
            100,
            250
        )


        xp = 20



        player_manager.add_coins(
            user_id,
            coins
        )


        player_manager.add_xp(
            user_id,
            xp
        )



        # 25% шанс кристалла

        loot_text = ""


        if random.randint(
            1,
            100
        ) <= 25:


            inventory_manager.add_item(
                user_id,
                "crystal",
                1
            )


            loot_text = "\n💎 Crystal x1"



        cooldown_manager.set_daily(
            user_id
        )



        await ctx.send(
            f"🎁 {ctx.author.mention} получил Daily Reward!\n\n"
            f"💰 +{coins} coins\n"
            f"✨ +{xp} XP"
            f"{loot_text}"
        )



async def setup(bot):

    print("✅ DAILY COG LOADED")

    await bot.add_cog(
        Daily(bot)
    )