#local imports
from models import Users
from werkzeug.security import generate_password_hash, check_password_hash

usersDB = Users()

class Password():
    
    def checkPassword(username, password):
        
        try:
            if check_password_hash(usersDB.password(username)[0], password):
                return True
            else:
                return False
        except:
            return False