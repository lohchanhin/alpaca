"""簡易交易機器人資訊管理模組。"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

# 機器人資訊儲存檔案
_ROBOTS_FILE = Path(__file__).with_name("robots.json")

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
    return list(_load())


def add_bot(bot: Dict[str, Any]) -> None:
    """新增一個交易機器人並存檔。"""
    bots = _load()
    bots.append(bot)
    _save()
