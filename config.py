from pathlib import Path
from dotenv import load_dotenv
import os

# ==========================
# Загрузка .env
# ==========================

load_dotenv()

# ==========================
# Пути проекта
# ==========================

BASE_DIR = Path(__file__).parent

DATA_DIR = BASE_DIR / "data"
LOGS_DIR = BASE_DIR / "logs"
ASSETS_DIR = BASE_DIR / "assets"

DATABASE_PATH = DATA_DIR / "database.db"

# Создаем папки автоматически
DATA_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)
ASSETS_DIR.mkdir(exist_ok=True)

# ==========================
# Discord
# ==========================

TOKEN = os.getenv("DISCORD_TOKEN")

# Для разработки можно оставить None.
# Позже сюда можно вписать ID сервера,
# чтобы Slash-команды обновлялись мгновенно.
GUILD_ID = None

# ==========================
# Цвета Embed
# ==========================

EMBED_COLOR = 0x5865F2
SUCCESS_COLOR = 0x57F287
ERROR_COLOR = 0xED4245
WARNING_COLOR = 0xFEE75C

# ==========================
# Экономика
# ==========================

START_BALANCE = 500

DAILY_MIN = 150
DAILY_MAX = 300

WORK_MIN = 80
WORK_MAX = 220

DEATH_LOSS_PERCENT = 0.15

# ==========================
# XP
# ==========================

START_LEVEL = 1
START_XP = 0

XP_PER_MESSAGE_MIN = 8
XP_PER_MESSAGE_MAX = 18

MESSAGE_XP_COOLDOWN = 60

# Формула:
# level² * LEVEL_MULTIPLIER
LEVEL_MULTIPLIER = 100

# ==========================
# RPG
# ==========================

START_HP = 100
MAX_HP = 100

START_ENERGY = 100
MAX_ENERGY = 100

START_HUNGER = 100
MAX_HUNGER = 100

PASSIVE_HP_REGEN = 2
PASSIVE_ENERGY_REGEN = 4

# ==========================
# Магазин
# ==========================

SHOP_REFRESH_MINUTES = 60

# ==========================
# Лимиты
# ==========================

MAX_INVENTORY_SIZE = 100

# ==========================
# Версия проекта
# ==========================

BOT_NAME = "Pixel Companion"

BOT_VERSION = "1.0.0"

BOT_AUTHOR = "Alecks & ChatGPT"

# ==========================
# Логирование
# ==========================

LOG_LEVEL = "INFO"