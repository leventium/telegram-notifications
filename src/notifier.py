from asyncio import sleep
from aiogram import Bot
from src.database import MemorySubscriptionRepo
from src.plugin_manager import PluginManager
from src.config import COOLDOWN
from src.logger import logger


async def send_happened_events_notice(
        bot: Bot,
        sub_repo: MemorySubscriptionRepo
) -> None:
    logger.info("Going to check for events' states")
    plug_manager = PluginManager()
    events = plug_manager.get_happened_events()

    for event in events:
        subscribed_chats = await sub_repo.get_chats_by_sub_name(event)
        for chat_id in subscribed_chats:
            logger.info(f'Sending notification "{event}" to chat "{chat_id}"')
            await bot.send_message(
                chat_id=chat_id,
                text=f'Hey, "{event}" has happened'
            )


async def loop(bot: Bot, sub_repo: MemorySubscriptionRepo):
    while True:
        await send_happened_events_notice(bot, sub_repo)
        await sleep(COOLDOWN * 60)
