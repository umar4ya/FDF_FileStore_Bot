import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
MONGO_URI = os.getenv('MONGO_URI')
TOR_PROXY_URL = os.getenv('socks5://127.0.0.1:9150')
