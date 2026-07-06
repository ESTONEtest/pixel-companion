import asyncio
import logging
import os
from pathlib import Path

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

# =========================
# CONFIG
# =========================

TOKEN = os.getenv("DISCORD_TOKEN")

BOT_NAME = "Pixel Companion"
BOT_VERSION = "1.0"
LOG_LEVEL = "INFO"

# =========================
# LOGGING
# =========================

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL.upper(), logging.INFO),
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

logger = logging.getLogger(BOT_NAME)

# =========================
# INTENTS
# =========================

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# =========================
# BOT
# =========================

bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    help_command=None,
)

# =========================
# COG LOADER
# =========================

async def load_cogs():
    cogs_path = Path("cogs")

    if not cogs_path.exists():
        logger.warning("cogs folder not found")
        return

    for file in cogs_path.glob("*.py"):
        if file.name.startswith("_"):
            continue

        extension = f"cogs.{file.stem}"

        try:
            await bot.load_extension(extension)
            logger.info(f"Loaded: {extension}")
        except Exception as e:
            logger.exception(f"Failed to load {extension}: {e}")

# =========================
# READY EVENT
# =========================

@bot.event
async def on_ready():
    logger.info("=" * 40)
    logger.info(f"{BOT_NAME} v{BOT_VERSION}")
    logger.info(f"Logged in as {bot.user}")
    logger.info("=" * 40)

# =========================
# MAIN
# =========================

async def main():
    print(">>> BOT STARTING <<<")

    if not TOKEN:
        logger.error("DISCORD_TOKEN is missing in .env or Railway Variables!")
        return

    async with bot:
        await load_cogs()
        await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())