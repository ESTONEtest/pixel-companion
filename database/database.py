import sqlite3
from config import DATABASE_PATH


class Database:
    def __init__(self):
        self.db_path = DATABASE_PATH
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def initialize(self):
        self.cursor.executescript("""
        PRAGMA foreign_keys = ON;

        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            level INTEGER NOT NULL DEFAULT 1,
            xp INTEGER NOT NULL DEFAULT 0,
            balance INTEGER NOT NULL DEFAULT 500,
            hp INTEGER NOT NULL DEFAULT 100,
            max_hp INTEGER NOT NULL DEFAULT 100,
            energy INTEGER NOT NULL DEFAULT 100,
            max_energy INTEGER NOT NULL DEFAULT 100,
            hunger INTEGER NOT NULL DEFAULT 100,
            max_hunger INTEGER NOT NULL DEFAULT 100,
            messages INTEGER NOT NULL DEFAULT 0,
            daily_timestamp INTEGER DEFAULT 0,
            work_timestamp INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            item_id TEXT,
            amount INTEGER DEFAULT 1
        );

        CREATE TABLE IF NOT EXISTS shop (
            item_id TEXT PRIMARY KEY,
            name TEXT,
            description TEXT,
            price INTEGER,
            category TEXT,
            rarity TEXT,
            usable INTEGER DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS achievements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            achievement TEXT,
            unlocked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS level_roles (
            level INTEGER PRIMARY KEY,
            role_id INTEGER
        );

        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT
        );
        """)

        self.conn.commit()


database = Database()