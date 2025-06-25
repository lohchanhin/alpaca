from __future__ import annotations

"""Alpaca 帳戶相關操作模組。"""

from decimal import Decimal, ROUND_HALF_UP
from typing import List, Optional

from alpaca.trading.client import TradingClient
from alpaca.trading.requests import GetOrdersRequest
from alpaca.trading.enums import QueryOrderStatus


def connect(api_key: str, secret_key: str, *, paper: bool = True) -> TradingClient:
    """建立並回傳 :class:`TradingClient`."""
    return TradingClient(api_key, secret_key, paper=paper)


def get_account_info(client: TradingClient) -> dict:
    """取得帳戶資訊，並轉為易讀格式。"""
    acct = client.get_account()
    buying_power = Decimal(str(acct.buying_power)).quantize(
        Decimal("0.01"), ROUND_HALF_UP
    )
    return {
        "status": acct.status,
        "equity": str(acct.equity),
        "buying_power": str(buying_power),
    }


def get_positions(client: TradingClient) -> List[dict]:
    """取得帳戶持倉資料列表，並過濾只回傳必要欄位。"""
    positions = client.get_all_positions()
    result = []
    for pos in positions:
        result.append(
            {
                "symbol": pos.symbol,
                "qty": str(getattr(pos, "qty", "")),
                "avg_entry_price": str(getattr(pos, "avg_entry_price", "")),
                "current_price": str(getattr(pos, "current_price", "")),
                "unrealized_pl": str(getattr(pos, "unrealized_pl", "")),
                "unrealized_plpc": str(getattr(pos, "unrealized_plpc", "")),
            }
        )
    return result


def get_trade_history(
    client: TradingClient,
    *,
    status: QueryOrderStatus = QueryOrderStatus.CLOSED,
    limit: Optional[int] = None,
) -> List[dict]:
    """取得歷史訂單（交易）紀錄，僅保留必要欄位。"""
    req = GetOrdersRequest(status=status, limit=limit)
    orders = client.get_orders(req)
    result = []
    for od in orders:
        result.append(
            {
                "symbol": od.symbol,
                "qty": str(getattr(od, "qty", "")),
                "side": getattr(od, "side", ""),
                "filled_avg_price": str(getattr(od, "filled_avg_price", "")),
                "status": getattr(od, "status", ""),
            }
        )
    return result
