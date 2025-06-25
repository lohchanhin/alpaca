import sys
from pathlib import Path
import pytest

root_path = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root_path))

import robots


def test_get_bots_from_file(tmp_path, monkeypatch):
    data_file = tmp_path / "robots.json"
    data_file.write_text('[{"name": "bot1"}]', encoding="utf-8")

    monkeypatch.setattr(robots, "_ROBOTS_FILE", data_file)
    robots._bots = None

    bots = robots.get_bots()
    assert bots == [{"name": "bot1"}]


def test_api_get_bots(tmp_path):
    pytest.importorskip("fastapi")
    pytest.importorskip("alpaca")
    from fastapi.testclient import TestClient
    import importlib
    api = importlib.import_module("api")

    data_file = tmp_path / "robots.json"
    data_file.write_text('[{"name": "api_bot"}]', encoding="utf-8")

    import robots as robots_mod
    robots_mod._ROBOTS_FILE = data_file
    robots_mod._bots = None

    client = TestClient(api.app)
    resp = client.get("/bots")
    assert resp.status_code == 200
    assert resp.json() == [{"name": "api_bot"}]
