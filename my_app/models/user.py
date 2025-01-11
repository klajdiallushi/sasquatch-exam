import re
from flask import flash
from my_app.config.mysqlconnection import connect_to_mysql

# re for validating email addresses
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# re for validating password complexity
PASSWORD_REGEX = re.compile(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$')

class User:
    db_name = 'finalexampy'  

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create_user(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connect_to_mysql(cls.db_name).query_db(query, data)

    @classmethod
    def find_user_by_id(cls, user_id):
        query = "SELECT * FROM users WHERE id = %(user_id)s;"
        data = {'user_id': user_id}
        user_from_db = connect_to_mysql(cls.db_name).query_db(query, data)
        if not user_from_db:
            return None
        return cls(user_from_db[0])

    @classmethod
    def find_user_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        user_from_db = connect_to_mysql(cls.db_name).query_db(query, data)
        if not user_from_db:
            return None
        return cls(user_from_db[0])

    @classmethod
    def update_user(cls, data):
        query = "UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s WHERE id = %(user_id)s;"
        return connect_to_mysql(cls.db_name).query_db(query, data)

    @classmethod
    def delete_user(cls, data):
        query = "DELETE FROM users WHERE id = %(user_id)s;"
        return connect_to_mysql(cls.db_name).query_db(query, data)

    @staticmethod
    def validate_user(user):
        is_valid = True
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address!", 'emailSignUp')
            is_valid = False
        if len(user['first_name']) < 2:
            flash('First name must be more than 2 characters', 'firstName')
            is_valid = False
        if len(user['last_name']) < 2:
            flash('Last name must be more than 2 characters', 'lastName')
            is_valid = False
        if len(user['password']) < 8:
            flash('Password must be at least 8 characters', 'password')
            is_valid = False
        if user['confirm_password'] != user['password']:
            flash('The passwords do not match', 'passwordConfirm')
            is_valid = False
        if not PASSWORD_REGEX.match(user['password']):
            flash('Password must contain at least one uppercase letter, one lowercase letter, and one digit', 'password')
            is_valid = False  
        if User.find_user_by_email({'email': user['email']}):  
            flash('Email is already in use', 'emailSignUp')
            is_valid = False 
        return is_valid