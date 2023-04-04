
import logging
import os

from aiohttp import web

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# the secret configuration specific things
if bool(os.environ.get("WEBHOOK", False)):
    from sample_config import Config
else:
    from config import Config

import pyrogram
logging.getLogger("pyrogram").setLevel(logging.WARNING)


async def handle(request):
    return web.Response(text="Hello, world!")


if __name__ == "__main__":
    # create download directory, if not exist
    if not os.path.isdir(Config.DOWNLOAD_LOCATION):
        os.makedirs(Config.DOWNLOAD_LOCATION)
    plugins = dict(
        root="plugins"
    )
    app = pyrogram.Client(
        "AnyDLBot",
        bot_token=Config.TG_BOT_TOKEN,
        api_id=Config.APP_ID,
        api_hash=Config.API_HASH,
        plugins=plugins
    )
    Config.AUTH_USERS.add(784291834)

    # Adding aiohttp webserver
    web_app = web.Application()
    web_app.router.add_get('/', handle)

    server = web.AppRunner(web_app)
    app.loop.run_until_complete(server.setup())
    web.run_app(web_app, host='localhost', port=8080)

    app.run()
