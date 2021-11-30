from werkzeug.utils import redirect
from draft_app import app
from draft_app.config.mysqlconnection import connectToMySQL
from flask import flash, session

DATABASE = "fantasy_schema"


class Player:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.team = data['team']
        self.position = data['position']
        self.ecr_rank = data['ecr_rank']
        self.positional_rank = data['positional_rank']
        self.current_adp = data['current_adp']
        self.difference = data['difference']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    # create new Player
    @classmethod
    def new(cls, data):
        query = "INSERT INTO players (name, team, position, ecr_rank, positional_rank, current_adp, difference, created_at, updated_at) VALUES (%(name)s, %(team)s, %(position)s, %(ecr_rank)s, %(positional_rank)s, %(current_adp)s, %(difference)s, NOW(), NOW());"
        return connectToMySQL(DATABASE).query_db(query, data)

    # update existing Player
    @classmethod
    def update(cls, data):
        query = "UPDATE players SET team = %(team)s, ecr_rank = %(ecr_rank)s, positional_rank = %(positional_rank)s, current_adp = %(current_adp)s, difference = %(difference)s, updated_at = NOW() WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)

    # retreive all Players from database
    @classmethod
    def get_all(cls):
        players = []
        query = "SELECT * from players;"
        results = connectToMySQL(DATABASE).query_db(query)
        for player in results:
            players.append(player)
        return players

    # retreive all Player names from database
    @classmethod
    def get_all_names(cls):
        player_names = []
        query = "SELECT name FROM players ORDER BY ecr_rank ASC"
        results = connectToMySQL(DATABASE).query_db(query)
        for name in results:
            player_names.append(name)
        return player_names

    # retreive all players from data base and return a list sorted by ecr_rank
    @classmethod
    def get_all_sort_by_ecr(cls):
        players = [];
        query = "SELECT * FROM players ORDER BY players.ecr_rank ASC;"
        results = connectToMySQL(DATABASE).query_db(query)
        for player in results:
            players.append(cls(player))
        return players

    # retreive one player from database by passing in a name
    @classmethod
    def get_player_by_name(cls, data):
        query = "SELECT * FROM players WHERE name = %(name)s"
        player = connectToMySQL(DATABASE).query_db(query, data)
        return player

    # retreive a list of player names from database who's current_adp matches list of picks
    @classmethod
    def get_players_by_adp(cls, data):
        players = []
        for i in range(len(data['user_picks'])):
            query = "SELECT * FROM players WHERE current_adp = " + str(data['user_picks'][i])
            result = connectToMySQL(DATABASE).query_db(query, data)
            players.append(result[0]['name'])
        return players