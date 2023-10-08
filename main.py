import tkinter as tk
import sqlite3
from tkinter import filedialog
import csv

# Определение класса Item (Товар), который содержит информацию о подарках
class Item:
    def __init__(self, group, item_type, price, amount):
        self.group = group
        self.item_type = item_type
        self.price = price
        self.amount = amount

items = []

# Функция для записи данных в базу данных
def write_to_database():
    conn = sqlite3.connect('gifts_db.sqlite')
    cursor = conn.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS items (group_name TEXT, item_type TEXT, price REAL, amount INTEGER)")

    for item in items:
        cursor.execute("INSERT INTO items (group_name, item_type, price, amount) VALUES (?, ?, ?, ?)",
                       (item.group, item.item_type, item.price, item.amount))

    conn.commit()
    conn.close()

# Функция для просмотра данных в базе
def view_database():
    conn = sqlite3.connect('gifts_db.sqlite')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM items")
    data = cursor.fetchall()

    print('------ Данные в базе данных -------')
    for row in data:
        print(f'Группа: {row[0]}, Тип: {row[1]}, Прайс: {row[2]}, Количество: {row[3]}')

    conn.close()

# Функция для обработки нажатия кнопки "Добавить в базу"
def add_to_database():
    group = entry_group.get()
    item_type = entry_item_type.get()
    price = entry_price.get()
    amount = entry_amount.get()

    if not (group and item_type and price and amount):
        # Проверка на пустые поля
        print("Все поля должны быть заполнены")
        return

    try:
        price = float(price)
        amount = int(amount)
    except ValueError:
        print("Неверный формат числа")
        return

    item = Item(group, item_type, price, amount)
    items.append(item)

    print_items_with_positive_amount()

    entry_group.delete(0, tk.END)
    entry_item_type.delete(0, tk.END)
    entry_price.delete(0, tk.END)
    entry_amount.delete(0, tk.END)

def print_items_with_positive_amount():
    text_area.delete("1.0", "end")
    text_area.insert('end', "------ Доступные товары ------\n")
    for item in items:
        if item.amount > 0:
            text_area.insert('end', f"Группа: {item.group}, Тип: {item.item_type}, Прайс: {item.price}, Количество: {item.amount}\n")

def print_items_with_not_positive_amount():
    text_area.delete("1.0", "end")
    text_area.insert('end', "------ Недоступные товары -------\n")
    for item in items:
        if item.amount <= 0:
            text_area.insert('end', f"Группа: {item.group}, Тип: {item.item_type}, Количество: {item.amount}\n")

def load_from_csv():
    global items
    file_path = filedialog.askopenfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
    if file_path:
        with open(file_path, newline='') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                group = row[0]
                item_type = row[1]
                price = float(row[2])
                amount = int(row[3])
                item = Item(group, item_type, price, amount)
                items.append(item)

def exit_program():
    write_to_database()
    root.destroy()

root = tk.Tk()
root.geometry("800x600")

text_area = tk.Text(root)
text_area.pack(fill=tk.BOTH, expand=True)

button_available = tk.Button(root, text="Доступные товары", command=print_items_with_positive_amount)
button_not_available = tk.Button(root, text="Недоступные товары", command=print_items_with_not_positive_amount)
button_add_to_db = tk.Button(root, text="Добавить в базу", command=add_to_database)
button_load_from_csv = tk.Button(root, text="Загрузить из CSV", command=load_from_csv)
button_view_db = tk.Button(root, text="Просмотреть базу данных", command=view_database)
button_exit = tk.Button(root, text="Выход", command=exit_program)

button_available.pack(side=tk.LEFT, padx=10, pady=10)
button_not_available.pack(side=tk.LEFT, padx=10, pady=10)
button_add_to_db.pack(side=tk.LEFT, padx=10, pady=10)
button_load_from_csv.pack(side=tk.LEFT, padx=10, pady=10)
button_view_db.pack(side=tk.LEFT, padx=10, pady=10)
button_exit.pack(side=tk.LEFT, padx=10, pady=10)

label_group = tk.Label(root, text="Группа:")
label_group.pack()

label_item_type = tk.Label(root, text="Тип:")
label_item_type.pack()

label_price = tk.Label(root, text="Цена:")
label_price.pack()

label_amount = tk.Label(root, text="Количество:")
label_amount.pack()

entry_group = tk.Entry(root)
entry_group.pack()

entry_item_type = tk.Entry(root)
entry_item_type.pack()

entry_price = tk.Entry(root)
entry_price.pack()

entry_amount = tk.Entry(root)
entry_amount.pack()

root.mainloop()
