# import csv

BALLERS_DATA_MAP = {
    'qb': [
      'name',
      'team',
      'bye_week',
      'rank',
      'fpts',
      'pass_yds',
      'pass_td',
      'rush_yds',
      'rush_td',
      'int',
      'fum',
    ],
    'rb': [
      'name',
      'team',
      'bye_week',
      'rank',
      'fpts',
      'rush_att',
      'rush_yds',
      'rush_td',
      'rec',
      'rec_yds',
      'rec_td',
      'fum',
    ],
    'wr': [
      'name',
      'team',
      'bye_week',
      'rank',
      'fpts',
      'rec',
      'rec_yds',
      'rec_td',
      'rush_att',
      'rush_yds',
      'rush_td',
      'fum',
    ],
    'te': [
      'name',
      'team',
      'bye_week',
      'rank',
      'fpts',
      'rec',
      'rec_yds',
      'rec_td',
      'fum',
    ],
}


def parse_projections_csv(data):
    print(f'DATA ===> (( {data} ))')
    players_dict = {}
    position = data['position']
    projections = data['projections']
    for row in projections:
        player = {}
        for i in range(len(row)):
            # skip columns at index 1 (team) and 2 (bye week)
            if i < 1 or i > 2:
                player.update({BALLERS_DATA_MAP[position][i]: row[i]})
        if len(row) > 0:
            players_dict.update({player['name']: player})
    return players_dict


def update_player_projections(existing, new):
    return {k:v for d in (existing, new) for k,v in d.items()}
