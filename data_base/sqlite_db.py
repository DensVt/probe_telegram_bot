import sqlite3 as sq  # встроенная бд, не требуется отдельный сервер


# бот асинхронный, он использует 1 поток исполнения.
# функция, для создания бд, если она есть то идет подключение к ней
def sql_start():
    global base, cur
    base = sq.connect("pizza_cool.db")  # подключение к бд, если файла нет, он создастся
    cur = base.cursor()
    if base:
        print("Data base connected OK!")
    base.execute("CREATE TABLE IF NOT EXISTS menu(img TEXT, name TEXT PRIMARY KEY, description TEXT, price TEXT)")
    base.commit()  # сохранение изменений


# Запись в бд
async def sql_add_command(state):
    async with state.proxy() as data:
        cur.execute("INSERT INTO menu VALUES (?, ?, ?, ?", tuple(data.values()))
        base.commit()