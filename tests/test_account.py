import importlib
import sys
import types
from types import SimpleNamespace
from pathlib import Path
import pytest

root_path = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root_path))


@pytest.fixture
def account_module(monkeypatch):
    alp_client = types.ModuleType('alpaca.trading.client')
    alp_req = types.ModuleType('alpaca.trading.requests')
    alp_enum = types.ModuleType('alpaca.trading.enums')
    alp_client.TradingClient = object
    alp_req.GetOrdersRequest = lambda **kw: kw
    alp_enum.QueryOrderStatus = SimpleNamespace(CLOSED='closed')
    monkeypatch.setitem(sys.modules, 'alpaca.trading.client', alp_client)
    monkeypatch.setitem(sys.modules, 'alpaca.trading.requests', alp_req)
    monkeypatch.setitem(sys.modules, 'alpaca.trading.enums', alp_enum)
    sys.modules.pop('account', None)
    mod = importlib.import_module('account')
    yield mod
    sys.modules.pop('account', None)


def test_get_positions_filtered(account_module):
    account = account_module

    class DummyClient:
        def get_all_positions(self):
            return [
                SimpleNamespace(
                    symbol='AAPL',
                    qty='10',
                    avg_entry_price='100',
                    current_price='110',
                    unrealized_pl='10',
                    unrealized_plpc='0.1',
                    ignore='x',
                )
            ]

    result = account.get_positions(DummyClient())
    assert result == [
        {
            'symbol': 'AAPL',
            'qty': '10',
            'avg_entry_price': '100',
            'current_price': '110',
            'unrealized_pl': '10',
            'unrealized_plpc': '0.1',
        }
    ]


def test_get_trade_history_filtered(account_module):
    account = account_module

    class DummyClient:
        def get_orders(self, req):
            return [
                SimpleNamespace(
                    symbol='AAPL',
                    qty='1',
                    side='buy',
                    filled_avg_price='105',
                    status='filled',
                    other='y',
                )
            ]

    result = account.get_trade_history(DummyClient(), limit=1)
    assert result == [
        {
            'symbol': 'AAPL',
            'qty': '1',
            'side': 'buy',
            'filled_avg_price': '105',
            'status': 'filled',
        }
    ]
