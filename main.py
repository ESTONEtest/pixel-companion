import asyncio
import os
from pathlib import Path

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    help_command=None
)


async def load_cogs():
    for file in Path("cogs").glob("*.py"):
        if file.name.startswith("_"):
            continue

        try:
            await bot.load_extension(f"cogs.{file.stem}")
            print(f"LOADED: cogs.{file.stem}")
        except Exception as e:
            print(f"ERROR LOADING {file.stem}: {e}")


@bot.event
async def on_ready():
    print(f"BOT ONLINE: {bot.user}")


@bot.event
async def setup_hook():
    await load_cogs()


async def main():
    if not TOKEN:
        print("NO TOKEN")
        return

    async with bot:
        await bot.start(TOKEN)


if __name__ == "__main__":
    asyncio.run(main())