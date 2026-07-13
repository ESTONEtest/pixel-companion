import asyncio
import traceback
import shutil
import os

import discord
from discord.ext import commands

from config import TOKEN
from utils.logger import logger


# ==================================================
# FFMPEG CHECK
# ==================================================

def check_ffmpeg():

    ffmpeg = shutil.which("ffmpeg")

    if ffmpeg:
        logger.info(
            f"🎵 FFmpeg найден: {ffmpeg}"
        )

        return ffmpeg

    else:
        logger.error(
            "❌ FFmpeg не найден"
        )

        return None


FFMPEG_PATH = check_ffmpeg()


# ==================================================
# TOKEN CHECK
# ==================================================

if not TOKEN:

    raise RuntimeError(
        "❌ TOKEN не найден. Добавь TOKEN в Railway Variables или .env"
    )


# ==================================================
# DATABASE
# ==================================================

from managers.database import database


# ==================================================
# BOT
# ==================================================

intents = discord.Intents.default()

intents.message_content = True
intents.members = True
intents.guilds = True
intents.voice_states = True


bot = commands.Bot(
    command_prefix="!",
    intents=intents
)


# ==================================================
# EVENTS
# ==================================================

@bot.event
async def on_ready():

    logger.info("=" * 50)

    logger.info(
        f"Logged in as: {bot.user}"
    )

    logger.info(
        f"Guilds: {len(bot.guilds)}"
    )

    logger.info(
        "Pixel Companion RPG v2.0 is ONLINE!"
    )

    logger.info("=" * 50)


    logger.info(
        "Loaded commands:"
    )


    for command in bot.commands:

        logger.info(
            f" - !{command.name}"
        )


# ==================================================
# COMMAND ERRORS
# ==================================================

@bot.event
async def on_command_error(
    ctx,
    error
):

    logger.error(
        f"Command '{ctx.command}' failed:"
    )


    traceback.print_exception(
        type(error),
        error,
        error.__traceback__
    )


# ==================================================
# COGS
# ==================================================

async def load_cogs():

    cogs = [

        "profile",

        "events",

        "rpg",

        "level",

        "inventory",

        "items",

        "loot",

        "equipment",

        "shop",

        "daily",

        "battle",

        "voice",

        "stream",

        "welcome",

        "test_level",

        "test_roles",

        "game_roles",

        "music",

        "wishes"

    ]


    for cog in cogs:

        try:

            await bot.load_extension(
                f"cogs.{cog}"
            )


            logger.info(
                f"✅ Loaded cog: {cog}"
            )


        except Exception as error:

            logger.error(
                f"❌ Failed loading {cog}: {error}"
            )


# ==================================================
# START
# ==================================================

async def main():

    async with bot:

        await load_cogs()


        await bot.start(
            TOKEN
        )


if __name__ == "__main__":

    asyncio.run(main())