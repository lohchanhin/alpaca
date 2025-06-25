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
python -m dotenv run -- python invesment.py
```

或是自行將環境變數匯出後再啟動程式。

## 執行程式

```bash
python invesment.py
```

程式啟動後即可在圖形介面中輸入或確認 API 憑證，進行連線與下單測試。
