from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3 
#from datetime import timedelta

app = Flask(__name__)
#app.session.permanent_lifetime(timedelta(days=7))  # Set session lifetime to 7 days

# Fungsi untuk menghubungkan ke database
def get_db_connection():
    conn = sqlite3.connect('data.db')
    conn.row_factory = sqlite3.Row  # Ini memungkinkan kita untuk mengakses kolom menggunakan nama
    return conn

# Rute halaman utama
@app.route('/')
def index():
    conn = get_db_connection()
    data = conn.execute('SELECT * FROM data').fetchall()
    conn.close()
    return render_template('index.html', data=data)

# Rute untuk menambahkan data baru
@app.route('/add', methods=('GET', 'POST'))
def add():
    if request.method == 'POST':
        username = request.form['username']
        surname = request.form['surname']
        date = request.form['date']
        password = request.form['password']
        conn = get_db_connection()
        conn.execute('INSERT INTO data (username, surname, date, password) VALUES (?, ?, ?, ?)', (username, surname, date, password))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('add.html')

# Rute untuk menghapus data
@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM data WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# Inisialisasi database jika belum ada
def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            surname TEXT NOT NULL,
            date INTEGER NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.close()

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
