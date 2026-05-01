from flask import Flask, render_template, request, redirect, url_for, session, flash
import pyodbc

app = Flask(__name__)
app.secret_key = 'SecretKeyPassword'

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

# DONE
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
            conn.commit()
            conn.close()
            return render_template('contact.html', success="Message sent successfully!")
        else:
            cursor.execute("INSERT INTO contactForm (email, name, message) VALUES (?, ?, ?)", email, name, message)
            conn.commit()
            conn.close()
            return render_template('contact.html', success="Message sent successfully!")

    return render_template('contact.html')

# DONE
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
            flash('login')
            return redirect(url_for('index'))
        else:
            conn.close()
            return render_template('login.html', error="Incorrect username or password")
    return render_template('login.html')

# DONE
@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('logout')
    return redirect(url_for('index'))

# DONE
@app.route('/info-removal', methods=['GET', 'POST'])
def info_removal():
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
            return render_template('info-removal.html', success=success)
        else:
            conn.close()
            error = "Username or password is incorrect, or the user does not exist."
            return render_template('info-removal.html', error=error)
    return render_template('info-removal.html')

# DONE
@app.route('/create-account', methods=['GET', 'POST'])
def create_account():
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
            conn.close()
            error = "Username is already taken, please choose another."
            return render_template('create-account.html', error=error)
        else:
            cursor.execute("""
                INSERT INTO Users (userName, email, name, password, high_score)
                VALUES (?, ?, ?, ?, 0)
            """, username, email, name, password)
            conn.commit()
            conn.close()
            success = "Account created successfully!"
            return render_template('create-account.html', success=success)
    return render_template('create-account.html')

# DONE
@app.route('/game-settings', methods=['GET', 'POST'])
def game_settings():
    if request.method == 'POST':
        session['amount'] = request.form['amount']
        session['category'] = request.form['category']
        session['difficulty'] = request.form['difficulty']
        session['type'] = request.form['type']
        return redirect(url_for('play_game'))
    return render_template('game-settings.html')

# DONE
@app.route('/leaderboard')
def leaderboard():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT TOP 50 userName, high_score FROM Users WHERE high_score > 0 ORDER BY high_score DESC")
    players = cursor.fetchall()
    conn.close()
    return render_template('leaderboard.html', players=players)


# NEED TO DO
@app.route('/play-game', methods=['GET', 'POST'])
def play_game():
    return render_template('play-game.html')


# DONE
@app.route('/terms', methods=['GET', 'POST'])
def terms():
    return render_template('terms.html')

# DONE
@app.route('/priv-statement', methods=['GET', 'POST'])
def priv_statement():
    return render_template('priv-statement.html')

if __name__ == '__main__':
    app.run(debug=True)