from discord.ext import commands

from managers.player_manager import player_manager
from managers.rank_manager import rank_manager
from utils.logger import logger


class LevelSystem(commands.Cog):

    def __init__(self, bot):

        self.bot = bot



    @commands.Cog.listener()
    async def on_message(
        self,
        message
    ):

        # Игнорируем ботов
        if message.author.bot:
            return


        user_id = message.author.id
        username = message.author.name



        # Получаем игрока

        player = player_manager.get_player(
            user_id
        )


        # Если игрока нет - создаём

        if not player:

            player_manager.create_player(
                user_id,
                username
            )


            player = player_manager.get_player(
                user_id
            )



        old_level = player["level"]


        old_rank = rank_manager.get_rank(
            old_level
        )



        # Добавляем XP

        player_manager.add_xp(
            user_id,
            10
        )



        # Добавляем сообщение в статистику

        player_manager.add_message(
            user_id
        )



        # Получаем обновлённые данные

        updated_player = player_manager.get_player(
            user_id
        )


        new_level = updated_player["level"]


        new_rank = rank_manager.get_rank(
            new_level
        )



        # ==============================
        # LEVEL UP
        # ==============================

        if new_level > old_level:


            await message.channel.send(
                f"🎉 {message.author.mention} повысил уровень!\n"
                f"⭐ Новый уровень: `{new_level}`"
            )



        # ==============================
        # RANK UP
        # ==============================

        if new_rank != old_rank:


            max_hp = rank_manager.get_max_hp(
                new_rank
            )


            await rank_manager.update_rank(
                message.author,
                new_level
            )


            await message.channel.send(
                f"🏆 {message.author.mention} получил новый ранг!\n"
                f"⚔ Ранг: `{new_rank}`\n"
                f"❤️ Максимальный HP: `{max_hp}`"
            )



        logger.info(
            f"{username}: +10 XP"
        )



async def setup(bot):

    print("✅ LEVEL COG LOADED")

    await bot.add_cog(
        LevelSystem(bot)
    )