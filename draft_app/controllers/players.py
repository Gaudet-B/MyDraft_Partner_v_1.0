from flask import app
from flask import render_template, request, redirect, session, flash
from werkzeug.utils import redirect
from draft_app import app
from draft_app.models.user import User, Admin
from draft_app.models.player import Player
from draft_app.controllers import general


# --> Display Routes <--

# confirm creation
@app.route("/players/create/confirm")
def show_all_created():
    players= []
    return render_template("players_created.html", players = players)


# --> Action Routes <--

# display results
@app.route("/players/results", methods=['POST'])
def display_results():
    # check for advanced settings and redirect
    if "qb_select" in request.form:
        return redirect("/players/results/advanced", code = 307)
    # retrieve data from user input, run draft_order function to determine "user_picks"
    data = {
        "team_name": request.form['team_name'],
        "num_of_teams": int(request.form['num_of_teams']),
        "draft_position": int(request.form['draft_position']),
        "num_of_rounds": int(request.form['draft_rounds']),
        "user_picks": general.draft_order(request.form['num_of_teams'], request.form['draft_position'], request.form['draft_rounds'])
    }
    # check that user is logged in
    if "user_id" in session:
        data.update({"logged_in": True})
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

    return render_template("results.html",  data = data)

# advanced results
@app.route("/players/results/advanced", methods=['POST'])
def display_advanced_results():
    # retrieve data from user input, run draft_order function to determine "user_picks"
    data = {
        "team_name": request.form['team_name'],
        "num_of_teams": int(request.form['num_of_teams']),
        "draft_position": int(request.form['draft_position']),
        "num_of_rounds": int(request.form['draft_rounds']),
        "user_picks": general.draft_order(request.form['num_of_teams'], request.form['draft_position'], request.form['draft_rounds']),
        "qb_select": request.form['qb_select'],
        "rb_select": request.form['rb_select'],
        "wr_select": request.form['wr_select'],
        "te_select": request.form['te_select'],
        "flex_select": request.form['flex_select'],
        "super_flex": request.form['super_flex'],
        "no_defenses": request.form['no_defenses'],
        "no_kickers": request.form['no_kickers'],
        "rd1_priority": request.form['rd1_priority'],
        "rd2_priority": request.form['rd2_priority'],
        "rd3_priority": request.form['rd3_priority'],
        "rd4_priority": request.form['rd4_priority'],
        "rd5_priority": request.form['rd5_priority'],
        "rd6_priority": request.form['rd6_priority'],
        "target_player": request.form['target_player']
    }
    # check that user is logged in
    if "user_id" in session:
        data.update({"logged_in": True})
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

    return render_template("results.html",  data = data)

# create
@app.route("/players/create", methods=['POST'])
def create_players():
    data = {
            "email": request.form['email_create'],
            "password": request.form['password_create']
        }
    # confirm admin credentials
    if not Admin.validate_login(data):
        return redirect("/admin")
    else:
        admin = Admin.get_admin_by_email(data)
        session['user_id'] = admin.id
        session['is_admin'] = admin.is_admin
        return redirect ("/players/create/confirm")
