import asyncio

from discord_bot import create_discord_bot
from tg import create_telegram_bridge
from qprocessor import MessageProcessor

from asyncio import create_task, gather, run
import os
from dotenv import load_dotenv


load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
DISCORD_CHANNEL = os.getenv('DISCORD_CHANNEL')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
API_HASH = os.getenv('API_HASH')
API_ID = os.getenv('API_ID')
DISCORD_GUILD = os.getenv('DISCORD_GUILD')
TELEGRAM_CHAT = os.getenv('TELEGRAM_CHAT')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


async def main():
    discord_bot = create_discord_bot(DISCORD_CHANNEL)

    telegram_bot = create_telegram_bridge(TELEGRAM_TOKEN, API_ID, API_HASH)
    await telegram_bot.start()

    processor = MessageProcessor(telegram_bot, discord_bot, DISCORD_GUILD, DISCORD_CHANNEL, TELEGRAM_CHAT)

    processor_task = create_task(processor.process())

    await gather(discord_bot.start(DISCORD_TOKEN), asyncio.Event().wait())


if __name__ == "__main__":
    run(main())