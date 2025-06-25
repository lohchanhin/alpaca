from decimal import Decimal, ROUND_HALF_UP
from alpaca.trading.client import TradingClient


def connect(api_key: str, secret_key: str, paper: bool) -> tuple[TradingClient, str]:
    """建立 TradingClient 並回傳帳戶資訊文字。"""
    client = TradingClient(api_key, secret_key, paper=paper)
    acct = client.get_account()

    buying_power = Decimal(str(acct.buying_power)).quantize(
        Decimal("0.01"), ROUND_HALF_UP
    )
    msg = (
        f"帳戶連線成功！\n"
        f"狀態：{acct.status}\n"
        f"總淨值（Equity）：${acct.equity}\n"
        f"可用買進金額（Buying Power）：${buying_power}"
    )
    return client, msg
