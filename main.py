from tkinter import *
from tkinter import ttk

import requests

crypto_data = [
    {"ID": "bitcoin", "symbol": "", "name": "", "image": "", "current_price_usd": 0},
    {"ID": "ethereum", "symbol": "", "name": "", "image": "", "current_price_usd": 0},
    {"ID": "tether", "symbol": "", "name": "", "image": "", "current_price_usd": 0},
    {"ID": "binancecoin", "symbol": "", "name": "", "image": "", "current_price_usd": 0},
    {"ID": "ripple", "symbol": "", "name": "", "image": "", "current_price_usd": 0},
]

coin_id = ",".join(item["ID"] for item in crypto_data)

url = "https://api.coingecko.com/api/v3/coins/markets"

params = {
    "vs_currency": "usd",
    "ids": coin_id,
}

def response_data():
    response = requests.get(url, params=params)
    response.raise_for_status()
    api_data = response.json()

    # Строим словарь для быстрого поиска по ID
    api_by_id = {coin["id"]: coin for coin in api_data}

    # Заполняем вашу структуру
    for item in crypto_data:
        coin = api_by_id.get(item["ID"])
        if coin:
            item["symbol"] = coin["symbol"]
            item["name"] = coin["name"]
            item["image"] = coin["image"]
            item["current_price_usd"] = coin["current_price"]


def resize_columns(event):
    total_width = table.winfo_width()
    weights = [0.20, 0.10, 0.20, 0.10, 0.25]
    for col, w in zip(columns, weights):
        table.column(col, width=int(total_width * w), stretch=True)

root = Tk()
root.title("Курс Криптовалюты")

WIDTH, HEIGHT = 520, 450
screen_w = root.winfo_screenwidth()
screen_h = root.winfo_screenheight()
x = (screen_w - WIDTH) // 2
y = (screen_h - HEIGHT) // 2
root.geometry(f"{WIDTH}x{HEIGHT}+{x}+{y}")

columns = ("ID", "Символ", "Название", "Иконка", "Цена (USD)")
table = ttk.Treeview(root, columns=columns, show="headings")

for col in columns:
    table.column(col, anchor=CENTER)
    table.heading(col, text=col)

table.pack(padx=10, pady=10, fill="both", expand=True)

update_btn = Button(root, text="Обновить курсы", bg="green")
update_btn.pack(pady=5)

table.bind("<Configure>", resize_columns)

root.mainloop()
