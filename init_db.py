import sqlite3

conn = sqlite3.connect('todo.db')
c = conn.cursor()
c.execute('''
    CREATE TABLE tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task TEXT NOT NULL,
        done BOOLEAN NOT NULL CHECK (done IN (0, 1))
    )
''')
conn.commit()
conn.close()