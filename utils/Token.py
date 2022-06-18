import uuid

#local
from models import Users
from models import Authentication

authDB = Authentication()
userDB = Users()

class Token():
    
    
    
    def makeTheToken(username):

        #make the UNIQUE token
        user_uuid = uuid.uuid4()

        #we need the user ID
        user_id = userDB.id(username)[0]

        #we need to insert it now
        #authDB.insert(user_id, user_uuid)

        return user_uuid