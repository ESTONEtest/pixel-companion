from database.database import database


class DatabaseManager:
    """
    Менеджер работы с базой данных.
    """

    async def create_user(self, user_id: int):

        async with await database.connect() as db:

            await db.execute(
                """
                INSERT OR IGNORE INTO users(user_id)
                VALUES(?)
                """,
                (user_id,)
            )

            await db.commit()

    async def user_exists(self, user_id: int) -> bool:

        async with await database.connect() as db:

            cursor = await db.execute(
                """
                SELECT user_id
                FROM users
                WHERE user_id = ?
                """,
                (user_id,)
            )

            row = await cursor.fetchone()

            return row is not None

    async def get_user(self, user_id: int):

        await self.create_user(user_id)

        async with await database.connect() as db:

            cursor = await db.execute(
                """
                SELECT *
                FROM users
                WHERE user_id = ?
                """,
                (user_id,)
            )

            return await cursor.fetchone()

                # ==========================================
    # Баланс
    # ==========================================

    async def get_balance(self, user_id: int) -> int:

        await self.create_user(user_id)

        async with await database.connect() as db:

            cursor = await db.execute(
                """
                SELECT balance
                FROM users
                WHERE user_id = ?
                """,
                (user_id,)
            )

            row = await cursor.fetchone()

            return row[0]

    async def add_money(self, user_id: int, amount: int):

        await self.create_user(user_id)

        async with await database.connect() as db:

            await db.execute(
                """
                UPDATE users
                SET balance = balance + ?
                WHERE user_id = ?
                """,
                (amount, user_id)
            )

            await db.commit()

    async def remove_money(self, user_id: int, amount: int):

        await self.create_user(user_id)

        async with await database.connect() as db:

            await db.execute(
                """
                UPDATE users
                SET balance = MAX(balance - ?, 0)
                WHERE user_id = ?
                """,
                (amount, user_id)
            )

            await db.commit()

    async def set_balance(self, user_id: int, amount: int):

        await self.create_user(user_id)

        async with await database.connect() as db:

            await db.execute(
                """
                UPDATE users
                SET balance = ?
                WHERE user_id = ?
                """,
                (amount, user_id)
            )

            await db.commit()

                # ==========================================
    # XP и уровень
    # ==========================================

    async def get_level(self, user_id: int) -> int:

        await self.create_user(user_id)

        async with await database.connect() as db:

            cursor = await db.execute(
                """
                SELECT level
                FROM users
                WHERE user_id = ?
                """,
                (user_id,)
            )

            row = await cursor.fetchone()

            return row[0]

    async def get_xp(self, user_id: int) -> int:

        await self.create_user(user_id)

        async with await database.connect() as db:

            cursor = await db.execute(
                """
                SELECT xp
                FROM users
                WHERE user_id = ?
                """,
                (user_id,)
            )

            row = await cursor.fetchone()

            return row[0]

    async def add_xp(self, user_id: int, amount: int):

        await self.create_user(user_id)

        async with await database.connect() as db:

            cursor = await db.execute(
                """
                SELECT xp, level
                FROM users
                WHERE user_id = ?
                """,
                (user_id,)
            )

            xp, level = await cursor.fetchone()

            xp += amount

            while xp >= (level * level * 100):
                xp -= (level * level * 100)
                level += 1

            await db.execute(
                """
                UPDATE users
                SET xp = ?, level = ?
                WHERE user_id = ?
                """,
                (xp, level, user_id)
            )

            await db.commit()

            return level
               
                # ==========================================
    # Профиль
    # ==========================================

    async def get_profile(self, user_id: int):

        await self.create_user(user_id)

        async with await database.connect() as db:

            cursor = await db.execute(
                """
                SELECT
                    level,
                    xp,
                    balance,
                    hp,
                    max_hp,
                    energy,
                    max_energy,
                    hunger,
                    max_hunger,
                    messages
                FROM users
                WHERE user_id = ?
                """,
                (user_id,)
            )

            row = await cursor.fetchone()

            if row is None:
                return None

            return {
                "level": row[0],
                "xp": row[1],
                "balance": row[2],
                "hp": row[3],
                "max_hp": row[4],
                "energy": row[5],
                "max_energy": row[6],
                "hunger": row[7],
                "max_hunger": row[8],
                "messages": row[9],
            }


# ==================================================
# Глобальный экземпляр менеджера
# ==================================================

manager = DatabaseManager()