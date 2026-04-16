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




@app.route('/contact', methods=['GET', 'POST'])
def contact():
    return render_template('contact.html')







# working on
@app.route('/login', methods=['GET', 'POST'])
def login():
    # return render_template('login.html')
    success = None
    failed = None
    login = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM Users WHERE userName = ? AND password = ?", username, password)
        existing_user = cursor.fetchone()


        if existing_user:
            success = "Welcome, " + name + ", you're login in."
            login = True
            # other logic to show name on screen somewhere for the rest of session
            conn.close()
            return render_template('/', success=True)
        else:
            failed = "Incorrect username or password, maybe create an account below."
            conn.close()
            return render_template('login.html')
    return render_template('login.html')





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
        
    failed = "No username or password incorrect, or user does not exist."
    return render_template('info-removal.html', failed=True)

            

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