from flask import Flask, render_template, request, redirect, url_for
import pyodbc

app = Flask(__name__)

def get_db():
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=localhost;'
        'DATABASE=IS117Project;'
        'Trusted_Connection=yes;'  
    )
    return conn

@app.route('/')
def index():
    return render_template('index.html')

# @app.route('/contact', methods=['GET', 'POST'])
# def contact():
#     if request.method == 'POST':





@app.route('/info-removal', methods=['GET', 'POST'])
def contact():
    success = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM Users WHERE userName = ?", username)
        existing_user = cursor.fetchone()
    
        if existing_user:
            cursor.execute("UPDATE Users SET high_score = 0 WHERE userName = ?", username)
            success = "Information successfully removed."
            




@app.route('/create-account', methods=['GET', 'POST'])
def create_account():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        name = request.form['name']
        password = request.form['password']

        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM Users WHERE userName = ?", username)
        existing_user = cursor.fetchone()

        if existing_user:
            error = "Username is already taken, please choose another."
        else:
            cursor.execute("""
                INSERT INTO Users (userName, email, name, password, high_score)
                VALUES (?, ?, ?, ?, 0)
            """, username, email, name, password)
            conn.commit()
            conn.close()

            return render_template('create-account.html', success=True)
        conn.close()

    return render_template('create-account.html', error=error)

if __name__ == '__main__':
    app.run(debug=True)


# **3. Folder structure you should have:**
# project/
# │
# ├── app.py
# ├── stylesheet.css
# ├── templates/
# │   ├── index.html
# │   ├── contact.html
# │   ├── terms.html
# │   └── create-account.html
# └── static/
#     └── stylesheet.css