from draft_app import app
from draft_app.config.mysqlconnection import connectToMySQL

DATABASE = "fantasy_schema"

class Ranking:
  def __init__(self, data):
    self.id = data['id']
    self.players = data['players']
    self.created_at = data['created_at']
    self.updated_at = data['updated_at']
    self.team_id = data['team_id']

  @classmethod
  def new(cls, data):
    query = "INSERT INTO rankings (players, created_at, updated_at, team_id) VALUES (%(players)s, NOW(), NOW(), %(team_id)s);"
    return connectToMySQL(DATABASE).query_db(query, data)

  @classmethod
  def get_all(cls):
    query = "SELECT * FROM rankings"
    return connectToMySQL(DATABASE).query_db(query)

  @classmethod
  def get_by_team(cls, data):
    query = "SELECT * FROM rankings WHERE team_id = %(team_id)s;"
    return connectToMySQL(DATABASE).query_db(query, data)

  @classmethod
  def get_by_id(cls, data):
    query = "SELECT * FROM rankings WHERE id = %(id)s;"
    return connectToMySQL(DATABASE).query_db(query, data)

  @classmethod
  def delete(cls, data):
    query = "DELETE FROM rankings WHERE team_id = %(team_id)s AND id = %(id)s;"
    return connectToMySQL(DATABASE).query_db(query, data)

  @classmethod
  def update(cls, data):
    query = "UPDATE rankings SET players = %(players)s, updated_at = NOW() WHERE id = %(id)s;"
    return connectToMySQL(DATABASE).query_db(query, data)
