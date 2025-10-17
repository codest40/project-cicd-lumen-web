from flask import Flask, render_template, request, redirect, url_for
from db import get_db_connection

app = Flask(__name__)

@app.route('/')
def login():
    return render_template('next.html')

@app.route('/login', methods=['POST'])
def handle_login():
    username = request.form.get('username')
    password = request.form.get('password')

    # Dummy auth for now
    if username == "admin" and password == "pass":
        return redirect(url_for('dashboard'))
    else:
        return render_template('log.html', error="Invalid credentials")

@app.route('/dashboard')
def dashboard():
    conn = get_db_connection()
    if conn:
        conn.close()
    return render_template('dashboard.html')

@app.route('/test')
def test_page():
    return render_template('test.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
