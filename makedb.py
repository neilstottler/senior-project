#imports
import sqlite3
from sqlite3 import Error
from datetime import datetime
from tabnanny import check
from werkzeug.security import generate_password_hash, check_password_hash
import tkinter

#local imports
from models import Users
from models import Authentication

now = datetime.now()

db = Users()
authy = Authentication()

print(authy.read())




#expire test
authy.expireToken(2, "342f4ada-9c14-411f-8988-eefc50e9d5d0", now)
authy.expireToken(2, "6bd64b4e-5381-4553-92be-925f0e9ef437", now)
authy.expireToken(2, "ba70eb25-4f1a-41a3-afc6-cf8f5072d543", now)
authy.expireToken(2, "9797e28d-897e-4258-a071-0e00d525e047", now)



print(authy.read())

#password=generate_password_hash('password', method='sha256')
#print(password)

#db.insert('neil', password, 'stottlern@wit.edu', now, now)
#for item in db.read():
#    print(item)

#for item in authy.read():
#    print(item)

#authy.insert(1, 'test_token_2', now)

#expire test token
#authy.expireToken( 1, 'test_token', now)
#print(authy.read())

#check for expired token
#print(authy.expiredToken('test_token'))
#print(authy.expiredToken('test_token_2'))
#print(authy.expiredToken('invalid_token'))

#print((db.password('neil')[0]))
#checks a passwords hash
#print(check_password_hash(db.password('neil')[0], 'password'))