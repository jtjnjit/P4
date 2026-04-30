from flask import Flask, render_template, request, redirect, url_for, session, flash
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


# check should be good
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        email = request.form['email']
        message = request.form['message']

        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM Users WHERE userName = ?", username)
        existing_user = cursor.fetchone()

        if existing_user:
            cursor.execute("INSERT INTO contactForm (userName, email, name, message) VALUES (?, ?, ?, ?)", username, email, name, message)
        else:
            cursor.execute("INSERT INTO contactForm (email, name, message) VALUES (?, ?, ?)", email, name, message)

    return render_template('contact.html')




# working on
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM Users WHERE userName = ? AND password = ?", username, password)
        existing_user = cursor.fetchone()

        if existing_user:
            session['username'] = username
            conn.close()
            flash('welcomeMessage')
            return redirect(url_for('index'))
        else:
            conn.close()
            return render_template('login.html', failed=True)
    return render_template('login.html')

# should be good
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


# should be good check
@app.route('/info-removal', methods=['GET', 'POST'])
def info_removal():
    success = None
    failed = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM Users WHERE userName = ? AND password = ?", username, password)
        existing_user = cursor.fetchone()
    
        if existing_user:
            cursor.execute("UPDATE Users SET high_score = 0 WHERE userName = ?", username)
            conn.commit()
            conn.close()
            success = "Information successfully removed."
            return render_template('info-removal.html', success=True)
        else:
            failed = "No username or password incorrect, or user does not exist."
            return render_template('info-removal.html', failed=True)
    return render_template('info-removal.html')



# done
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


@app.route('/play-game', methods=['GET', 'POST'])
def play_game():
    return render_template('play-game.html')

@app.route('/game-settings', methods=['GET', 'POST'])
def game_settings():
    return render_template('game-settings.html')

@app.route('/leaderboard', methods=['GET', 'POST'])
def leaderboard():
    return render_template('leaderboard.html')

@app.route('/terms', methods=['GET', 'POST'])
def terms():
    return render_template('terms.html')

@app.route('/priv-statement', methods=['GET', 'POST'])
def priv_statement():
    return render_template('priv-statement.html')


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