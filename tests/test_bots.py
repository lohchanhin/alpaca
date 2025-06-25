import sys
from pathlib import Path
import pytest

root_path = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root_path))

import robots


def test_get_bots_from_file(tmp_path, monkeypatch):
    data_file = tmp_path / "robots.json"
    data_file.write_text('[{"name": "bot1", "strategy": "s", "enabled": true, "params": {"a": 1}}]', encoding="utf-8")

    monkeypatch.setattr(robots, "_ROBOTS_FILE", data_file)
    robots._bots = None

    bots = robots.get_bots()
    assert bots == [{"name": "bot1", "strategy": "s", "enabled": True, "params": {"a": 1}}]


def test_api_get_bots(tmp_path):
    pytest.importorskip("fastapi")
    pytest.importorskip("alpaca")
    from fastapi.testclient import TestClient
    import importlib
    api = importlib.import_module("api")

    data_file = tmp_path / "robots.json"
    data_file.write_text('[{"name": "api_bot", "strategy": "st", "enabled": false, "params": {}}]', encoding="utf-8")

    import robots as robots_mod
    robots_mod._ROBOTS_FILE = data_file
    robots_mod._bots = None

    client = TestClient(api.app)
    resp = client.get("/bots")
    assert resp.status_code == 200
    assert resp.json() == [{"name": "api_bot", "strategy": "st", "enabled": False, "params": {}}]


def test_bot_crud(tmp_path, monkeypatch):
    data_file = tmp_path / "robots.json"
    monkeypatch.setattr(robots, "_ROBOTS_FILE", data_file)
    robots._bots = None

    robots.add_bot({"name": "one", "strategy": "s1", "enabled": True, "params": {}})
    robots.add_bot({"name": "two", "strategy": "s2", "enabled": False, "params": {"x": 1}})
    assert robots.get_bots() == [
        {"name": "one", "strategy": "s1", "enabled": True, "params": {}},
        {"name": "two", "strategy": "s2", "enabled": False, "params": {"x": 1}},
    ]

    robots.update_bot(1, {"name": "updated", "enabled": True})
    updated = robots.get_bots()[1]
    assert updated["name"] == "updated"
    assert updated["enabled"] is True
    assert updated["strategy"] == "s2"
    assert updated["params"] == {"x": 1}

    robots.delete_bot(0)
    assert robots.get_bots() == [
        {"name": "updated", "strategy": "s2", "enabled": True, "params": {"x": 1}}
    ]


def test_api_bot_crud(tmp_path):
    pytest.importorskip("fastapi")
    pytest.importorskip("alpaca")
    from fastapi.testclient import TestClient
    import importlib
    api = importlib.import_module("api")

    data_file = tmp_path / "robots.json"
    import robots as robots_mod
    robots_mod._ROBOTS_FILE = data_file
    robots_mod._bots = None

    client = TestClient(api.app)

    resp = client.post("/bots", json={"name": "bot", "strategy": "s", "enabled": False, "params": {}})
    assert resp.status_code == 200
    assert robots_mod.get_bots() == [{"name": "bot", "strategy": "s", "enabled": False, "params": {}}]

    resp = client.put("/bots/0", json={"enabled": True})
    assert resp.status_code == 200
    assert robots_mod.get_bots()[0]["enabled"] is True

    resp = client.delete("/bots/0")
    assert resp.status_code == 200
    assert robots_mod.get_bots() == []
