import discord

from utils.logger import logger


class RankManager:


    # ==================================================
    # RANKS
    # ==================================================

    RANKS = {

        "🌱 Rookie": {
            "level": 1,
            "max_hp": 500
        },

        "🕹 Player": {
            "level": 2,
            "max_hp": 1000
        },

        "🎮 Gamer": {
            "level": 5,
            "max_hp": 2000
        },

        "⚔ Veteran": {
            "level": 10,
            "max_hp": 4000
        },

        "💎 Elite": {
            "level": 20,
            "max_hp": 6000
        },

        "🔥 Pro Player": {
            "level": 35,
            "max_hp": 8000
        },

        "👑 Legend": {
            "level": 50,
            "max_hp": 10000
        }

    }



    # ==================================================
    # GET RANK
    # ==================================================

    def get_rank(
        self,
        level: int
    ):

        current_rank = "🌱 Rookie"


        for rank, data in self.RANKS.items():

            if level >= data["level"]:

                current_rank = rank


        return current_rank



    # ==================================================
    # GET MAX HP
    # ==================================================

    def get_max_hp(
        self,
        rank: str
    ):

        data = self.RANKS.get(
            rank
        )


        if not data:

            return 500


        return data["max_hp"]



    # ==================================================
    # CHECK RANK UP
    # ==================================================

    def check_rank_up(
        self,
        old_level: int,
        new_level: int
    ):


        old_rank = self.get_rank(
            old_level
        )


        new_rank = self.get_rank(
            new_level
        )


        if old_rank != new_rank:

            logger.info(
                f"Rank up: {old_rank} -> {new_rank}"
            )

            return new_rank


        return False



    # ==================================================
    # GIVE DISCORD ROLE
    # ==================================================

    async def update_rank(
        self,
        member,
        level: int
    ):


        new_rank = self.get_rank(
            level
        )


        guild = member.guild


        role = discord.utils.get(
            guild.roles,
            name=new_rank
        )


        if not role:

            logger.warning(
                f"Role not found: {new_rank}"
            )

            return False



        # Удаляем старые RPG роли

        for rank_name in self.RANKS.keys():

            old_role = discord.utils.get(
                guild.roles,
                name=rank_name
            )


            if old_role and old_role in member.roles:

                await member.remove_roles(
                    old_role
                )



        # Добавляем новую роль

        await member.add_roles(
            role
        )


        logger.info(
            f"{member.name} received rank role: {new_rank}"
        )


        return new_rank



rank_manager = RankManager()