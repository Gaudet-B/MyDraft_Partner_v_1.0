from draft_app import app
from draft_app.config.mysqlconnection import connectToMySQL

DATABASE = "mdp_v3_schema"
# @TODO update this!
LIST_OF_FIELDS = [
    'name',
    'rank',
    'pass_comp_and_att',
    'pass_yds',
    'pass_td',
    'int',
    'rush_att',
    'rush_yds',
    'rush_td',
    'rec',
    'rec_yds',
    'rec_td',
    'rec_tgt',
    'total_fpts',
    'avg_fpts',
]


class Projection:
    def __init__(self, data):
        self.id = data['id']
        self.source = data['source']
        self.projections = data['projections']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def new(cls, data):
        query = "INSERT INTO projections (source, projections, created_at, updated_at) VALUES (%(source)s, %(projections)s, NOW(), NOW());"
        return connectToMySQL(DATABASE).query_db(query, data)
      
    @classmethod
    def update(cls, data):
        query = "UPDATE projections SET projections = %(projections)s, updated_at = NOW() WHERE source = %(source)s;"
        return connectToMySQL(DATABASE).query_db(query, data)
      
    @classmethod
    def get_by_source(cls, data):
        query = "SELECT * FROM projections WHERE source = %(source)s;"
        return connectToMySQL(DATABASE).query_db(query, data)
