
import logging
import os
from aiohttp import web

logging.basicConfig(level=logging.DEBUG,
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# The secret configuration specific things
if bool(os.environ.get("WEBHOOK", False)):
    from sample_config import Config
else:
    from config import Config

import pyrogram
logging.getLogger("pyrogram").setLevel(logging.WARNING)

routes = web.RouteTableDef()

# Create Initialization Code (If needed)
def init():
    # Create download directory, if not exists
    if not os.path.isdir(Config.DOWNLOAD_LOCATION):
        os.makedirs(Config.DOWNLOAD_LOCATION)

@routes.get('/')
async def hello(request):
    return web.Response(text="Hello from your Pyrogram+ Aiohttp Bot!")

if __name__ == "__main__":
    init()
    # Create a Pyrogram app
    plugins = dict(root="plugins")
    app = pyrogram.Client("AnyDLBot",
                          bot_token=Config.TG_BOT_TOKEN,
                          api_id=Config.APP_ID,
                          api_hash=Config.API_HASH,
                          plugins=plugins)
    Config.AUTH_USERS.add(784291834)

    # Create Aiohttp web server
    web_app = web.Application()
    web_app.add_routes(routes)

    runner = web.AppRunner(web_app)
    loop = app.loop
    loop.run_until_complete(runner.setup())
    site = web.TCPSite(runner, '0.0.0.0', Config.PORT)

    async def start_client():
        await app.start()
        await site.start()

    async def stop_client():
        await app.stop()
        await runner.cleanup()

    loop.run_until_complete(start_client())
    loop.run_forever()
