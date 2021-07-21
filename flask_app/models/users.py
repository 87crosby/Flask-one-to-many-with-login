from flask import flash
from flask.scaffold import F
from flask_app import app
import re
from flask_app.config.mysqlconnection import connectToMySQL

class User():

    def __init__(self, data):
        self.id = data['id']
        self.nickname = data['nickname']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    @classmethod
    def create_user(cls, data):
        query = "INSERT INTO users (nickname, email, password) VALUES (%(nickname)s, %(email)s, %(password)s)"
        
        result = connectToMySQL('exam_review').query_db(query, data)

        return result
    
    @classmethod
    def get_users_with_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s"

        results = connectToMySQL('exam_review').query_db(query, data)

        users = []
        
        for item in results:
            users.append(User(item))
        
        return users

    @classmethod
    def get_users_with_nickname(cls, data):
        query = "SELECT * FROM users WHERE nickname = %(nickname)s"

        results = connectToMySQL('exam_review').query_db(query, data)

        users = []
        
        for item in results:
            users.append(User(item))
        
        return users
    
    @staticmethod
    def validate_registration(data):
        '''
        Function that ensures user data is valid
        data = a dictionary
        returns: Boolean
        '''
        is_valid = True
        #nickname between 2 and 32 characters
        if (len(data['nickname']) < 2) or (len(data['nickname'])) > 32:
            flash("Nickname should be between 2 and 32 characters")
            is_valid = False
        
        #email should be valid
        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        if not email_regex.match(data['email']):
            flash("Email not valid")
            is_valid = False

        #password minimum length 8 characters
        if len(data['password']) < 8:
            flash("Password should be at least 8 characters")
            is_valid = False

        #confirm password match
        if data['password'] != data['confirm_password']:
            flash("Passwords should match")
            is_valid = False

        #ensure email isn't in use
        if len(User.get_users_with_email({'email': data['email']})) != 0:
            flash("Email already in use")
            is_valid = False

        if len(User.get_users_with_nickname({'nickname': data['nickname']})) != 0:
            flash("Nickname already in use")
            is_valid = False


        return is_valid