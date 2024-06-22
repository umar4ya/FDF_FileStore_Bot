import os
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from handlers import start, help, contact, save_pdf, search_query, search_command
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Tor proxy URL
TOR_PROXY_URL = os.getenv('TOR_PROXY_URL')

def main():
    app = ApplicationBuilder() \
        .token(os.getenv('BOT_TOKEN')) \
        .proxy_url(TOR_PROXY_URL) \
        .get_updates_proxy(TOR_PROXY_URL) \
        .build()

    # Register command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help))
    app.add_handler(CommandHandler("contact", contact))
    app.add_handler(CommandHandler("search", search_command))

    # Register document handler
    app.add_handler(MessageHandler(filters.Document.PDF, save_pdf))

    # Register message handler for search queries
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), search_query))

    # Start polling
    app.run_polling()

if __name__ == '__main__':
    main()
