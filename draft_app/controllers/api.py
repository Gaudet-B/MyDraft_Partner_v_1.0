import flask
from flask import app
from flask import request, make_response

from draft_app import app
from draft_app.models.user import User, Admin
from draft_app.models.player import Player
from draft_app.models.projection import Projection
from draft_app.models.team import Team
from draft_app.models.ranking import Ranking
from draft_app.models.roster import Roster
from draft_app.models.recommendation import Recommendation
from draft_app.controllers import general
from draft_app.util.scraper_util import scrape_and_parse_player_data, scrape_and_parse_espn_projections
from draft_app.util.csv_util import parse_projections_csv, update_player_projections
import json


# --> API Routes <--

@app.route('/api/results', methods=['GET'])
def api_results():
  # check for advanced settings and redirect
    # if "qb_select" in request.form:
    #     return redirect("/players/results/advanced", code = 307)
    # retrieve data from user input, run draft_order function to determine "user_picks"
    data = {
        "team_name": request.form['team_name'],
        "num_of_teams": int(request.form['num_of_teams']),
        "draft_position": int(request.form['draft_position']),
        "num_of_rounds": int(request.form['draft_rounds']),
        "user_picks": general.draft_order(request.form['num_of_teams'], request.form['draft_position'], request.form['draft_rounds'])
    }
    # check that user is logged in
    # if "user_id" in session:
    #     data.update({"logged_in": True})
    # call pick_recs fuction to generate recommendations, then add them to the data that is passed to the html template
    player_recs = general.pick_recs(data['user_picks'], data['num_of_teams'])
    data.update({"player_recs": player_recs})
    # declare variables needed to generate player targets
    sorted_players = []
    unsorted_players = player_recs[:]
    # generate targets, then add them to the data that is passed to the html template
    general.sort_by_value(unsorted_players, sorted_players)
    player_targets = sorted_players[:]
    data.update({"player_targets": player_targets})
    res = flask.Response(json.dumps(data))
    res.headers['Access-Control-Allow-Origin'] = '*'
    # print(res)

    return res

@app.route('/api/all_players', methods=['GET'])
def api_display_all_player_names():
  # print('running...')
  # players = general.get_player_names()
  players = Player.get_all()
  res = make_response(players)
  res.headers['Access-Control-Allow-Origin'] = '*'
  # print(res)

  # return json.dumps(players)
  return res

@app.route('/api/create_player_list', methods=['POST'])
def api_create_player_list():
  # print(os.getcwd() + '/chromedriver')
  print('running...')
  player_list = scrape_and_parse_player_data()
  for player in player_list:
    # @TODO need an error handler here?
    # create a new instance of the Player class and add to DB
    Player.new(player)
  res = flask.Response(json.dumps('players created'))
  res.headers['Access-Control-Allow-Origin'] = '*'
  return res

@app.route('/api/update_player_list', methods=['PUT'])
def api_update_player_list():
  print('running...')
  player_list = scrape_and_parse_player_data()
  for player in player_list:
    Player.edit(player)
  res = flask.Response(json.dumps('players updated'))
  res.headers['Access-Control-Allow-Origin'] = '*'
  return res


@app.route('/api/get_espn_projections', methods=['POST'])
def api_get_espn_projections():
  print('running...')
  player_projections = scrape_and_parse_espn_projections()
  if not player_projections:
    raise Exception('Error scraping ESPN projections')
  
  Projection.new({'source': 'espn', 'projections': json.dumps(player_projections)})
  # players = general.get_espn_projections(data)
  res = flask.Response(json.dumps('player projections updated'))
  res.headers['Access-Control-Allow-Origin'] = '*'
  return res


@app.route('/api/upload_ballers_player_projections', methods=['POST'])
def api_upload_player_projections():
  print('running... upload_ballers_player_projections')
  data = request.get_json()
  source = f'footballers-{data["source"]}'
  existing_projections = Projection.get_by_source({'source': source})
  print(f'EXISTING PROJECTIONS ===> {existing_projections}')
  existing = json.loads(existing_projections[0]['projections']) if existing_projections else None
  new = parse_projections_csv(data)
  print(f'NEW PROJECTIONS ===> {new}')
  player_projections = new if existing is None else update_player_projections(existing, new)
  print(f'PLAYER PROJECTIONS ===> {player_projections}')
  # if no projections exist for the source, create a new entry
  if existing is None:
    Projection.new({'source': source, 'projections': json.dumps(player_projections)})
  else:
    Projection.update({'source': source, 'projections': json.dumps(player_projections)})
  res = flask.Response(json.dumps('player projections uploaded'))
  res.headers['Access-Control-Allow-Origin'] = '*'
  return res


@app.route('/api/create_team', methods=['POST'])
def api_create_team():
  print('running...')
  # get data from request
  data = request.get_json()
  #
  # print(data)
  # 
  team_info = data['info']
  # team_settings = data['settings']
  team_settings = {
    "draft_position": data['settings']['draftPosition'],
    "superflex": data['settings']['superflex'],
    "ppr": data['settings']['ppr'],
    "num_of_teams": data['settings']['numOfTeams'],
    "roster": data['roster'],
  }

  team_data = {
    "name": team_info['name'],
    "league": team_info['league'],
    "settings": json.dumps(team_settings),
    # "ranks": data['ranks'], # list of player f_pros_id
    # "roster": data['roster'], # list of player f_pros_id
    "user_id": data['user_id'],
  }
  # create a new instance of the Team class
  team = Team.new(team_data)
  if team:
    res = flask.Response(json.dumps('team created'))
    # res = make_response('team created')
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res
  else:
    res = flask.Response(json.dumps('error creating team'))
    # res = make_response('team not created')
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res

@app.route('/api/edit_team', methods=['POST'])
def api_update_team():
  print('running...')
  # get data from request
  data = request.get_json()
  #
  # print(data)
  # 
  team_info = data['info']
  # team_settings = data['settings']
  team_settings = {
    "draft_position": data['settings']['draftPosition'],
    "superflex": data['settings']['superflex'],
    "ppr": data['settings']['ppr'],
    "num_of_teams": data['settings']['numOfTeams'],
    "roster": data['roster'],
  }

  team_data = {
    "name": team_info['name'],
    "league": team_info['league'],
    "settings": json.dumps(team_settings),
    # "ranks": data['ranks'], # list of player f_pros_id
    # "roster": data['roster'], # list of player f_pros_id
    "team_id": data['id'],
  }
  # create a new instance of the Team class
  team = Team.update(team_data)
  if team:
    res = flask.Response(json.dumps('team updated'))
    # res = make_response('team updated')
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res
  else:
    res = flask.Response(json.dumps('error updating team'))
    # res = make_response('team not updated')
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res


@app.route('/api/get_teams_by_user', methods=['POST'])
def api_get_teams_by_user():
  print('running...')
  # get data from request
  data = request.get_json()
  id = data['user_id']
  #
  print(id)
  # 
  teams = Team.get_by_user(data)
  print(teams)
  if teams:
    # res = flask.Response(teams)
    res = make_response(teams)
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res
  else:
    res = flask.Response(json.dumps('no teams found'))
    # res = make_response('no teams found')
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res

# @app.route('/api/get_team_by_id', methods=['POST'])
# def api_get_team_by_id():
#   print('running...')
#   # get data from request
#   data = request.get_json()
#   id = data['id']
#   #
#   print(id)
#   # 
#   team = Team.get_by_id(data)
#   print(team)
#   if team:
#     # res = flask.Response(team)
#     res = make_response(team)
#     res.headers['Access-Control-Allow-Origin'] = '*'
#     return res
#   else:
#     res = flask.Response(json.dumps('no team found'))
#     # res = make_response('no team found')
#     res.headers['Access-Control-Allow-Origin'] = '*'
#     return res

@app.route('/api/get_rankings_by_team', methods=['POST'])
def api_get_rankings_by_team():
  print('running...')
  # get data from request
  data = request.get_json()
  id = data['team_id']
  #
  print(id)
  # 
  rankings = Ranking.get_by_team({'team_id': id})
  print(rankings)
  if rankings:
    # res = flask.Response(rankings)
    res = make_response(rankings)
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res
  else:
    res = flask.Response(json.dumps('no rankings found'))
    # res = make_response('no rankings found')
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res

@app.route('/api/get_roster_by_team', methods=['POST'])
def api_get_roster_by_team():
  print('running...')
  # get data from request
  data = request.get_json()
  id = data['team_id']
  #
  print(id)
  # 
  roster = Roster.get_by_team({'team_id': id})
  print(roster)
  if roster:
    # res = flask.Response(roster)
    res = make_response(roster)
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res
  else:
    res = flask.Response(json.dumps('no roster found'))
    # res = make_response('no roster found')
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res

@app.route('/api/new_ranks', methods=['POST'])
def api_new_ranks():
  print('running...')
  # get data from request
  data = request.get_json()
  #
  print(data)
  # 
  ranking_data = {
    "team_id": data['teamId'],
    "players": json.dumps(data['players'])
  }
  #
  ranking = Ranking.new(ranking_data)
  print(ranking)
  if ranking:
    res = flask.Response(json.dumps('ranks created'))
    # res = make_response('ranks created')
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res
  else:
    res = flask.Response(json.dumps('error creating ranks'))
    # res = make_response('ranks not created')
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res

@app.route('/api/save_ranks', methods=['POST'])
def api_save_ranks():
  print('running...')
  # get data from request
  data = request.get_json()
  #
  print(data)
  # 
  ranking_data = {
    "id": data['id'],
    "players": json.dumps(data['players'])
  }
  #
  ranking = Ranking.update(ranking_data)
  print(ranking)
  if ranking:
    res = flask.Response(json.dumps('ranks saved'))
    # res = make_response('ranks saved')
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res
  else:
    res = flask.Response(json.dumps('error saving ranks'))
    # res = make_response('ranks not saved')
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res

@app.route("/api/recommendations", methods=['POST'])
def api_display_results():
  #
  data = request.get_json()
  #
  print(data)
  # check for advanced settings and redirect
  # if "qb_select" in data:
  #     return redirect("/api/recommendations/advanced", code = 307)
  # retrieve data from user input, run draft_order function to determine "user_picks"
  new_data = {
      "num_of_teams": int(data['numOfTeams']),
      "draft_position": int(data['draftPosition']),
      "num_of_rounds": general.get_num_of_rounds(data['roster']),
      "settings": data['roster'],
      # "user_picks": general.draft_order(data['num_of_teams'], data['draft_position'], data['draft_rounds'])
  }
  # call draft_order fuction to generate user_picks, then add them to the data
  user_picks = general.draft_order(new_data['num_of_teams'], new_data['draft_position'], new_data['num_of_rounds'])
  print(f'**USER PICKS*** {user_picks}')
  new_data.update({"user_picks": user_picks})

  # =========> NEED TO CHANGE THIS SO ONLY THE PLAYER IDs ARE SENT, NOT ALL THE DATA... THEN WE CAN FILTER ON THE FRONTEND <========= 

  # call pick_recs fuction to generate recommendations, then add them to the data
  player_recs = general.new_pick_recs(user_picks, new_data['num_of_teams'], new_data['settings'])
  # print(f'**PLAYER RECS*** {player_recs}')
  # new_data.update({"player_recs": player_recs})
  # declare variables needed to generate player targets
  # unsorted_players = player_recs[:]
  # generate targets, then add them to the data
  # sorted_players = general.new_sort_by_value(player_recs, [])
  # print(f'**SORTED PLAYERS*** {sorted_players}')
  # player_targets = sorted_players[:]
  new_data['player_targets'] = []
  for player in player_recs:
    new_data['player_targets'].append(player['id'])
  # new_data['player_targets'] = player_recs
  # return render_template("results.html",  data = data)
  print(f'RECS => {new_data["player_targets"]}')
  res = flask.Response(json.dumps(new_data))
  # res = make_response(json.dumps(new_data))
  res.headers['Access-Control-Allow-Origin'] = '*'
  # print(f'RES => {res}')
  # print(f'USER PICKS => {user_picks}')
  return res

@app.route("/api/recommendations/advanced", methods=['POST'])
def api_display_advanced_results():
  #
  data = request.get_json()
  #
  print(data)
  # retrieve data from user input, run draft_order function to determine "user_picks"
  new_data = {
      "team_name": data['team_name'],
      "league": data['league_name'],
      "num_of_teams": int(data['num_of_teams']),
      "draft_position": int(data['draft_position']),
      "num_of_rounds": int(data['draft_rounds']),
      "user_picks": general.draft_order(data['num_of_teams'], data['draft_position'], data['draft_rounds']),
      "qb_select": data['qb_select'],
      "rb_select": data['rb_select'],
      "wr_select": data['wr_select'],
      "te_select": data['te_select'],
      "flex_select": data['flex_select'],
      "super_flex": data['super_flex'],
      "no_defenses": data['no_defenses'],
      "no_kickers": data['no_kickers'],
      "rd1_priority": data['rd1_priority'],
      "rd2_priority": data['rd2_priority'],
      "rd3_priority": data['rd3_priority'],
      "rd4_priority": data['rd4_priority'],
      "rd5_priority": data['rd5_priority'],
      "rd6_priority": data['rd6_priority'],
      "target_player": data['target_player']
  }
  # call pick_recs fuction to generate recommendations, then add them to the data that is passed to the html template
  player_recs = general.pick_recs(data['user_picks'], data['num_of_teams'], options = data)
  new_data.update({"player_recs": player_recs})
  # declare variables needed to generate player targets
  sorted_players = []
  unsorted_players = player_recs[:]
  # generate targets, then add them to the data that is passed to the html template
  general.sort_by_value(unsorted_players, sorted_players)
  player_targets = sorted_players[:]
  new_data.update({"player_targets": player_targets})

  # check that user is logged in
  # if "user_id" in session:
  #     new_data.update({
  #         "settings": json.dumps(data),
  #         "logged_in": True,
  #         "user_id": session['user_id']
  #     })
  #     team = Team.new(data)
  #     new_data.update({"team": team})

  # return render_template("results.html",  data = data)
  res = make_response(json.dumps(new_data))
  res.headers['Access-Control-Allow-Origin'] = '*'
  return res