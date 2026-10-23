import time
from tkinter import *
from tkinter import ttk

import requests

crypto_data = [
    {"ID": "bitcoin", "symbol": "", "name": "", "current_price_usd": 0},
    {"ID": "ethereum", "symbol": "", "name": "", "current_price_usd": 0},
    {"ID": "tether", "symbol": "", "name": "", "current_price_usd": 0},
    {"ID": "binancecoin", "symbol": "", "name": "", "current_price_usd": 0},
    {"ID": "ripple", "symbol": "", "name": "", "current_price_usd": 0},
]

coin_id = ",".join(item["ID"] for item in crypto_data)

url = "https://api.coingecko.com/api/v3/coins/markets"

params = {
    "vs_currency": "usd",
    "ids": coin_id,
}

def response_data():
    btn.config(state=DISABLED)
    response = requests.get(url, params=params)
    response.raise_for_status()
    api_data = response.json()

    api_by_id = {coin["id"]: coin for coin in api_data}

    for item in crypto_data:
        coin = api_by_id.get(item["ID"])
        if coin:
            item["symbol"] = coin["symbol"]
            item["name"] = coin["name"]
            item["current_price_usd"] = coin["current_price"]

def clear_table():
    table.delete(*table.get_children())

def insert_table():
    for crypto in crypto_data:
        table.insert("", "end", values=(
            crypto["symbol"].upper(),
            crypto["name"],
            crypto["current_price_usd"]
        ))

def update_table():
    clear_table()
    response_data()
    label.config(text=time.strftime("%Y-%m-%d %H:%M:%S"))
    insert_table()
    btn.config(state=NORMAL)

def resize_columns(event):
    total_width = table.winfo_width()
    weights = [0.10, 0.20, 0.25]
    for col, w in zip(columns, weights):
        table.column(col, width=int(total_width * w), stretch=True)

root = Tk()
root.title("Курс Криптовалюты")

WIDTH, HEIGHT = 520, 300
screen_w = root.winfo_screenwidth()
screen_h = root.winfo_screenheight()
x = (screen_w - WIDTH) // 2
y = (screen_h - HEIGHT) // 2
root.geometry(f"{WIDTH}x{HEIGHT}+{x}+{y}")

columns = ("Символ", "Название", "Цена (USD)")
table = ttk.Treeview(root, columns=columns, show="headings")

for col in columns:
    table.column(col, anchor=CENTER)
    table.heading(col, text=col)

table.pack(padx=10, pady=10, fill="both", expand=True)

frame = Frame(root)
frame.pack(fill=X)

btn = Button(frame, text="Обновить данные", bg="green", command=update_table)
btn.pack(side=LEFT, padx=5)

label = Label(frame, text="Дата обновления")
label.pack(side=RIGHT, padx=5)

table.bind("<Configure>", resize_columns)

update_table()
root.mainloop()
