# from types import ClassMethodDescriptorType
# from werkzeug.utils import redirect
from draft_app import app
from draft_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from flask_bcrypt import Bcrypt
import re

DATABASE = "fantasy_schema"

bcrypt = Bcrypt(app)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
USER_NAME_REGEX = re.compile(r'^[a-zA-Z0-9]+(?:_[a-zA-Z0-9]+)?$')

class User:
    def __init__(self, data):
        self.id = data['id']
        self.user_name = data['user_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    # user validation method
    @staticmethod
    def validate_user(user):
        # is_valid starts as True and must pass all validation tests without being set to False
        is_valid = True
        # declare variables to be validated
        user_name = user['user_name_input']
        user_email = user['email_input']
        confirm = user['confirm_password']
        # MySQL query
        query = "SELECT email FROM users;"
        emails = connectToMySQL(DATABASE).query_db(query)
        
        # validation tests
        if not EMAIL_REGEX.match(user['email_input']):
            flash("invalid email address.", "email")
            is_valid = False
        if len(user['user_name_input']) == 0:
            flash("all fields required", "user_name")
            is_valid = False
        if len(user['user_name_input']) < 6:
            flash("username must be at least six characters long.", "user_name")
            is_valid = False
        if len(user['user_name_input']) > 45:
            flash("username cannot be longer than 45 characters")
        if not USER_NAME_REGEX.match(user['user_name_input']):
            flash("invalid username - username must only contain alphanumeric chatacters and underscores(_) and may not include consecutive underscores.", "user_name")
        if len(user['email_input']) == 0:
            flash("all fields required", "email")
            is_valid = False
        # check user-provided email against all existing emails
        for email in emails:
            if user_email == email['email']:
                flash("a user with this email address already exists.", "email")
                is_valid = False
        if len(user['password_input']) == 0:
            flash("all fields required", "password")
            is_valid = False
        if len(user['password_input']) < 8:
            flash("password must be at least 8 characters long", "password")
            is_valid = False
        if len(user['confirm_password']) == 0:
            flash("all fields required", "confirm_password")
            is_valid = False
        if confirm != user['password_input']:
            flash("passwords do not match.", "confirm_password")
            is_valid = False
        return is_valid

    # login validation method
    @staticmethod
    def validate_login(data):
        is_valid = True
        user = User.get_user_by_email(data)
        if not user:
            flash("invalid email/password", "login")
            is_valid = False
        elif not bcrypt.check_password_hash(user.password, data['password']):
            flash("invalid email/password", "login")
            is_valid = False
        return is_valid

    # create a new instance of the User class
    @classmethod
    def new_user(cls, data):
        query = "INSERT INTO users (user_name, email, password, created_at, updated_at) VALUES (%(user_name)s, %(email)s, %(password)s, NOW(), NOW());"
        return connectToMySQL(DATABASE).query_db(query, data)

    # retreive one User from database by id
    @classmethod
    def get_user_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        user = cls(results[0])
        return user

    # retreive one User'ss name from database by id
    @classmethod
    def get_user_name_by_id(cls, data):
        query = "SELECT user_name FROM users WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)

    # retreive one User from m databasase by email
    @classmethod
    def get_user_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        user = cls(result[0])
        return user


# Admin class inherits from User class
class Admin (User):
    def __init__(self, data):
        super().__init__(data)
        self.is_admin = data['is_admin']

    # create a new instance of the Admin class
    @classmethod
    def new(cls, data):
        query = "INSERT INTO admins (user_name, email, password, created_at, updated_at, is_admin) VALUES (%(user_name)s, %(email)s, %(password)s, NOW(), NOW(), 'y');"
        return connectToMySQL(DATABASE).query_db(query, data)

    # retreive one Admin from database by email
    @classmethod
    def get_admin_by_email(cls, data):
        query = "SELECT * FROM admins WHERE email = %(email)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        admin = cls(result[0])
        return admin

    # login validation
    @staticmethod
    def validate_login(data):
        is_valid = True
        admin = Admin.get_admin_by_email(data)
        if not admin:
            flash("invalid email/password", "login")
            is_valid = False
        elif not bcrypt.check_password_hash(admin.password, data['password']):
            flash("invalid email/password", "login")
            is_valid = False
        return is_valid
