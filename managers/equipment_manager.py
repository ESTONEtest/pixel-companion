from managers.database import database
from managers.item_manager import item_manager
from utils.logger import logger


class EquipmentManager:

    # ==================================================
    # EQUIP ITEM
    # ==================================================

    def equip_item(
        self,
        user_id: int,
        item_id: str
    ):

        item = item_manager.get_item(item_id)

        if not item:
            return False

        equipment = database.fetchone(
            """
            SELECT *
            FROM equipment
            WHERE user_id = ?
            """,
            (user_id,)
        )

        if not equipment:

            database.execute(
                """
                INSERT INTO equipment(user_id)
                VALUES(?)
                """,
                (user_id,)
            )

        slot = item["type"]

        if slot == "weapon":

            database.execute(
                """
                UPDATE equipment
                SET weapon = ?
                WHERE user_id = ?
                """,
                (
                    item_id,
                    user_id
                )
            )

        elif slot == "armor":

            database.execute(
                """
                UPDATE equipment
                SET armor = ?
                WHERE user_id = ?
                """,
                (
                    item_id,
                    user_id
                )
            )

        else:
            return False

        self.update_stats(user_id)

        logger.info(
            f"{user_id} equipped {item_id}"
        )

        return True

    # ==================================================
    # UPDATE STATS
    # ==================================================

    def update_stats(
        self,
        user_id: int
    ):

        equipment = database.fetchone(
            """
            SELECT *
            FROM equipment
            WHERE user_id = ?
            """,
            (user_id,)
        )

        attack = 5
        defense = 5
        luck = 1

        if equipment["weapon"]:

            weapon = item_manager.get_item(
                equipment["weapon"]
            )

            if weapon:

                attack += weapon.get("attack", 0)
                defense += weapon.get("defense", 0)
                luck += weapon.get("luck", 0)

        if equipment["armor"]:

            armor = item_manager.get_item(
                equipment["armor"]
            )

            if armor:

                attack += armor.get("attack", 0)
                defense += armor.get("defense", 0)
                luck += armor.get("luck", 0)

        database.execute(
            """
            UPDATE users
            SET attack = ?,
                defense = ?,
                luck = ?
            WHERE user_id = ?
            """,
            (
                attack,
                defense,
                luck,
                user_id
            )
        )

        return True

    # ==================================================
    # GET EQUIPMENT
    # ==================================================

    def get_equipment(
        self,
        user_id: int
    ):

        return database.fetchone(
            """
            SELECT *
            FROM equipment
            WHERE user_id = ?
            """,
            (user_id,)
        )


equipment_manager = EquipmentManager()