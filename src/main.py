import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from routers import router
from config import TOKEN
from database import MemorySubscriptionRepo
from notifier import loop


async def main():
    bot = Bot(token=TOKEN, parse_mode=ParseMode.MARKDOWN)
    dp = Dispatcher()
    sub_repo = MemorySubscriptionRepo()
    dp["sub_repo"] = sub_repo
    dp.include_router(router)

    await asyncio.gather(*[dp.start_polling(bot), loop(bot, sub_repo)])


if __name__ == "__main__":
    asyncio.run(main())
