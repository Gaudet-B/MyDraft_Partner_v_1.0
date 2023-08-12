from draft_app import app
from draft_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from flask_bcrypt import Bcrypt
import re

DATABASE = "fantasy_schema"

bcrypt = Bcrypt(app)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
USER_NAME_REGEX = re.compile(r'^[a-zA-Z0-9]+(?:_[a-zA-Z0-9]+)?$')

class Team:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['team_name']
        self.league = data['league']
        self.settings = data['settings']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

    @classmethod
    def new(cls, data):
        query = "INSERT INTO teams (name, league, settings, created_at, updated_at, user_id) VALUES (%(name)s, %(league)s, %(settings)s,  NOW(), NOW(), %(user_id)s);"
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def update(cls, data):
        query = "UPDATE teams SET name = %(name)s, league = %(league)s, settings = %(settings)s, updated_at = NOW() WHERE team_id = %(team_id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM teams"
        return connectToMySQL(DATABASE).query_db(query)
    
    @classmethod
    def get_by_user(cls, data):
        query = "SELECT * FROM teams WHERE user_id = %(user_id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)
    
    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM teams WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)
    
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM teams WHERE user_id = %(user_id)s AND id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)