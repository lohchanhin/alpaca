"""交易機器人設定檔。"""

from dotenv import load_dotenv
import os

load_dotenv()

ALPACA_API_KEY = os.getenv("APCA_API_KEY_ID", "")
ALPACA_SECRET_KEY = os.getenv("APCA_API_SECRET_KEY", "")
USE_PAPER = True
