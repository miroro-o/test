import sqlite3

def create_connection():
    conn = sqlite3.connect('dishes.db')
    return conn

def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS dishes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            price REAL,
            category TEXT
        )
    ''')
    conn.commit()
    conn.close()


def add_dish(dish_name, description=None, price=None, category=None):
    # Добавляет новое блюдо в таблицу dishes
    conn = create_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO dishes (name, description, price, category)
        VALUES (?, ?, ?, ?)
    ''', (dish_name, description, price, category))
    
    conn.commit()
    conn.close()

def clear_database():
    """Удаляет все записи из всех таблиц в базе данных."""
    conn = create_connection()
    cursor = conn.cursor()

    # Получаем список всех таблиц
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    # Удаляем записи из каждой таблицы
    for table in tables:
        table_name = table[0]
        cursor.execute(f"DELETE FROM {table_name};")
        print(f"Записи из таблицы {table_name} удалены.")

    # Сохраняем изменения и закрываем соединение
    conn.commit()
    conn.close()
    

def drop_tables():
    """Удаляет все таблицы в базе данных."""
    conn = create_connection()
    cursor = conn.cursor()

    # Получаем список всех таблиц
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    # Удаляем каждую таблицу
    for table in tables:
        table_name = table[0]
        cursor.execute(f"DROP TABLE IF EXISTS {table_name};")
        print(f"Таблица {table_name} удалена.")

    # Сохраняем изменения и закрываем соединение
    conn.commit()
    conn.close()

def get_data():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM dishes;")  # Исправлено имя таблицы
    rows = cursor.fetchall()
    conn.close()
    return rows

