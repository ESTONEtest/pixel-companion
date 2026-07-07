import os
from dotenv import load_dotenv

load_dotenv()


# ==========================
# BOT
# ==========================

TOKEN = os.getenv("TOKEN")

PREFIX = "!"


# ==========================
# BOT INFO
# ==========================

BOT_NAME = "Pixel Companion RPG"
BOT_VERSION = "2.0.0"


# ==========================
# COLORS
# ==========================

COLOR_DEFAULT = 0x5865F2
COLOR_SUCCESS = 0x57F287
COLOR_ERROR = 0xED4245
COLOR_WARNING = 0xFEE75C


# ==========================
# RPG
# ==========================

START_HP = 100
START_LEVEL = 1

START_COINS = 500
START_GEMS = 0

MAX_LEVEL = 100


# ==========================
# XP
# ==========================

XP_PER_MESSAGE = (3, 7)

VOICE_XP_PER_MINUTE = 4


# ==========================
# DATABASE
# ==========================

DATABASE = "database/users.db"


# ==========================
# LOGS
# ==========================

LOG_FILE = "logs/bot.log"


# ==========================
# VOICE
# ==========================

VOICE_CATEGORY_NAME = "🎧 Pixel Voices"

VOICE_CREATE_CHANNEL = "➕ create-voice"


# ==========================
# STREAM
# ==========================

STREAM_CHANNEL_ID = int(
    os.getenv(
        "STREAM_CHANNEL_ID",
        0
    )
)


TWITCH_CHANNEL = "captain_icecream"


# ==========================
# WELCOME
# ==========================

WELCOME_CHANNEL_ID = int(
    os.getenv(
        "WELCOME_CHANNEL_ID",
        0
    )
)