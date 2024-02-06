#!/usr/bin/env python
# pylint: disable=unused-argument

import os

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OLLAMA_ENDPOINT = os.getenv("OLLAMA_ENDPOINT")

import requests

from telegram import Update
from telegram.ext import Application, ContextTypes, MessageHandler, filters

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    data = {
      "model": "mistral:7b",
      "messages": [
        {
          "role": "user",
          "content": update.message.text
        }
      ],
      "stream": False
    }
    response = requests.post(OLLAMA_ENDPOINT, json=data )

    if response.status_code == 200:
        ollama_response = response.json().get('message').get('content')
        await update.message.reply_text(ollama_response)
    else:
        await update.message.reply_text('Sorry, there was an error processing your request.')

def main() -> None:
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
