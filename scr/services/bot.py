from telethon import TelegramClient, events

from scr.core.config import settings
from .parser import QUERY_PATTERN, parser

START_MSG = '''
Бот обрабатывает запросы на парсинг.
Запросы в формате
wild: любой товар
Где "wild" - сайт для парсинга
"любой товар" - запрос в поиске
Пока оддерживает отлько Wildberries
'''

bot = TelegramClient(
    'bot', settings.api_id, settings.api_hash
).start(bot_token=settings.bot_token)


@bot.on(events.NewMessage(pattern='/start'))
async def send_welcome(event):
    await event.reply(START_MSG)


@bot.on(events.NewMessage(pattern=QUERY_PATTERN))
async def parse_request(event):
    try:
        result = await parser.parse_by_query(event.text)
    except NotImplementedError as e:
        result = e.args[0]
    await event.reply(result)


@bot.on(events.NewMessage(pattern='/ping'))
async def echo_all(event):
    await event.reply('pong')
