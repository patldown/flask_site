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


def login_credentials(conn):
    '''
    inputs:= connection_string
    '''
    cursor = conn.execute("SELECT * from USERS")
    usr_info = {}
    for row in cursor:
        usr_info[row[0]] = [row[1], row[2], row[3], row[4]]
        print('Name = ', row[1],row[2],row[3])
        print("EMAILADDRESS = ", row[0])
        print("PASSWORD = ", row[1])
    return usr_info

def deinitialize(conn):
    conn.close()       

if __name__ == '__main__':
    conn = initialize()
    create_table_users(conn)
    add_user(conn, 'Patrick', 'Luis', 'Downey', 12, 2018, 'patldown@gmail.com', 'Patld#121893')
    login_credentials(conn)
    deinitialize(conn)


