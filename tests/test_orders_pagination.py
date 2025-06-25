import sys
import types
import importlib
from pathlib import Path

import pytest

root_path = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root_path))


def _setup_dummy_alpaca(monkeypatch):
    alp_client = types.ModuleType('alpaca.trading.client')
    alp_req = types.ModuleType('alpaca.trading.requests')
    alp_enum = types.ModuleType('alpaca.trading.enums')

    class DummyTradingClient:
        def __init__(self, *a, **k):
            pass

        def get_orders(self, req):
            return [{'id': i} for i in range(1, 11)]

    alp_client.TradingClient = DummyTradingClient
    alp_req.GetOrdersRequest = lambda **kw: kw
    alp_enum.QueryOrderStatus = types.SimpleNamespace(CLOSED='closed')

    monkeypatch.setitem(sys.modules, 'alpaca.trading.client', alp_client)
    monkeypatch.setitem(sys.modules, 'alpaca.trading.requests', alp_req)
    monkeypatch.setitem(sys.modules, 'alpaca.trading.enums', alp_enum)

    import account
    importlib.reload(account)
    return account


def test_get_trade_history_page(monkeypatch):
    acct = _setup_dummy_alpaca(monkeypatch)
    client = acct.connect('k', 's')
    orders = acct.get_trade_history(client, limit=3, page=2)
    assert orders == [{'id': 4}, {'id': 5}, {'id': 6}]


def test_api_orders_pagination(monkeypatch):
    pytest.importorskip('fastapi')

    acct = _setup_dummy_alpaca(monkeypatch)

    import config
    monkeypatch.setattr(config, 'ALPACA_API_KEY', 'key')
    monkeypatch.setattr(config, 'ALPACA_SECRET_KEY', 'secret')
    monkeypatch.setattr(config, 'USE_PAPER', True)

    import api
    importlib.reload(api)
    api._client = None

    from fastapi.testclient import TestClient
    client = TestClient(api.app)

    resp = client.get('/orders', params={'page': 2, 'limit': 3})
    assert resp.status_code == 200
    assert resp.json() == [{'id': 4}, {'id': 5}, {'id': 6}]

