from draft_app import app
from draft_app.config.mysqlconnection import connectToMySQL

# DATABASE = "fantasy_schema"
DATABASE = "mdp_v3_schema"

class Roster:
  def __init__(self, data):
    self.id = data['id']
    self.players = data['players']
    self.created_at = data['created_at']
    self.updated_at = data['updated_at']
    self.team_id = data['team_id']

  @classmethod
  def new(cls, data):
    query = "INSERT INTO rosters (players, created_at, updated_at, team_id) VALUES (%(players)s, NOW(), NOW(), %(team_id)s);"
    return connectToMySQL(DATABASE).query_db(query, data)

  @classmethod
  def get_all(cls):
    query = "SELECT * FROM rosters"
    return connectToMySQL(DATABASE).query_db(query)

  @classmethod
  def get_by_team(cls, data):
    query = "SELECT * FROM rosters WHERE team_id = %(team_id)s;"
    return connectToMySQL(DATABASE).query_db(query, data)

  @classmethod
  def get_by_id(cls, data):
    query = "SELECT * FROM rosters WHERE id = %(id)s;"
    return connectToMySQL(DATABASE).query_db(query, data)

  @classmethod
  def delete(cls, data):
    query = "DELETE FROM rosters WHERE team_id = %(team_id)s AND id = %(id)s;"
    return connectToMySQL(DATABASE).query_db(query, data)

  @classmethod
  def update(cls, data):
    query = "UPDATE rosters SET players = %(players)s, updated_at = NOW() WHERE id = %(id)s;"
    return connectToMySQL(DATABASE).query_db(query, data)
