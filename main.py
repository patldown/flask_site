from flask import Flask, render_template, redirect
from flask import url_for, request, session, abort, flash
import os, db, datetime

### session allows session login to be read

app = Flask(__name__)

def list_generator(start_value = 1, count_value = 0, max_count = 13):
    '''
    Creates a lsit of numbers with a start and max iteration
    '''
    temp_list = []

    while count_value < max_count:
        temp_list.append(str(abs(start_value - count_value)))
        count_value+=1
    return temp_list

def extract_settings(file):
    handle = open(os.path.join(os.getcwd(), 'static', file), 'r', newline = '')
    reader = handle.readlines()
    handle.close()

    settings = {}

    for line in reader:
        line = line.split(':')
        settings[line[0].strip()] = line[1].strip()

    return settings
        

@app.route('/')
def index():
    settings = extract_settings('categories.settings')
    return render_template('index.html', settings = settings)

### Get and Post allows an if statement to allow for page reach dependant on inputs/or not
@app.route('/login', methods=['GET', 'POST'])
def login():
    settings = extract_settings('categories.settings')
    if request.method == 'POST':
        conn = db.initialize()
        login_info = db.db_Aquery(conn, 'USERS')
        db.deinitialize(conn)
        if request.form['username'].strip() in login_info:
            if request.form['password'] == login_info[request.form['username'].strip()][0]:
                session['logged_in'] = True
                session['username'] = login_info[request.form['username'].strip()][1] +\
                                      ' ' + login_info[request.form['username'].strip()][3]
                session['identifier'] = request.form['username'].strip()
                print(session['username'])
            else:
                flash('Login and/or Password is incorrect!')
                return render_template('login.html', settings = settings)
        else:
            flash('Login and/or Password is incorrect!')
            return render_template('login.html', settings = settings)
        return index()
    else:
        return render_template('login.html', settings = settings)

@app.route('/register', methods=['GET','POST'])
def register():
    settings = extract_settings('categories.settings')
    #construct months
    months = list_generator(start_value = 0, count_value = 1)

    #construct years
    years = list_generator(start_value = datetime.datetime.now().year, max_count = 100)

    #Main handler
    
    if request.method == 'POST':
        conn = db.initialize()
        login_info = db.db_Aquery(conn, 'USERS')
        db.deinitialize(conn)
        if request.form['username'].strip() in login_info:
            flash('Username already exists!')
            return render_template('register.html', months=months, years = years)
        else:
            if request.form['password'] != '' and request.form['FirstName'] != '' and\
               request.form['LastName'] != '' and request.form['Month'] != '' and\
               request.form['Year'] != '':
                #print('month', request.form['Month'])
                #print('Year', request.form['Year'])

                conn = db.initialize()
                db.add_user(conn, request.form['FirstName'], request.form['MiddleName'], \
                            request.form['LastName'], request.form['Month'], request.form['Year'], \
                            request.form['username'].strip(), request.form['password'])
                db.deinitialize(conn)
                
                flash('Success')
                session['logged_in'] = True
                session['username'] = request.form['FirstName'].strip() + ' ' + request.form['LastName'].strip()
                session['identifier'] = request.form['username'].strip()
                return index()
            else:
                flash('Missing required fields!')
                return render_template('register.html', months=months, years = years, settings = settings)
    else:
        return render_template('register.html', months=months, years = years, settings = settings)

@app.route("/profile/<username>")
def profile(username):
    settings = extract_settings('categories.settings')
    conn = db.initialize()
    login_info = db.db_Aquery(conn, 'USERS')
    db.deinitialize(conn)
    if session['identifier'] in login_info:
        email = session['identifier']
        firstname = login_info[session['identifier']][1]
        middlename = login_info[session['identifier']][2]
        lastname = login_info[session['identifier']][3]
        birthdate = str(login_info[session['identifier']][4]) + '/' + str(login_info[session['identifier']][5])
        return render_template('profile.html', email = email, firstname = firstname, middlename = middlename,\
                               lastname = lastname, birthdate = birthdate, settings = settings)

@app.route('/logout', methods=['GET'])
def logout():
    settings = extract_settings('categories.settings')
    session['logged_in'] = False
    session['username'] = None
    session['identifier'] = None
    return render_template('index.html', settings = settings)
        

@app.route('/articles')
def articles():
    settings = extract_settings('categories.settings')
    conn = db.initialize()
    articles = db.db_Aquery(conn, 'ARTICLES')
    db.deinitialize(conn)
    return render_template('articles.html', name = 'Articles', articles = articles, settings = settings)

@app.route('/profile/<username>/article_create')
def article_create(username):
    settings = extract_settings('categories.settings')
    return render_template('create_article.html', username = username, settings = settings)

@app.route('/articles/<category>')
def categories(category):
    settings = extract_settings('categories.settings')
    conn = db.initialize()
    articles = db.db_Aquery(conn, 'ARTICLES', add_criteria = [category, 6])
    db.deinitialize(conn)
    return render_template('articles.html', name = category, articles = articles, settings = settings)

@app.route('/articles/<category>/<article>')
def article(category, article):
    settings = extract_settings('categories.settings')
    conn = db.initialize()
    articles = db.db_Aquery(conn, 'ARTICLES')
    db.deinitialize(conn)
    for story in articles:
        if articles[story][0] == article:
            info = articles[story]
    return render_template('article.html', category = category, article = article, info = info, settings = settings)

app.secret_key = os.urandom(12)

