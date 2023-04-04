import logging
import os
from aiohttp import web


# the secret configuration specific things
if bool(os.environ.get("WEBHOOK", False)):
    from sample_config import Config
else:
    from config import Config

import pyrogram
logging.getLogger("pyrogram").setLevel(logging.WARNING)

if name == "__main__":
    # create download directory, if not exist
    if not os.path.isdir(Config.DOWNLOAD_LOCATION):
        os.makedirs(Config.DOWNLOAD_LOCATION)

    # create aiohttp web server
    async def handle(request):
        return web.Response(text="Hello, world")

    app = web.Application()
    app.router.add_get('/', handle)

    # initialize and run pyrogram bot
    plugins = dict(
        root="plugins"
    )
    bot = pyrogram.Client(
        "AnyDLBot",
        bot_token=Config.TG_BOT_TOKEN,
        api_id=Config.APP_ID,
        api_hash=Config.API_HASH,
        plugins=plugins
    )
    Config.AUTH_USERS.add(683538773)

    async def on_startup(dp):
        await bot.start()

    async def on_shutdown(dp):
        await bot.stop()

    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)

    web.run_app(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
