
import logging
import os

from aiohttp import web
import pyrogram
assert pyrogram

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# The secret configuration specific things
if bool(os.environ.get("WEBHOOK", False)):
    from sample_config import Config
else:
    from config import Config


# Create download directory, if not exist
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

# Here we begin the aiohttp server
async def handle(request):
    return web.Response(text="Hello, world")

app.router.add_get('/', handle)

if __name__ == "__main__":
    try:
        import nest_asyncio

        nest_asyncio.apply()
    except ImportError:
        pass

    import asyncio

    asyncio.ensure_future(app.start())

    web.run_app(app, host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))

    # This is the closing
    app.stop()
