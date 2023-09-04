import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from routers import router
from config import TOKEN
from database import MemorySubscriptionRepo


async def main():
    bot = Bot(token=TOKEN, parse_mode=ParseMode.MARKDOWN)
    dp = Dispatcher()
    dp["sub_repo"] = MemorySubscriptionRepo()
    dp.include_router(router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
