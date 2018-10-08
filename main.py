from flask import Flask, render_template, redirect
from flask import url_for, request, session, abort, flash

### session allows session login to be read

app = Flask(__name__)

@app.route('/')
def index():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    if request.form['password'] == 'password' and request.form['username'] == 'admin':
        session['logged_in'] = True
    else:
        flash('wrong password!')
    return index()

@app.route('/articles')
def articles():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('articles.html')

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        conn.close()

app.secret_key = os.urandom(12)

