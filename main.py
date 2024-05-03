import asyncio
import os

from functions_framework import http
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
)
from telegram import Update


@http
def telegram_bot(request):
    return asyncio.run(main(request))


async def main(request):
    token = os.environ.get('TELEGRAM_BOT_TOKEN')
    app = Application.builder().token(token).build()
    bot = app.bot

    app.add_handler(CommandHandler("start", on_start))
    app.add_handler(MessageHandler(filters.TEXT, on_message))

    if request.method == 'GET':
        await bot.set_webhook(f'https://{request.host}/telegram_bot')
        return "webhook set"

    async with app:
        update = Update.de_json(request.json, bot)
        await app.process_update(update)

    return "ok"


async def on_start(update: Update, context):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Hello, I'm your first bot!"
    )


async def on_message(update: Update, context):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=update.message.text
    )
