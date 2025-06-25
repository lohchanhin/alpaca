"""交易機器人設定檔。"""

from dotenv import load_dotenv
import os

load_dotenv()

ALPACA_API_KEY = os.getenv("APCA_API_KEY_ID", "")
ALPACA_SECRET_KEY = os.getenv("APCA_API_SECRET_KEY", "")
# 是否使用 Paper Trading 環境，可透過環境變數 ALPACA_USE_PAPER 設定
USE_PAPER = os.getenv("ALPACA_USE_PAPER", "true").lower() == "true"
