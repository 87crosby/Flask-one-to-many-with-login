from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app
from flask_app.models.users import User

class Show():

    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.date = data['date']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.users_id = data['users_id']
        self.user = None

    @classmethod
    def create_show(cls,data):
        query = "INSERT INTO shows (title, description, date, users_id) VALUES (%(title)s, %(description)s, %(date)s, %(users_id)s)"

        result = connectToMySQL('exam_review').query_db(query, data)

        return result

    @classmethod
    def get_all_shows(cls):
        query = "SELECT * FROM shows JOIN users ON shows.users_id = users.id"

        result = connectToMySQL('exam_review').query_db(query)

        shows = []
        for item in result:
            show = cls(item)
            user_data = {
                'id' : item['users.id'],
                'nickname' : item['nickname'],
                'email' : item['email'],
                'password' : item['password'],
                'created_at' : item['users.created_at'],
                'updated_at' : item['users.updated_at']
            }
            show.user = User(user_data)
            shows.append(show)

        return shows

    @classmethod
    def get_show_by_id(cls,data):
        query = "SELECT * FROM shows JOIN users ON shows.users_id = users.id WHERE shows.id = %(id)s"

        result = connectToMySQL('exam_review').query_db(query,data)

        show = cls(result[0])
        user_data = {
            'id' : result[0]['users.id'],
            'nickname' : result[0]['nickname'],
            'email' : result[0]['email'],
            'password' : result[0]['password'],
            'created_at' : result[0]['users.created_at'],
            'updated_at' : result[0]['users.updated_at']
        }
        show.user = User(user_data)
        
        return show

    @classmethod
    def update_show(cls, data):
        query = "UPDATE shows SET title = %(title)s, description = %(description)s, date = %(date)s WHERE id = %(id)s"

        connectToMySQL('exam_review').query_db(query,data)

    @classmethod
    def delete_show(cls, data):
        query = "DELETE FROM shows WHERE id = %(id)s"

        connectToMySQL('exam_review').query_db(query,data)


    @staticmethod
    def validate_show(data):
        '''
        Function that ensures user data is valid
        data = a dictionary
        returns: Boolean
        '''
        is_valid = True
        #show title between 1 and 100 characters
        if (len(data['title']) < 1) or (len(data['title'])) > 100:
            flash("Show title must be between 1 and 100 characters")
            is_valid = False
        
        #description between 1 and 500 characters
        if (len(data['description']) < 1) or (len(data['description'])) > 500:
            flash("Description must be between 1 and 500 characters")
            is_valid = False
        
        #check date
        if len(data['date']) == 0:
            flash("Date is blank")
            is_valid = False

        return is_valid