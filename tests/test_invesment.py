import importlib
import sys
import types
from types import SimpleNamespace
from pathlib import Path

import pytest

class DummyVar:
    def __init__(self, value=""):
        self.value = value
    def get(self):
        return self.value
    def set(self, value):
        self.value = value

class DummyWidget:
    def __init__(self, *args, **kwargs):
        pass
    def pack(self, *args, **kwargs):
        pass
    def grid(self, *args, **kwargs):
        pass
    def configure(self, *args, **kwargs):
        pass
    def insert(self, *args, **kwargs):
        pass
    def delete(self, *args, **kwargs):
        pass

class DummyTk(DummyWidget):
    def title(self, *args, **kwargs):
        pass
    def geometry(self, *args, **kwargs):
        pass
    def resizable(self, *args, **kwargs):
        pass
    def destroy(self):
        pass

@pytest.fixture
def invesment(monkeypatch):
    root_path = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(root_path))
    tk = types.ModuleType('tkinter')
    ttk = types.ModuleType('ttk')
    tk.Tk = DummyTk
    tk._default_root = None
    tk.StringVar = lambda master=None, value="": DummyVar(value)
    tk.BooleanVar = lambda master=None, value=False: DummyVar(value)
    tk.Text = DummyWidget
    tk.END = "end"
    ttk.LabelFrame = DummyWidget
    ttk.Label = DummyWidget
    ttk.Entry = DummyWidget
    ttk.Checkbutton = DummyWidget
    ttk.Button = DummyWidget
    tk.ttk = ttk
    tk.messagebox = types.SimpleNamespace(
        showwarning=lambda *a, **k: None,
        showinfo=lambda *a, **k: None,
        showerror=lambda *a, **k: None,
    )
    sys.modules['tkinter'] = tk
    sys.modules['tkinter.ttk'] = ttk
    sys.modules['tkinter.messagebox'] = tk.messagebox

    alp_client = types.ModuleType('alpaca.trading.client')
    alp_req = types.ModuleType('alpaca.trading.requests')
    alp_enum = types.ModuleType('alpaca.trading.enums')

    class DummyTradingClient:
        def __init__(self, *a, **k):
            pass
        def get_account(self):
            return SimpleNamespace(status='ACTIVE', buying_power='1000', equity='1000')
        def submit_order(self, req):
            return SimpleNamespace(id='order123')

    alp_client.TradingClient = DummyTradingClient
    alp_req.MarketOrderRequest = lambda **kw: kw
    alp_enum.OrderSide = SimpleNamespace(BUY='buy')
    alp_enum.TimeInForce = SimpleNamespace(DAY='day')

    sys.modules['alpaca.trading.client'] = alp_client
    sys.modules['alpaca.trading.requests'] = alp_req
    sys.modules['alpaca.trading.enums'] = alp_enum

    module = importlib.import_module('investment')
    return module


def test_connect_account_success(monkeypatch, invesment):
    inv = invesment
    inv.api_key_var.get = lambda: "key"
    inv.secret_key_var.get = lambda: "secret"
    inv.use_paper_var.get = lambda: True

    monkeypatch.setattr(inv.messagebox, 'showinfo', lambda *a, **k: None)
    monkeypatch.setattr(inv.messagebox, 'showwarning', lambda *a, **k: None)
    monkeypatch.setattr(inv.messagebox, 'showerror', lambda *a, **k: None)
    called = {}
    def fake_show(text):
        called['text'] = text
    monkeypatch.setattr(inv, '_show_result', fake_show)

    inv.connect_account()

    assert inv.client is not None
    assert '帳戶連線成功' in called['text']


def test_connect_account_missing_key(monkeypatch, invesment):
    inv = invesment
    inv.api_key_var.get = lambda: ""
    inv.secret_key_var.get = lambda: "secret"
    inv.use_paper_var.get = lambda: True

    called = {}
    def fake_warning(title, msg):
        called['msg'] = msg
    monkeypatch.setattr(inv.messagebox, 'showwarning', fake_warning)

    inv.connect_account()

    assert '請輸入完整的 API Key' in called['msg']


def test_place_order_success(monkeypatch, invesment):
    inv = invesment
    inv.client = types.SimpleNamespace(submit_order=lambda req: SimpleNamespace(id='ok'))
    inv.symbol_var.get = lambda: 'AAPL'
    inv.qty_var.get = lambda: '1'

    called = {}
    def fake_info(title, msg):
        called['msg'] = msg
    monkeypatch.setattr(inv.messagebox, 'showinfo', fake_info)

    inv.place_order()

    assert '訂單已提交' in called['msg']


def test_place_order_no_client(monkeypatch, invesment):
    inv = invesment
    inv.client = None
    called = {}
    def fake_warning(title, msg):
        called['msg'] = msg
    monkeypatch.setattr(inv.messagebox, 'showwarning', fake_warning)

    inv.place_order()

    assert '請先成功連線帳戶' in called['msg']
