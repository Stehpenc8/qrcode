import asyncio 
from aiogram import Bot,Dispatcher

from app.handlers import router


async def main():
    bot = Bot(token='7381846033:AAGJLEvyAaLeaPMIK0a_Xi5ntAK6-vrRyAo')
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот отключен')