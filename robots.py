"""簡易交易機器人資訊管理模組。"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

# 機器人資訊儲存檔案
_ROBOTS_FILE = Path(__file__).with_name("robots.json")

# 預設欄位
_DEFAULT_BOT: Dict[str, Any] = {
    "name": "",
    "strategy": "",
    "enabled": False,
    "params": {},
}

# 內部快取
_bots: List[Dict[str, Any]] | None = None


def _load() -> List[Dict[str, Any]]:
    global _bots
    if _bots is None:
        if _ROBOTS_FILE.exists():
            text = _ROBOTS_FILE.read_text(encoding="utf-8")
            try:
                _bots = json.loads(text)
            except json.JSONDecodeError:
                _bots = []
        else:
            _bots = []
    return _bots


def _save() -> None:
    if _bots is not None:
        _ROBOTS_FILE.write_text(
            json.dumps(_bots, ensure_ascii=False, indent=2), encoding="utf-8"
        )


def get_bots() -> List[Dict[str, Any]]:
    """取得所有交易機器人資訊。"""
    bots = []
    for bot in _load():
        merged = {**_DEFAULT_BOT, **bot}
        bots.append(merged)
    return bots


def add_bot(bot: Dict[str, Any]) -> None:
    """新增一個交易機器人並存檔。"""
    bots = _load()
    new_bot = {**_DEFAULT_BOT, **bot}
    bots.append(new_bot)
    _save()


def update_bot(bot_id: int, bot: Dict[str, Any]) -> None:
    """更新指定索引的交易機器人資料。"""
    bots = _load()
    if bot_id < 0 or bot_id >= len(bots):
        raise IndexError("bot not found")
    bots[bot_id].update(bot)
    # 確保所有欄位皆存在
    bots[bot_id] = {**_DEFAULT_BOT, **bots[bot_id]}
    _save()


def delete_bot(bot_id: int) -> None:
    """刪除指定索引的交易機器人。"""
    bots = _load()
    if bot_id < 0 or bot_id >= len(bots):
        raise IndexError("bot not found")
    del bots[bot_id]
    _save()
