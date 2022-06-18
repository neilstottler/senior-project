from flask import request
from flask_restful import Resource

#local


class User(Resource):

    def get(self):
        return {"data": "Hello World"}

    def post(self):
        username = request.form.get('username')
        password = request.form.get('password')
        return str(username) + " " + str(password)