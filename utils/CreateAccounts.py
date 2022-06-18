#local imports
from models import Users
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

now = datetime.now()
userDB = Users()

class CreateAccounts():
    
    def create_account(username, email, password):
        #check if username exists in DB
        if userDB.username_exists(username) is None:
            #check if the email exists in the DB
            if userDB.email_exists(email) is None:
                #passes both checks

                #hash password
                hash_password = generate_password_hash(password, method='sha256')
                userDB.insert(username, hash_password, email, now, now)
                return "Success. Please Login."
            else:
                #email exists
                return "Email Exists."
        else:
            #username exists
            return "Username Exists."