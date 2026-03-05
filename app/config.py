import os

BOT_TOKEN = os.getenv("TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")

if not BOT_TOKEN:
    raise ValueError("TOKEN is not set")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set")