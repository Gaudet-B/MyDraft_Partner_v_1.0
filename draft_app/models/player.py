# from werkzeug.utils import redirect
from draft_app import app
from draft_app.config.mysqlconnection import connectToMySQL
# from flask import flash, session
# import json

# DATABASE = "fantasy_schema"
DATABASE = "mdp_v3_schema"

# PLAYERS_TABLE = "players"
PLAYERS_TABLE = "players_2024"

# ====================================================== #
# @TODO
#   1. add a method to update player consistency once
#       new data is available
#
# ====================================================== #


class Player:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.team = data['team']
        self.position = data['position']
        self.ecr = data['ecr_rank']
        self.positional_rank = data['positional_rank']
        self.current_adp = data['current_adp']
        self.f_pros_id = data['f_pros_id']
        self.consistency_t1 = data['consistency_t1']
        self.consistency_t2 = data['consistency_t2']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    # create new Player
    @classmethod
    def new(cls, data):
        # data.update({'table': PLAYERS_TABLE})
        # query = "INSERT INTO %(table)s (name, team, position, ecr, positional_rank, current_adp, f_pros_id, consistency_t1, consistency_t2, created_at, updated_at) VALUES (%(name)s, %(team)s, %(position)s, %(ecr_rank)s, %(positional_rank)s, %(current_adp)s, %(f_pros_id)s, %(consistency_t1)s, %(consistency_t2)s, NOW(), NOW());"
        query = "INSERT INTO players_2024 (name, team, position, ecr, positional_rank, current_adp, f_pros_id, consistency_t1, consistency_t2, created_at, updated_at) VALUES (%(name)s, %(team)s, %(position)s, %(ecr_rank)s, %(positional_rank)s, %(current_adp)s, %(f_pros_id)s, %(consistency_t1)s, %(consistency_t2)s, NOW(), NOW());"
        return connectToMySQL(DATABASE).query_db(query, data)

    # update existing Player (DEPRICATED)
    @classmethod
    def update(cls, data):
        query = "UPDATE players_2024 SET team = %(team)s, ecr = %(ecr_rank)s, positional_rank = %(positional_rank)s, current_adp = %(current_adp)s, updated_at = NOW() WHERE f_pros_id = %(f_pros_id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)
    
    # alternative update method
    @classmethod
    def edit(cls, data):
        query = """
            UPDATE players_2024
            SET
                name = CASE WHEN name <> %(name)s THEN %(name)s ELSE name END,
                team = CASE WHEN team <> %(team)s THEN %(team)s ELSE team END,
                position = CASE WHEN position <> %(position)s THEN %(position)s ELSE position END,
                ecr = CASE WHEN ecr <> %(ecr_rank)s THEN %(ecr_rank)s ELSE ecr END,
                positional_rank = CASE WHEN positional_rank <> %(positional_rank)s THEN %(positional_rank)s ELSE positional_rank END,
                current_adp = CASE WHEN current_adp <> %(current_adp)s THEN %(current_adp)s ELSE current_adp END,
                consistency_t1 = CASE WHEN consistency_t1 <> %(consistency_t1)s THEN %(consistency_t1)s else consistency_t1 END,
                consistency_t2 = CASE WHEN consistency_t2 <> %(consistency_t2)s THEN %(consistency_t2)s else consistency_t2 END,
                updated_at = NOW()
            WHERE f_pros_id = %(f_pros_id)s;
        """
        # query = "UPDATE players SET consistency = %(consistency)s WHERE f_pros_id = %(f_pros_id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)

    # retreive all Players from database
    @classmethod
    def get_all(cls):
        players = []
        query = f"SELECT * from players_2024;"
        results = connectToMySQL(DATABASE).query_db(query)
        for player in results:
            players.append(player)
        return players

    # retreive all Player names from database
    @classmethod
    def get_all_names(cls):
        player_names = []
        query = f"SELECT name FROM players_2024 ORDER BY ecr ASC"
        results = connectToMySQL(DATABASE).query_db(query)
        for name in results:
            player_names.append(name)
        return player_names

    # retreive all players from data base and return a list sorted by ecr
    @classmethod
    def get_all_sort_by_ecr(cls):
        players = []
        query = f"SELECT * FROM players_2024 ORDER BY players_2024.ecr ASC;"
        results = connectToMySQL(DATABASE).query_db(query)
        for player in results:
            players.append(cls(player))
        return players

    # retreive one player from database by passing in a name
    @classmethod
    def get_player_by_name(cls, data):
        query = "SELECT * FROM players_2024 WHERE name = %(name)s"
        player = connectToMySQL(DATABASE).query_db(query, data)
        return player

    # retreive a list of player names from database who's current_adp matches list of picks
    @classmethod
    def get_players_by_adp(cls, data):
        players = []
        for i in range(len(data['user_picks'])):
            query = "SELECT * FROM players_2024 WHERE current_adp = " + str(data['user_picks'][i])
            result = connectToMySQL(DATABASE).query_db(query, data)
            players.append(result[0]['name'])
        return players