from datetime import datetime, timedelta

from managers.database import database



class CooldownManager:



    # ==================================================
    # CHECK DAILY
    # ==================================================

    def check_daily(
        self,
        user_id: int
    ):


        data = database.fetchone(
            """
            SELECT daily
            FROM cooldowns
            WHERE user_id = ?
            """,
            (
                user_id,
            )
        )


        if not data or not data["daily"]:

            return True



        last = datetime.fromisoformat(
            data["daily"]
        )


        if datetime.now() >= last + timedelta(hours=24):

            return True



        return False



    # ==================================================
    # SET DAILY
    # ==================================================

    def set_daily(
        self,
        user_id: int
    ):


        database.execute(
            """
            UPDATE cooldowns
            SET daily = ?
            WHERE user_id = ?
            """,
            (
                datetime.now().isoformat(),
                user_id
            )
        )



cooldown_manager = CooldownManager()