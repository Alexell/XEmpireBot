import asyncio
import os
from aiohttp import web
from bot.core import launcher
from bot.utils.logger import log

# Start the bot process
async def run_bot():
    await launcher.start()

# Web server handler
async def handle(request):
    return web.Response(text="Bot is running!")

async def init_app():
    app = web.Application()
    app.router.add_get('/', handle)
    return app

async def main():
    # Start the bot process in the background
    asyncio.create_task(run_bot())

    # Setup the web server
    app = await init_app()
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get('PORT', 8000))  # Get the port from environment, default to 8000
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()

    # Keep the app running
    try:
        while True:
            await asyncio.sleep(3600)  # Keep the event loop running
    except KeyboardInterrupt:
        log.info("Bot stopped by user")

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        log.info("Bot stopped by user")
