import os
import sqlite3
from typing import Any

from config import DATABASE
from utils.logger import logger


class DatabaseManager:

    def __init__(self):

        os.makedirs(
            "database",
            exist_ok=True
        )

        self.connection = sqlite3.connect(
            DATABASE,
            check_same_thread=False
        )

        self.connection.row_factory = sqlite3.Row

        self.cursor = self.connection.cursor()

        logger.info(
            "Database connected successfully."
        )

        self.create_tables()

        self.migrate_users_table()

    # ==================================================
    # SQL
    # ==================================================

    def execute(
        self,
        query: str,
        params: tuple = ()
    ):

        self.cursor.execute(
            query,
            params
        )

        self.connection.commit()

    def fetchone(
        self,
        query: str,
        params: tuple = ()
    ) -> Any:

        self.cursor.execute(
            query,
            params
        )

        return self.cursor.fetchone()

    def fetchall(
        self,
        query: str,
        params: tuple = ()
    ):

        self.cursor.execute(
            query,
            params
        )

        return self.cursor.fetchall()

    # ==================================================
    # TABLE HELPERS
    # ==================================================

    def get_table_columns(
        self,
        table_name: str
    ):

        rows = self.fetchall(
            f"""
            PRAGMA table_info({table_name})
            """
        )

        return [
            row["name"]
            for row in rows
        ]

    def add_column_if_missing(
        self,
        table_name: str,
        column_name: str,
        column_sql: str
    ):

        columns = self.get_table_columns(
            table_name
        )

        if column_name in columns:
            return False

        self.execute(
            f"""
            ALTER TABLE {table_name}
            ADD COLUMN {column_sql}
            """
        )

        logger.info(
            f"Database migration: added {table_name}.{column_name}"
        )

        return True

    # ==================================================
    # MIGRATIONS
    # ==================================================

    def migrate_users_table(self):

        self.add_column_if_missing(
            "users",
            "level",
            "level INTEGER DEFAULT 1"
        )

        self.add_column_if_missing(
            "users",
            "xp",
            "xp INTEGER DEFAULT 0"
        )

        self.add_column_if_missing(
            "users",
            "hp",
            "hp INTEGER DEFAULT 100"
        )

        self.add_column_if_missing(
            "users",
            "max_hp",
            "max_hp INTEGER DEFAULT 100"
        )

        self.add_column_if_missing(
            "users",
            "coins",
            "coins INTEGER DEFAULT 500"
        )

        self.add_column_if_missing(
            "users",
            "gems",
            "gems INTEGER DEFAULT 0"
        )

        self.add_column_if_missing(
            "users",
            "attack",
            "attack INTEGER DEFAULT 5"
        )

        self.add_column_if_missing(
            "users",
            "defense",
            "defense INTEGER DEFAULT 5"
        )

        self.add_column_if_missing(
            "users",
            "luck",
            "luck INTEGER DEFAULT 1"
        )

    # ==================================================
    # TABLES
    # ==================================================

    def create_tables(self):

        logger.info(
            "Creating database tables..."
        )

        # ================= USERS =================

        self.execute("""
        CREATE TABLE IF NOT EXISTS users (

            user_id INTEGER PRIMARY KEY,

            username TEXT NOT NULL,

            level INTEGER DEFAULT 1,

            xp INTEGER DEFAULT 0,

            hp INTEGER DEFAULT 100,

            max_hp INTEGER DEFAULT 100,

            coins INTEGER DEFAULT 500,

            gems INTEGER DEFAULT 0,

            attack INTEGER DEFAULT 5,

            defense INTEGER DEFAULT 5,

            luck INTEGER DEFAULT 1,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
        """)

        # ================= INVENTORY =================

        self.execute("""
        CREATE TABLE IF NOT EXISTS inventory (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER NOT NULL,

            item_id TEXT NOT NULL,

            quantity INTEGER DEFAULT 1,

            FOREIGN KEY(user_id)
            REFERENCES users(user_id)

        )
        """)

        # ================= EQUIPMENT =================

        self.execute("""
        CREATE TABLE IF NOT EXISTS equipment (

            user_id INTEGER PRIMARY KEY,

            weapon TEXT,

            armor TEXT,

            accessory TEXT,

            FOREIGN KEY(user_id)
            REFERENCES users(user_id)

        )
        """)

        # ================= STATISTICS =================

        self.execute("""
        CREATE TABLE IF NOT EXISTS statistics (

            user_id INTEGER PRIMARY KEY,

            messages INTEGER DEFAULT 0,

            voice_minutes INTEGER DEFAULT 0,

            monsters_killed INTEGER DEFAULT 0,

            bosses_killed INTEGER DEFAULT 0,

            chests_opened INTEGER DEFAULT 0,

            total_coins_earned INTEGER DEFAULT 0,

            login_days INTEGER DEFAULT 0,

            FOREIGN KEY(user_id)
            REFERENCES users(user_id)

        )
        """)

        # ================= VOICE ROOMS =================

        self.execute("""
        CREATE TABLE IF NOT EXISTS voice_rooms (

            owner_id INTEGER PRIMARY KEY,

            channel_id INTEGER,

            channel_name TEXT,

            user_limit INTEGER DEFAULT 0,

            locked INTEGER DEFAULT 0,

            FOREIGN KEY(owner_id)
            REFERENCES users(user_id)

        )
        """)

        # ================= VOICE BANS =================

        self.execute("""
        CREATE TABLE IF NOT EXISTS voice_bans (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            channel_id INTEGER NOT NULL,

            user_id INTEGER NOT NULL

        )
        """)

        # ================= COOLDOWNS =================

        self.execute("""
        CREATE TABLE IF NOT EXISTS cooldowns (

            user_id INTEGER PRIMARY KEY,

            daily TEXT,

            loot TEXT,

            dungeon TEXT,

            boss TEXT,

            FOREIGN KEY(user_id)
            REFERENCES users(user_id)

        )
        """)

        # ================= ACHIEVEMENTS =================

        self.execute("""
        CREATE TABLE IF NOT EXISTS achievements (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER,

            achievement TEXT,

            FOREIGN KEY(user_id)
            REFERENCES users(user_id)

        )
        """)

        # ================= QUESTS =================

        self.execute("""
        CREATE TABLE IF NOT EXISTS quests (

            user_id INTEGER PRIMARY KEY,

            daily_progress INTEGER DEFAULT 0,

            weekly_progress INTEGER DEFAULT 0,

            FOREIGN KEY(user_id)
            REFERENCES users(user_id)

        )
        """)

        logger.info(
            "All database tables created successfully."
        )

    # ==================================================
    # DATABASE
    # ==================================================

    def commit(self):

        self.connection.commit()

    def close(self):

        logger.info(
            "Closing database connection..."
        )

        self.connection.close()

    # ==================================================
    # USERS
    # ==================================================

    def user_exists(
        self,
        user_id: int
    ) -> bool:

        return self.fetchone(
            """
            SELECT 1
            FROM users
            WHERE user_id = ?
            """,
            (
                user_id,
            )

        ) is not None

    def create_user(
        self,
        user_id: int,
        username: str
    ):

        if self.user_exists(user_id):

            return

        logger.info(
            f"Creating player: {username} ({user_id})"
        )

        self.execute(
            """
            INSERT INTO users
            (
                user_id,
                username
            )

            VALUES (?, ?)

            """,
            (
                user_id,
                username
            )
        )

        self.execute(
            """
            INSERT INTO statistics
            (
                user_id
            )

            VALUES (?)

            """,
            (
                user_id,
            )
        )

        self.execute(
            """
            INSERT INTO equipment
            (
                user_id
            )

            VALUES (?)

            """,
            (
                user_id,
            )
        )

        self.execute(
            """
            INSERT INTO cooldowns
            (
                user_id
            )

            VALUES (?)

            """,
            (
                user_id,
            )
        )

        self.execute(
            """
            INSERT INTO quests
            (
                user_id
            )

            VALUES (?)

            """,
            (
                user_id,
            )
        )

        logger.info(
            f"Player {username} created successfully."
        )

    def get_user(
        self,
        user_id: int
    ):

        return self.fetchone(
            """
            SELECT *
            FROM users
            WHERE user_id = ?
            """,
            (
                user_id,
            )
        )

    def update_username(
        self,
        user_id: int,
        username: str
    ):

        self.execute(
            """
            UPDATE users

            SET username = ?

            WHERE user_id = ?

            """,
            (
                username,
                user_id
            )
        )


# ==================================================
# INSTANCE
# ==================================================

database = DatabaseManager()