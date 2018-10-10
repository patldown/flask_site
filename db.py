import sqlite3

def initialize():
    conn = sqlite3.connect('test.db')
    print('success')
    return conn

###
def create_table_users(conn):
    '''
    This script sets up the user table in the database.
    '''
    
    try:
        conn.execute('''CREATE TABLE USERS
                 (EMAILADDRESS TEXT PRIMARY KEY     NOT NULL,
                 PASSWORD           TEXT    NOT NULL,
                 FIRSTNAME           TEXT    NOT NULL,
                 MIDDLENAME           TEXT    NOT NULL,
                 LASTNAME           TEXT    NOT NULL,
                 MONTH            INT     NOT NULL,
                 YEAR            INT     NOT NULL);''')
        print("Table created successfully")
    except:
        print('Table already exists.')

def create_table_article(conn):
    '''
    This script sets up the user table in the database.
    '''
    
    try:
        conn.execute('''CREATE TABLE ARTICLES
                 (ID INT PRIMARY KEY     NOT NULL,
                 TITLE           TEXT    NOT NULL,
                 AUTHOR           TEXT    NOT NULL,
                 DATE           TEXT    NOT NULL,
                 PICTURES           TEXT    NOT NULL,
                 CONTENT            TEXT     NOT NULL,
                 CATEGORY            TEXT     NOT NULL);''')
        print("Table created successfully")
    except:
        print('Table already exists.')

def add_article(conn, TITLE=False, AUTHOR=False, DATE=False, Pictures=False, CONTENT=False, CATEGORY = False):
    if __name__ == '__main__':
        usr_info = login_credentials(conn)
        TITLE = input('Title:')
        auth = input('email:')
        status = False
        while status == False:
            if auth.strip() in usr_info:
                if input('Password: ') ==  usr_info[auth.strip()][0]:
                    AUTHOR = usr_info[auth.strip()][1] + ' ' + usr_info[auth.strip()][2][0] + '. ' + usr_info[auth.strip()][3]
                    status = True
                else:
                    status = False
        DATE = input('Date(mm/dd/yyyy):')
        PICTURES = input('Paste file locs with ";" separating them:')
        CONTENT = input('Textual Content:')

        print('SELECT a CATEGORY:')
        print('1','-','iOS Music')
        print('2','-','Full-Fledge DAWs')
        print('3','-','Music Reviews')
        CATEGORY = input('Category #: ')
        if CATEGORY == '1':CATEGORY = 'iOS Music'
        if CATEGORY == '1':CATEGORY = 'Full-Fledge DAWs'
        if CATEGORY == '1':CATEGORY = 'Music Reviews'
        
            
        
    cursor = conn.execute("SELECT * from ARTICLES")
    x = 1
    for row in cursor:
        x += 1
    
    conn.execute("INSERT INTO ARTICLES (ID,TITLE,AUTHOR,DATE,PICTURES,CONTENT,CATEGORY) \
          VALUES (" + str(x) + ", '" + TITLE + "', '" + AUTHOR + "', '" + DATE + "', '" + PICTURES + "', '" + CONTENT + "', '" + CATEGORY + "' )");
    conn.commit()
    

def add_user(conn, first, middle, last, month, year, email, password):
    '''
    inputs:= conn, first, middle, last, month, year, email, password
    '''

    try:
        cursor = conn.execute("SELECT * from USERS")
            
        conn.execute("INSERT INTO USERS (EMAILADDRESS,PASSWORD,FIRSTNAME,MIDDLENAME,LASTNAME,MONTH,YEAR) \
              VALUES ('" + email.lower() + "', '" + password + "', '" + first + "', '" + middle + "', '" + last + "', " + str(month) + ", " + str(year) + " )");
        conn.commit()
    except:
        0

def alter_table(conn, table, new_col, Type):

    cursor = conn.execute('ALTER TABLE ' + table + ' ADD COLUMN ' + new_col + ' ' + Type + ';')

def login_credentials(conn):
    '''
    inputs:= connection_string
    '''
    cursor = conn.execute("SELECT * from USERS")
    usr_info = {}
    for row in cursor:
        usr_info[row[0]] = [row[1], row[2], row[3], row[4], row[5], row[6]]
        print('Name = ', row[1],row[2],row[3])
        print("EMAILADDRESS = ", row[0])
        print("PASSWORD = ", row[1])
    return usr_info

def return_articles(conn):
    cursor = conn.execute("SELECT * from ARTICLES")
    usr_info = {}
    for row in cursor:
        usr_info[row[0]] = [row[1], row[2], row[3], row[4], row[5], row[6]]
    return usr_info    

def deinitialize(conn):
    conn.close()       

if __name__ == '__main__':
    conn = initialize()
    create_table_users(conn)
    add_user(conn, 'Patrick', 'Luis', 'Downey', 12, 2018, 'patldown@gmail.com', 'Patld#121893')
    create_table_article(conn)
    add_article(conn)
    deinitialize(conn)


