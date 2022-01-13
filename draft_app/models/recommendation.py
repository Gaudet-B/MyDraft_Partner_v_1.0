from draft_app import app
from draft_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from flask_bcrypt import Bcrypt
import re

DATABASE = "fantasy_schema"

bcrypt = Bcrypt(app)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
USER_NAME_REGEX = re.compile(r'^[a-zA-Z0-9]+(?:_[a-zA-Z0-9]+)?$')

class Recommendation:
    def __init__(self, data):
        self.id = data['id']
        self.picks = data['picks']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.team_id = data['team_id']

    @classmethod
    def new(cls, data):
        query = "INSERT INTO recommendations (picks, created_at, updated_at, team_id) VALUES (%(picks)s, NOW(), NOW(), %(team_id)s, "
        return connectToMySQL(DATABASE).query_db(query, data)
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recommendations"
        return connectToMySQL(DATABASE).query_db(query)
    
    @classmethod
    def get_by_team(cls, data):
        query = "SELECT * FROM recommendations WHERE team_id = %(team_id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)
    
    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM recommendations WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)
    
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM recommendations WHERE team_id = %(team_id)s AND id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)