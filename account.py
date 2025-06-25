from __future__ import annotations

"""Alpaca 帳戶相關操作模組。"""

from decimal import Decimal, ROUND_HALF_UP
from typing import List, Optional

from alpaca.trading.client import TradingClient
from alpaca.trading.requests import GetOrdersRequest
from alpaca.trading.enums import OrderStatus


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


def get_positions(client: TradingClient):
    """取得帳戶持倉資料列表。"""
    return client.get_all_positions()


def get_trade_history(
    client: TradingClient,
    *,
    status: OrderStatus = OrderStatus.CLOSED,
    limit: Optional[int] = None,
) -> list:
    """取得歷史訂單（交易）紀錄。"""
    req = GetOrdersRequest(status=status, limit=limit)
    return client.get_orders(req)
