import sqlite3

class Users:
    def __init__(self):
        self.con = sqlite3.connect('levelgame.db', check_same_thread=False)
        self.cur = self.con.cursor()
        self.create_table()

    def create_table(self):
        #self.cur.execute("""DROP TABLE users""")
        self.cur.execute("""CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            time_created DATETIME,
            last_accessed DATETIME
        )""")

    def insert(self, username, password, email, time_created, last_accessed):
        self.cur.execute("""INSERT OR IGNORE INTO users (username, password, email, time_created, last_accessed) VALUES (?,?,?,?,?)""", (username, password, email, time_created, last_accessed))
        self.con.commit()

    def read(self):
        self.cur.execute("""SELECT * FROM users""")
        rows = self.cur.fetchall()
        return rows

    def password(self, password):
        self.cur.execute("""SELECT password FROM users WHERE username=(?) """, (password,))
        rows = self.cur.fetchone()
        return rows

    def id(self, username):
        self.cur.execute("""SELECT user_id FROM users WHERE username=(?) """, (username,))
        rows = self.cur.fetchone()
        return rows

    def username_exists(self, username):
        self.cur.execute("""SELECT username FROM users WHERE username=(?) """, (username,))
        rows = self.cur.fetchone()
        return rows

    def email_exists(self, email):
        self.cur.execute("""SELECT email FROM users WHERE email=(?) """, (email,))
        rows = self.cur.fetchone()
        return rows
