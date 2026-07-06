import sqlite3
import os


class Database:
    def __init__(self):
        db_path = os.path.join(os.path.dirname(__file__), "database.db")

        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()

        self.initialize()

    def initialize(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            level INTEGER DEFAULT 0,
            xp INTEGER DEFAULT 0,
            money INTEGER DEFAULT 0
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS economy (
            user_id INTEGER PRIMARY KEY,
            balance INTEGER DEFAULT 0
        )
        """)

        self.conn.commit()

    def get_user(self, user_id: int):
        self.cursor.execute(
            "SELECT level, xp, money FROM users WHERE user_id = ?",
            (user_id,)
        )
        return self.cursor.fetchone()

    def create_user(self, user_id: int):
        self.cursor.execute(
            "INSERT OR IGNORE INTO users (user_id, level, xp, money) VALUES (?, 0, 0, 0)",
            (user_id,)
        )
        self.conn.commit()

    def update_xp(self, user_id: int, xp: int):
        self.cursor.execute(
            "UPDATE users SET xp = xp + ? WHERE user_id = ?",
            (xp, user_id)
        )
        self.conn.commit()

    def update_level(self, user_id: int, level: int):
        self.cursor.execute(
            "UPDATE users SET level = ? WHERE user_id = ?",
            (level, user_id)
        )
        self.conn.commit()


database = Database()