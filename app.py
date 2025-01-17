from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
from functools import wraps
import os

app = Flask(__name__)
app.secret_key = 'kunci_rahasia_anda'

# Konfigurasi database filess.io
db_config = {
    'host': 'r4dnc.h.filess.io',
    'user': 'crypto_warmbasis',
    'password': 'd2dbf9edb95d7fc8c28b6ec3feb01fd716086831',
    'database': 'crypto_warmbasis',
    'port': '3305'
}

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            flash('Silakan login terlebih dahulu')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def get_db_connection():
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
        return None

@app.route('/')
def loading():
    return render_template('loading.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor(dictionary=True)
                cursor.execute("INSERT INTO login_user (username, password) VALUES (%s, %s)", 
                               (username, password))
                conn.commit()
                
                session['logged_in'] = True
                session['username'] = username
                session['user_id'] = cursor.lastrowid
                return redirect(url_for('sukses'))
            except Exception as e:
                print(f"Database error: {e}")
                flash('Terjadi kesalahan sistem')
            finally:
                cursor.close()
                conn.close()
        else:
            flash('Tidak dapat terhubung ke database')
    
    return render_template('halamanlogin.html')

@app.route('/sukses')
@login_required
def sukses():
    return render_template('sukses.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/grafik')
@login_required
def grafik():
    return render_template('grafik.html')

@app.route('/transaksi')
@login_required
def transaksi():
    return render_template('transaksi.html')

@app.route('/berita')
@login_required
def berita():
    return render_template('berita.html')

@app.route('/pengaturan')
@login_required
def pengaturan():
    return render_template('pengaturan.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
