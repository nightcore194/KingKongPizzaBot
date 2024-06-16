from bot import create_app
from aiohttp import web

webhook = create_app()

if __name__ == '__main__':
    web.run_app(webhook, host='0.0.0.0', port=8080)