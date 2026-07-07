from managers.database import database
from cogs.level_manager import level_manager
from managers.rank_manager import rank_manager
from utils.logger import logger


class PlayerManager:

    # ==================================================
    # CREATE PLAYER
    # ==================================================

    def create_player(
        self,
        user_id: int,
        username: str
    ):

        if database.user_exists(user_id):
            return False

        database.create_user(
            user_id,
            username
        )

        logger.info(
            f"New player created: {username}"
        )

        return True

    # ==================================================
    # GET PLAYER
    # ==================================================

    def get_player(
        self,
        user_id: int
    ):

        return database.get_user(
            user_id
        )

    # ==================================================
    # XP
    # ==================================================

    def add_xp(
        self,
        user_id: int,
        amount: int
    ):

        player = self.get_player(
            user_id
        )

        if not player:
            return False

        new_xp = player["xp"] + amount

        database.execute(
            """
            UPDATE users
            SET xp = ?
            WHERE user_id = ?
            """,
            (
                new_xp,
                user_id
            )
        )

        self.update_level(
            user_id
        )

        return True

    # ==================================================
    # LEVEL + RANK CHECK
    # ==================================================

    def update_level(
        self,
        user_id: int
    ):

        player = self.get_player(
            user_id
        )

        if not player:
            return False

        old_level = player["level"]

        new_level = level_manager.get_level(
            player["xp"]
        )

        if new_level != old_level:

            database.execute(
                """
                UPDATE users
                SET level = ?
                WHERE user_id = ?
                """,
                (
                    new_level,
                    user_id
                )
            )

            logger.info(
                f"Player {user_id} level up: {old_level} -> {new_level}"
            )

            old_rank = rank_manager.get_rank(
                old_level
            )

            new_rank = rank_manager.get_rank(
                new_level
            )

            if old_rank != new_rank:

                logger.info(
                    f"Player {user_id} rank up: {old_rank} -> {new_rank}"
                )

            return new_level

        return False

    # ==================================================
    # SET LEVEL (TEST / ADMIN)
    # ==================================================

    def set_level(
        self,
        user_id: int,
        level: int
    ):

        player = self.get_player(
            user_id
        )

        if not player:
            return False

        xp = level_manager.get_xp_for_level(
            level
        )

        database.execute(
            """
            UPDATE users
            SET level = ?, xp = ?
            WHERE user_id = ?
            """,
            (
                level,
                xp,
                user_id
            )
        )

        logger.info(
            f"Player {user_id} level manually set to {level}"
        )

        return True

    # ==================================================
    # MESSAGES
    # ==================================================

    def add_message(
        self,
        user_id: int
    ):

        database.execute(
            """
            UPDATE statistics
            SET messages = messages + 1
            WHERE user_id = ?
            """,
            (
                user_id,
            )
        )

        return True

    # ==================================================
    # HP
    # ==================================================

    def add_hp(
        self,
        user_id: int,
        amount: int
    ):

        player = self.get_player(
            user_id
        )

        if not player:
            return False

        max_hp = player["max_hp"]

        new_hp = max(
            0,
            min(
                player["hp"] + amount,
                max_hp
            )
        )

        database.execute(
            """
            UPDATE users
            SET hp = ?
            WHERE user_id = ?
            """,
            (
                new_hp,
                user_id
            )
        )

        return True

    # ==================================================
    # SET HP
    # ==================================================

    def set_hp(
        self,
        user_id: int,
        hp: int
    ):

        player = self.get_player(
            user_id
        )

        if not player:
            return False

        max_hp = player["max_hp"]

        new_hp = max(
            0,
            min(
                hp,
                max_hp
            )
        )

        database.execute(
            """
            UPDATE users
            SET hp = ?
            WHERE user_id = ?
            """,
            (
                new_hp,
                user_id
            )
        )

        return True

    # ==================================================
    # COINS
    # ==================================================

    def add_coins(
        self,
        user_id: int,
        amount: int
    ):

        player = self.get_player(
            user_id
        )

        if not player:
            return False

        new_coins = player["coins"] + amount

        database.execute(
            """
            UPDATE users
            SET coins = ?
            WHERE user_id = ?
            """,
            (
                new_coins,
                user_id
            )
        )

        return True

    # ==================================================
    # STATISTICS
    # ==================================================

    def get_statistics(
        self,
        user_id: int
    ):

        return database.fetchone(
            """
            SELECT *
            FROM statistics
            WHERE user_id = ?
            """,
            (
                user_id,
            )
        )

    def add_monster_kill(
        self,
        user_id: int
    ):

        database.execute(
            """
            UPDATE statistics
            SET monsters_killed = monsters_killed + 1
            WHERE user_id = ?
            """,
            (
                user_id,
            )
        )

        return True


player_manager = PlayerManager()