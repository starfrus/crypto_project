from tkinter import *
from tkinter import ttk

crypto_data = [
    {"ID": "", "symbol": "", "name": "", "image": "", "current_price_usd": 0},
]

def resize_columns(event):
    total_width = table.winfo_width()
    weights = [0.08, 0.30, 0.22, 0.15, 0.25]
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

columns = ("ID", "Название", "Иконка", "Символ", "Цена (USD)")
table = ttk.Treeview(root, columns=columns, show="headings")

for col in columns:
    table.column(col, anchor=CENTER)
    table.heading(col, text=col)

for crypto in crypto_data:
    table.insert("", "end", values=(
        crypto["ID"],
        crypto["symbol"],
        crypto["name"],
        crypto["image"],
        crypto["current_price_usd"]
    ))

table.pack(padx=10, pady=10, fill="both", expand=True)

update_btn = Button(root, text="Обновить курсы", bg="green")
update_btn.pack(pady=5)

table.bind("<Configure>", resize_columns)

root.mainloop()
