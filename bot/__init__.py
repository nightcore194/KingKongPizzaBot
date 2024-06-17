import logging
import asyncio
from aiohttp.web import Application
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

from bot.bot import bot, dp, on_startup
from bot.modules import admin, cooking, info, report


def create_app() -> Application:
    # Create aiohttp.web.Application instance
    dp.include_routers(admin.router, cooking.router, info.router, report.router)
    dp.startup.register(on_startup)
    app = Application()
    SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path='/webhook')
    setup_application(app, dp, bot=bot)
    # init logger
    logging.basicConfig(filename='./log/bot.log', level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
    return app

"""
FOR LOCAL HOSTING 
RUN WITH python -c "from bot import run; run()" FROM VENV SPACE
"""


async def main() -> None:
    try:
        logging.basicConfig(filename='./log/bot.log', level=logging.DEBUG,
                            format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
        dp.include_routers(admin.router, cooking.router, info.router, report.router)
        await bot.delete_webhook()
        await dp.start_polling(bot)
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


def run() -> None:
    asyncio.run(main())
