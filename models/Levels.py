import sqlite3

from sqlalchemy import null

class Levels:
    def __init__(self):
        self.con = sqlite3.connect('levelgame.db', check_same_thread=False)
        self.cur = self.con.cursor()
        self.foreign_keys()
        self.create_table()

    def foreign_keys(self):
        self.cur.execute("""PRAGMA foreign_keys = ON;""")

    def create_table(self):
        #self.cur.execute("""DROP TABLE auth""")
        self.cur.execute("""CREATE TABLE IF NOT EXISTS levels (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            platform VARCHAR(255) NOT NULL,
            obsticles VARCHAR(255) NOT NULL,
            powerups VARCHAR(255) NOT NULL,
            besttree VARCHAR(255) NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(user_id)            
        )""")

    #insert new token into DB
    def insert(self, user_id, platform, obsticles, powerups, besttree):
        self.cur.execute("""INSERT INTO levels (user_id,  platform, obsticles, powerups, besttree) VALUES (?,?,?,?,?)""", (user_id, platform, obsticles, powerups, besttree))
        self.con.commit()

    #read all from the DB - dev
    def read(self):
        self.cur.execute("""SELECT * FROM levels""")
        rows = self.cur.fetchall()
        return rows

    def getLevelsByUser(self, user_id):
        self.cur.execute("""SELECT * FROM levels WHERE user_id=(?)""", (user_id,))
        rows = self.cur.fetchall()
        return rows

    def getLevel(self, level_id):
        self.cur.execute("""SELECT * FROM levels WHERE id=(?)""", (level_id,))
        rows = self.cur.fetchall()
        return rows
