import time

from utils.database import (
    create_user,
    get_user,
    update_user
)

# ─────────────────────────────
# НАСТРОЙКИ ЭКОНОМИКИ
# ─────────────────────────────

VOICE_REWARD_TIME = 300     # 5 минут
VOICE_XP_REWARD = 10
VOICE_COINS_REWARD = 5

LEVELS = [
    (1, 0),
    (2, 250),
    (3, 1000),
    (4, 3000),
    (5, 7000),
    (6, 15000),
    (7, 30000),
]

# ─────────────────────────────
# СОЗДАНИЕ ПРОФИЛЯ
# ─────────────────────────────

def register_user(user_id):
    create_user(user_id)


# ─────────────────────────────
# ВХОД В ГОЛОС
# ─────────────────────────────

def voice_join(user_id):

    user = create_user(user_id)

    user["last_voice_join"] = int(time.time())

    update_user(user_id, user)


# ─────────────────────────────
# ВЫХОД ИЗ ГОЛОСА
# ─────────────────────────────

def voice_leave(user_id):

    user = get_user(user_id)

    if not user:
        return

    if user["last_voice_join"] is None:
        return

    now = int(time.time())

    seconds = now - user["last_voice_join"]

    user["voice_time"] += seconds

    rewards = seconds // VOICE_REWARD_TIME

    if rewards > 0:

        user["coins"] += rewards * VOICE_COINS_REWARD
        user["xp"] += rewards * VOICE_XP_REWARD

    user["last_voice_join"] = None

    user["level"] = calculate_level(user["xp"])

    update_user(user_id, user)


# ─────────────────────────────
# ПОЛУЧИТЬ УРОВЕНЬ
# ─────────────────────────────

def calculate_level(xp):

    level = 1

    for lvl, required in LEVELS:
        if xp >= required:
            level = lvl

    return level