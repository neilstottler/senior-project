import sqlite3

from sqlalchemy import null

class Authentication:
    def __init__(self):
        self.con = sqlite3.connect('levelgame.db', check_same_thread=False)
        self.cur = self.con.cursor()
        self.foreign_keys()
        self.create_table()

    def foreign_keys(self):
        self.cur.execute("""PRAGMA foreign_keys = ON;""")

    def create_table(self):
        #self.cur.execute("""DROP TABLE auth""")
        self.cur.execute("""CREATE TABLE IF NOT EXISTS auth (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            token VARCHAR(255) NOT NULL,
            date_created DATETIME NOT NULL,
            date_expired DATETIME,
            FOREIGN KEY(user_id) REFERENCES users(user_id)            
        )""")

    #insert new token into DB
    def insert(self, user_id, token, created):
        self.cur.execute("""INSERT INTO auth (user_id, token, date_created) VALUES (?,?, ?)""", (user_id, token, created))
        self.con.commit()

    #expire the token provided
    def expireToken(self, user_id, token, expired):
        self.cur.execute("""UPDATE auth SET date_expired=? WHERE user_id=? AND token=?""", (expired, user_id, token))
        self.con.commit()

    #read all from the DB - dev
    def read(self):
        self.cur.execute("""SELECT * FROM auth""")
        rows = self.cur.fetchall()
        return rows

    #check if token exists for a user
    def tokenCheck(self, user_id):
        self.cur.execute("""SELECT token FROM auth WHERE user_id=(?) AND date_expired IS NULL""", (user_id,))
        rows = self.cur.fetchone()
        return rows

    #used to check is a given token is expired
    def expiredToken(self, token):
        try:
            self.cur.execute("""SELECT date_expired FROM auth WHERE token=(?)""", (token,))
            rows = self.cur.fetchone()
            
            if rows[0] is None:
                return False
            else:
                return True
        except:
            return "Invalid Token"

    #get user id with token
    def getUserIdWithToken(self, token):
        self.cur.execute("""SELECT user_id FROM auth WHERE token=(?) AND date_expired IS NULL""", (token,))
        rows = self.cur.fetchone()
        return rows