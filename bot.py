import logging
import os
import aiohttp
from aiohttp import web
from pyrogram import Client, filters

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

if bool(os.environ.get("WEBHOOK", False)):
    from sample_config import Config
else:
    from config import Config

logging.getLogger('pyrogram').setLevel(logging.WARNING)

plugins = dict(root='plugins')
app = Client('AnyDLBot', bot_token=Config.TG_BOT_TOKEN, api_id=Config.APP_ID, api_hash=Config.API_HASH, plugins=plugins)
webhook_app = web.Application()


async def webhook(request):
    content = await request.json()
    update = content['message']
    await app.process_updates([update])
    return web.Response(status=200)


webhook_app.add_routes([web.post('/webhook', webhook)])
webhook_runner = web.AppRunner(webhook_app)

async def start():
    await app.start()
    await aiohttp.ClientSession().post(Config.WEBHOOK_URL+'/setWebhook?url='+Config.WEBHOOK_URL+'/webhook')


async def stop():
    await app.stop()
    await webhook_runner.cleanup()


if __name__ == '__main__':
    app.add_handler(filters.private & filters.command(['start']))(start)

    try:
        loop = asyncio.get_event_loop()
        loop.create_task(start_webhook())
        app.run()
    except Exception as e:
        logger.error(e)
        asyncio.get_event_loop().run_until_complete(webhook_runner.cleanup())
