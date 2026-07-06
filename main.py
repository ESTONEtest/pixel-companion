import asyncio
import logging
from pathlib import Path

import discord
from discord.ext import commands

from dotenv import load_dotenv
load_dotenv()

from config import (
    TOKEN,
    BOT_NAME,
    BOT_VERSION,
    LOG_LEVEL,
)

from database.database import database

# ==========================
# LOGGING
# ==========================

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL.upper(), logging.INFO),
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

logger = logging.getLogger(BOT_NAME)

# ==========================
# INTENTS
# ==========================

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# ==========================
# BOT
# ==========================

bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    help_command=None,
)

# ==========================
# COGS
# ==========================

async def load_cogs():
    cogs_path = Path("cogs")

    if not cogs_path.exists():
        logger.warning("Папка cogs не найдена")
        return

    for file in cogs_path.glob("*.py"):

        if file.name.startswith("_"):
            continue

        extension = f"cogs.{file.stem}"

        try:
            await bot.load_extension(extension)
            logger.info(f"Загружен модуль: {extension}")

        except Exception as error:
            logger.exception(f"Ошибка загрузки {extension}: {error}")

# ==========================
# READY EVENT
# ==========================

@bot.event
async def on_ready():

    logger.info("=" * 40)
    logger.info(f"{BOT_NAME} v{BOT_VERSION}")
    logger.info(f"Logged in as {bot.user}")
    logger.info("=" * 40)

# ==========================
# MAIN
# ==========================

async def main():

    logger.info("Инициализация базы данных...")

    database.initialize()   # <-- sync, без await

    logger.info("База данных готова")

    async with bot:

        await load_cogs()
        await bot.start(TOKEN)


if __name__ == "__main__":
    asyncio.run(main())