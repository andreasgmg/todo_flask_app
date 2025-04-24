from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DATABASE = 'todo.db'

# Hjälpfunktion för att hämta databasanslutning
def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Hämta alla uppgifter
def fetch_all_tasks():
    with get_connection() as conn:
        return conn.execute('SELECT * FROM tasks').fetchall()

# Lägg till ny uppgift
def insert_task(task):
    with get_connection() as conn:
        conn.execute('INSERT INTO tasks (task, done) VALUES (?, ?)', (task, False))
        conn.commit()

# Uppdatera en uppgift
def update_task(id, new_task):
    with get_connection() as conn:
        conn.execute('UPDATE tasks SET task = ? WHERE id = ?', (new_task, id))
        conn.commit()

# Markera som klar
def mark_task_done(id):
    with get_connection() as conn:
        conn.execute('UPDATE tasks SET done = 1 WHERE id = ?', (id,))
        conn.commit()

# Ta bort en uppgift
def delete_task(id):
    with get_connection() as conn:
        conn.execute('DELETE FROM tasks WHERE id = ?', (id,))
        conn.commit()

# Hämta en uppgift
def get_task(id):
    with get_connection() as conn:
        return conn.execute('SELECT * FROM tasks WHERE id = ?', (id,)).fetchone()

@app.route('/')
def index():
    tasks = fetch_all_tasks()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add():
    task = request.form['task']
    if task:
        insert_task(task)
    return redirect(url_for('index'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    if request.method == 'POST':
        new_task = request.form['task']
        update_task(id, new_task)
        return redirect(url_for('index'))
    else:
        task = get_task(id)
        return render_template('edit.html', task=task)

@app.route('/done/<int:id>')
def done(id):
    mark_task_done(id)
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete(id):
    delete_task(id)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
