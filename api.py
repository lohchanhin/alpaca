"""提供簡易 Web API 的介面。"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path
from typing import Optional

import robots

import account
import config

app = FastAPI(title="Alpaca Trading API")


@app.get("/")
def dashboard():
    """回傳前端儀表板頁面"""
    path = Path(__file__).parent / "dashboard" / "index.html"
    return FileResponse(path)

_client = None


def _ensure_client():
    global _client
    if _client is None:
        if not config.ALPACA_API_KEY or not config.ALPACA_SECRET_KEY:
            raise HTTPException(status_code=400, detail="API key 尚未設定")
        _client = account.connect(
            config.ALPACA_API_KEY, config.ALPACA_SECRET_KEY, paper=config.USE_PAPER
        )
    return _client


@app.get("/account")
def get_account():
    client = _ensure_client()
    return account.get_account_info(client)


@app.get("/positions")
def positions():
    client = _ensure_client()
    return account.get_positions(client)


@app.get("/orders")
def orders(limit: Optional[int] = None):
    client = _ensure_client()
    return account.get_trade_history(client, limit=limit)


@app.get("/bots")
def bots() -> list:
    """取得所有交易機器人資訊。"""
    return robots.get_bots()


@app.post("/bots")
def create_bot(bot: dict):
    """新增一個交易機器人。"""
    robots.add_bot(bot)
    return {"id": len(robots.get_bots()) - 1}


@app.get("/bots/{bot_id}")
def get_bot(bot_id: int):
    bots = robots.get_bots()
    if bot_id < 0 or bot_id >= len(bots):
        raise HTTPException(status_code=404, detail="Bot not found")
    return bots[bot_id]


@app.put("/bots/{bot_id}")
def update_bot(bot_id: int, bot: dict):
    try:
        robots.update_bot(bot_id, bot)
    except IndexError:
        raise HTTPException(status_code=404, detail="Bot not found")
    return {"success": True}


@app.delete("/bots/{bot_id}")
def delete_bot(bot_id: int):
    try:
        robots.delete_bot(bot_id)
    except IndexError:
        raise HTTPException(status_code=404, detail="Bot not found")
    return {"success": True}
