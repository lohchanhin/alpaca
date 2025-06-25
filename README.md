# Alpaca Paper Trading GUI

本專案提供一個簡易的圖形介面，方便在 Alpaca 的 Paper Trading 環境下測試下單與查詢功能。

## 安裝套件

確保已安裝 Python 3，接著於專案根目錄執行：

```bash
pip install -r requirements.txt
```

## 設定環境變數

請依照 `.env.example` 的格式新增一個 `.env` 檔案，內容範例如下：

```dotenv
APCA_API_KEY_ID=你的APIKey
APCA_API_SECRET_KEY=你的SecretKey
```

建議透過 `python-dotenv` 在執行程式前載入 `.env`：

```bash
python -m dotenv run -- python investment.py
```

或是自行將環境變數匯出後再啟動程式。

## 執行程式

```bash
python investment.py
```

程式啟動後即可在圖形介面中輸入或確認 API 憑證，進行連線與下單測試。

## 啟動 Web API

專案同時提供簡易的 FastAPI 介面，可透過 `uvicorn` 啟動：

```bash
<<<<<<< HEAD
python -m uvicorn api:app
=======
python -m dotenv run -- uvicorn api:app
>>>>>>> e2336abe90db43bbda8c325823b8a6a5ae28edff
```

若未使用 `python-dotenv`，請先於 `config.py` 中設定 API Key。

常用路由及用途簡述如下：

- `/`：回傳前端儀表板頁面。
- `/account`：取得帳戶資訊。
- `/positions`：列出目前持倉狀態。
- `/orders`：查詢歷史訂單。
- `/bots`：取得交易機器人清單。

## 執行單元測試

專案內含基本的單元測試，可在根目錄執行：

```bash
pytest
```
