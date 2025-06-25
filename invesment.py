# -*- coding: utf-8 -*-
"""
Alpaca Paper Trading GUI 測試工具（修正版 2025-06-25）
----------------------------------------------------
• 輸入 API Key / Secret Key，可：
  1) 測試連線（顯示帳戶狀態與 Buying Power）
  2) 在 Paper 環境下市價買入指定股票
----------------------------------------------------
依賴套件：pip install alpaca-py==0.14
"""

from decimal import Decimal, ROUND_HALF_UP
import tkinter as tk
from tkinter import ttk, messagebox

from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce

import account

# ────────────────────────────────────────────────
# 0. 清理殘留的 default root（Spyder 反覆執行時必要）
# ────────────────────────────────────────────────
if tk._default_root is not None:
    try:
        tk._default_root.destroy()
    except tk.TclError:
        pass

# ────────────────────────────────────────────────
# 1. 建立主視窗
# ────────────────────────────────────────────────
root = tk.Tk()
root.title("Alpaca Paper Trading GUI 測試工具")
root.geometry("520x430")
root.resizable(False, False)

# ────────────────────────────────────────────────
# 2. 變數定義（全數指定 master=root）
# ────────────────────────────────────────────────
api_key_var    = tk.StringVar(master=root)
secret_key_var = tk.StringVar(master=root)
use_paper_var  = tk.BooleanVar(master=root, value=True)

symbol_var = tk.StringVar(master=root, value="AAPL")
qty_var    = tk.StringVar(master=root, value="1")

client: TradingClient | None = None  # 連線成功後賦值

# ────────────────────────────────────────────────
# 3. 功能函式
# ────────────────────────────────────────────────
def connect_account() -> None:
    """建立 TradingClient 並取得帳戶資訊。"""
    global client

    api_key = api_key_var.get()
    secret_key = secret_key_var.get()
    paper_mode = use_paper_var.get()

    if api_key == "" or secret_key == "":
        messagebox.showwarning("缺少憑證", "請輸入完整的 API Key 與 Secret Key！")
        return

    try:
        client = account.connect(api_key, secret_key, paper=paper_mode)
        info = account.get_account_info(client)

        msg = (
            "帳戶連線成功！\n"
            f"狀態：{info['status']}\n"
            f"總淨值（Equity）：${info['equity']}\n"
            f"可用買進金額（Buying Power）：${info['buying_power']}"
        )
        _show_result(msg)
        messagebox.showinfo("成功", "帳戶連線並取得資訊成功！")
    except Exception as exc:
        client = None
        _show_result(f"連線失敗：{exc}")
        messagebox.showerror("連線失敗", f"無法連線至 Alpaca：\n{exc}")

def place_order() -> None:
    """以市價單買入指定股票（僅 Paper）。"""
    if client is None:
        messagebox.showwarning("尚未連線", "請先成功連線帳戶再下單！")
        return

    symbol = symbol_var.get().strip().upper()
    qty    = qty_var.get().strip()

    if symbol == "" or qty == "":
        messagebox.showwarning("缺少參數", "請填寫股票代號與數量！")
        return
    if not qty.isdigit() or int(qty) <= 0:
        messagebox.showwarning("數量錯誤", "數量必須為正整數！")
        return

    try:
        req = MarketOrderRequest(
            symbol=symbol,
            qty=int(qty),
            side=OrderSide.BUY,
            time_in_force=TimeInForce.DAY,
        )
        order = client.submit_order(req)
        messagebox.showinfo("下單成功", f"訂單已提交！\n訂單 ID：{order.id}")
    except Exception as exc:
        messagebox.showerror("下單失敗", f"發生錯誤：\n{exc}")

def _show_result(text: str) -> None:
    """在下方訊息框顯示文字。"""
    result_text.configure(state="normal")
    result_text.delete("1.0", tk.END)
    result_text.insert(tk.END, text)
    result_text.configure(state="disabled")

# ────────────────────────────────────────────────
# 4. 介面佈局
# ────────────────────────────────────────────────
# 4-1 API 憑證
frame_api = ttk.LabelFrame(root, text="API 憑證設定", padding=10)
frame_api.pack(fill="x", padx=12, pady=8)

ttk.Label(frame_api, text="API Key:").grid(row=0, column=0, sticky="w")
ttk.Entry(frame_api, textvariable=api_key_var, width=60).grid(
    row=0, column=1, padx=4, pady=4, sticky="w"
)

ttk.Label(frame_api, text="Secret Key:").grid(row=1, column=0, sticky="w")
ttk.Entry(frame_api, textvariable=secret_key_var, width=60, show="*").grid(
    row=1, column=1, padx=4, pady=4, sticky="w"
)

ttk.Checkbutton(
    frame_api, text="使用 Paper 交易環境（測試）", variable=use_paper_var
).grid(row=2, column=0, columnspan=2, sticky="w", pady=(4, 0))

ttk.Button(
    frame_api, text="連線並測試憑證", command=connect_account
).grid(row=3, column=0, columnspan=2, pady=10)

# 4-2 結果區
frame_result = ttk.LabelFrame(root, text="帳戶資訊 / 系統訊息", padding=10)
frame_result.pack(fill="both", expand=True, padx=12, pady=8)

result_text = tk.Text(frame_result, height=8, state="disabled")
result_text.pack(fill="both", expand=True)

# 4-3 下單區
frame_order = ttk.LabelFrame(root, text="市價下單（Paper 測試）", padding=10)
frame_order.pack(fill="x", padx=12, pady=8)

ttk.Label(frame_order, text="股票代號:").grid(row=0, column=0, sticky="w")
ttk.Entry(frame_order, textvariable=symbol_var, width=15).grid(
    row=0, column=1, padx=4, pady=4, sticky="w"
)

ttk.Label(frame_order, text="數量:").grid(row=0, column=2, sticky="w")
ttk.Entry(frame_order, textvariable=qty_var, width=10).grid(
    row=0, column=3, padx=4, pady=4, sticky="w"
)

ttk.Button(frame_order, text="立即下單", command=place_order).grid(
    row=0, column=4, padx=8, pady=4
)

# 4-4 版權標示
ttk.Label(
    root, text="© 2025 wwwch • Alpaca GUI 測試工具", anchor="center"
).pack(fill="x", pady=(4, 8))

# ────────────────────────────────────────────────
# 5. 主循環
# ────────────────────────────────────────────────
if __name__ == "__main__":
    root.mainloop()
