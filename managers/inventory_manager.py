from managers.database import database
from utils.logger import logger


class InventoryManager:


    # ==================================================
    # ADD ITEM
    # ==================================================

    def add_item(
        self,
        user_id: int,
        item_id: str,
        quantity: int = 1
    ):


        existing = database.fetchone(
            """
            SELECT *
            FROM inventory
            WHERE user_id = ?
            AND item_id = ?
            """,
            (
                user_id,
                item_id
            )
        )


        if existing:

            database.execute(
                """
                UPDATE inventory
                SET quantity = quantity + ?
                WHERE user_id = ?
                AND item_id = ?
                """,
                (
                    quantity,
                    user_id,
                    item_id
                )
            )


        else:

            database.execute(
                """
                INSERT INTO inventory
                (
                    user_id,
                    item_id,
                    quantity
                )
                VALUES (?, ?, ?)
                """,
                (
                    user_id,
                    item_id,
                    quantity
                )
            )


        logger.info(
            f"Item added: {item_id} x{quantity} to {user_id}"
        )


        return True



    # ==================================================
    # REMOVE ITEM
    # ==================================================

    def remove_item(
        self,
        user_id: int,
        item_id: str,
        quantity: int = 1
    ):


        item = database.fetchone(
            """
            SELECT *
            FROM inventory
            WHERE user_id = ?
            AND item_id = ?
            """,
            (
                user_id,
                item_id
            )
        )


        if not item:

            return False



        new_quantity = item["quantity"] - quantity



        if new_quantity <= 0:


            database.execute(
                """
                DELETE FROM inventory
                WHERE user_id = ?
                AND item_id = ?
                """,
                (
                    user_id,
                    item_id
                )
            )


        else:


            database.execute(
                """
                UPDATE inventory
                SET quantity = ?
                WHERE user_id = ?
                AND item_id = ?
                """,
                (
                    new_quantity,
                    user_id,
                    item_id
                )
            )


        return True



    # ==================================================
    # GET INVENTORY
    # ==================================================

    def get_inventory(
        self,
        user_id: int
    ):


        return database.fetchall(
            """
            SELECT *
            FROM inventory
            WHERE user_id = ?
            """,
            (
                user_id,
            )
        )



    # ==================================================
    # CLEAR INVENTORY
    # ==================================================

    def clear_inventory(
        self,
        user_id: int
    ):


        database.execute(
            """
            DELETE FROM inventory
            WHERE user_id = ?
            """,
            (
                user_id,
            )
        )


        logger.info(
            f"Inventory cleared: {user_id}"
        )



inventory_manager = InventoryManager()