from flask import Flask, request, jsonify
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

#local
from utils import Password, Token, CreateAccounts
from models import Users, Authentication, Levels

now = datetime.now()

authDB = Authentication()
usersDB = Users()
levelsDB = Levels()

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///levelgame.db'
db = SQLAlchemy(app)

class UserModel(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    time_created = db.Column(db.DateTime, nullable=False)
    last_accessed = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f"UserID: {UserModel.user_id}, Username: {UserModel.username})"

user_fields = {
    'user_id': fields.Integer,
    'username': fields.String,
    'password': fields.String,
    'email': fields.String,
    'time_created': fields.DateTime,
    'time_accessed': fields.DateTime
}

class AuthenticationModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    token = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"ID: {AuthenticationModel.id}, UserID: {AuthenticationModel.user_id})"

authentication_fields = {
    'id': fields.Integer,
    'user_id': fields.Integer,
    'token': fields.String
}

class Level(Resource):
    pass

class Login(Resource):
    #@marshal_with(user_fields)
    def get(self):
        return {"Error": "You're not supposed to be here."}

    #@marshal_with(user_fields)
    def put(self):
        return 404

    #@marshal_with(user_fields)
    def patch(self):
        return 404

    def delete(self):
        return 204

    def post(self):
        username = request.form.get('username')
        password = request.form.get('password')

        if Password.checkPassword(username, password):
            
            #get the user ID
            user_id = usersDB.id(username)
            print("USER ID: "+ str(user_id))

            #check if there is an old token
            old_token = authDB.tokenCheck(user_id[0])
            print("OLD TOKEN: " + str(old_token[0]))
            #check if old token exists
            if old_token is None:
                #make new token
                print("Old token is none")
                token = Token.makeTheToken(username)

                #insert token into DB
                authDB.insert(user_id, str(token), now)
                return token
            else:

                #expire old token
                authDB.expireToken(user_id[0], str(old_token[0]), now)

                #make new token
                new_token = Token.makeTheToken(username)

                #insert new token into DB
                authDB.insert(user_id[0], str(new_token), now)
                print("NEW TOKEN: " + str(new_token))
                
                #this should be 200 and NOT the token, that is meant to be somewhat secret
                return str(new_token)

                #we are given username and password
                #get User ID from username
                #check if there is an old token
                    #to do this we need 
                    #user id
                    #expect true or false returned
                #if there is invalidate it
                #enter new token into DB


        else:
            return 404
        #return str(username) + " " + str(password)

class CreateAccount(Resource):
    #@marshal_with(user_fields)
    def get(self):
        return {"Error": "You're not supposed to be here."}

    #@marshal_with(user_fields)
    def put(self):
        return 404

    #@marshal_with(user_fields)
    def patch(self):
        return 404

    def delete(self):
        return 204

    def post(self):
        username = request.form.get('username')
        email = request.form.get('email')
        confirm_email = request.form.get('confirm_email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        #we should return a string after doing checks for is the creds are already used
        return CreateAccounts.create_account(username, email, password)

api.add_resource(Login, "/login")
api.add_resource(CreateAccount, "/createaccount")
api.add_resource(Level, "/level")

if __name__ == "__main__":
    app.run(debug=True)

