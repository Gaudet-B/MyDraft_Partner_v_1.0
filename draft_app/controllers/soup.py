from flask import app
from flask import render_template, redirect, request, session, flash
from draft_app import app
from draft_app.models.user import User, Admin
from draft_app.models.player import Player
from draft_app.controllers import general
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from flask_bcrypt import Bcrypt
import re
import time

bcrypt = Bcrypt(app)


# --> Display Routes <--

# admin login page
@app.route("/admin")
def admin_login():
    session.clear()
    return render_template("dev_login.html")

# database management page
@app.route("/dev_controls")
def dev_controls():
    if "is_admin" not in session:
        return redirect("/admin")
    else:
        return render_template("dev_controls.html")


# --> Action Routes <--

# update database
@app.route("/dev_controls/update", methods=['POST'])
def update():
    data = {
                "email": request.form['email_update'],
                "password": request.form['password_update']
            }
    # confirm admin credentials
    if not Admin.validate_login(data):
        return redirect("/admin")
    
    else:
        
        # > SELENIUM SETUP <

        # use Chrome driver options
        options = webdriver.ChromeOptions()
        # custom options
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--incognito")
        options.add_argument("--headless")
        path = "../static/chromedriver.exe"
        driver = webdriver.Chrome(executable_path=path, chrome_options=options)

        # > SELENIUM SCRAPE <

        url = "https://www.fantasypros.com/nfl/rankings/consensus-cheatsheets.php"
        driver.get(url)
        # allow Selenium time to scroll page
        time.sleep(5)
        # scrolls down the page to trigger loading of the entire list
        driver.execute_script("window.scrollTo(0, 500)")
        # allow Selenium to finish scraping
        time.sleep(3)
        # creates a representation of the html elements on the page
        html = driver.page_source

        # > BEAUTIFUL SOUP EXTRACTION <

        # creates a Beautiful Soup document
        soup = BeautifulSoup(html)
        # player table
        table = soup.find("table", attrs={"id":"ranking-table"})
        # body of table
        body = table.find("tbody")
        # all rows in table body
        rows = body.find_all("tr")
        # empty array that will store players
        players = []
        # iterate through table rows 
        for row in rows:
            columns = row.find_all("td")
            # beautiful soup built-in to strip excess text
            columns = [element.text.strip() for element in columns]
            # add data to the "players" list
            players.append([element for element in columns if element])
        
        # iterate through "players" list
        for player in players:
            # handle edge case where there are periodic breaks in the usable data
            if player[0][0] != "T":
                # retreive all player names from database
                player_name_list = Player.get_all_names()
                # pull each player name from the data
                player_name = general.split_string(player[1])
                full_name = player_name[0] + " " + player_name[1]
                # conditionals that handle different lengths and formats of player positions
                if player[2][0] == "D":
                    player_position = player[2][0:3]
                elif player[2][0] == "K":
                    player_position = player[2][0]
                else:
                    player_position = player[2][0:2]
                # check players from data against players from database -> if this is a new player, create a new instance of the Player class
                if full_name not in player_name_list:
                    # edge cases where negative integers are parsed differently 
                    if player[5] == "-":
                        new_edge_data = {
                            "name": player_name[0] + " " + player_name[1],
                            "team": player_name[2],
                            "position": player_position,
                            "ecr_rank": float(player[0]),
                            "positional_rank": player[2],
                            "current_adp": float(player[0]),
                            "difference": 0
                        }
                        # create a new instance of the Player class
                        Player.new(new_edge_data)
                    # cases with positive integers - handle normally
                    else:
                        new_player_data = {
                            "name": player_name[0] + " " + player_name[1],
                            "team": player_name[2],
                            "position": player_position,
                            "ecr_rank": float(player[0]),
                            "positional_rank": player[2],
                            "current_adp": float(player[0]),
                            "difference": float(player[5])
                            }
                        # create a new instance of the Player class
                        Player.new(new_player_data)
                
                # if this player already exists in the database, update that player with the new data
                else:
                    # edge cases where negative integers are parsed differently 
                    if player[5] == "-":
                        edge_case_data = {
                            "name": player_name[0] + " " + player_name[1]
                        }
                        # retreive Player from database
                        update_edge = Player.get_player_by_name(edge_case_data)
                        update_edge_data = {
                            "id": update_edge[0]['id'],
                            "team": player_name[1],
                            "ecr_rank": float(player[0]),
                            "positional_rank": player[2],
                            "current_adp": float(player[0]),
                            "difference": 0
                        }
                        # update Player from database
                        Player.update(update_edge_data)
                    # cases with positive integers - handle normally
                    else:
                        player_data = {
                            "name": player_name[0] + " " + player_name[1]
                        }
                        # retreive Player from database
                        update = Player.get_player_by_name(player_data)
                        update_data = {
                            "id": update[0]['id'],
                            "team": player_name[1],
                            "ecr_rank": float(player[0]),
                            "positional_rank": player[2],
                            "current_adp": float(player[0]) - float(player[5]),
                            "difference": float(player[5])
                        }
                        # update Player from database
                        Player.update(update_data)

        return redirect("/dev_controls")

# create new database
@app.route("/dev_controls/create", methods=['POST'])
def create():
    data = {
                "email": request.form['email_create'],
                "password": request.form['password_create']
            }
    # confirm admin credentials
    if not Admin.validate_login(data):
        return redirect("/admin")
    
    else:

        # > SELENIUM SETUP <

        # use Chrome driver options
        options = webdriver.ChromeOptions()
        # custom options
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--incognito")
        options.add_argument("--headless")
        path = "../static/chromedriver.exe"
        driver = webdriver.Chrome(executable_path=path, chrome_options=options)

        # > SELENIUM SCRAPE <

        url = "https://www.fantasypros.com/nfl/rankings/consensus-cheatsheets.php"
        driver.get(url)
        # allow Selenium time to scroll page
        time.sleep(5)
        # scrolls down the page to trigger loading of the entire list
        driver.execute_script("window.scrollTo(0, 500)")
        # allow Selenium to finish scraping
        time.sleep(3)
        # creates a representation of the html elements on the page
        html = driver.page_source

        # > BEAUTIFUL SOUP EXTRACTION <

        # creates a Beautiful Soup document
        soup = BeautifulSoup(html)
        # player table
        table = soup.find("table", attrs={"id":"ranking-table"})
        # body of table
        body = table.find("tbody")
        # all rows in table body
        rows = body.find_all("tr")
        # empty array that will store players
        players = []
        # iterate through table rows 
        for row in rows:
            columns = row.find_all("td")
            # beautiful soup built-in to strip excess text
            columns = [element.text.strip() for element in columns]
            # add data to the "players" list
            players.append([element for element in columns if element])
        
        # iterate through "players" list
        for player in players:
            # handle edge case where there are periodic breaks in the usable data
            if player[0][0] != "T":
                # pull each player name from the data
                player_name = general.split_string(player[1])
                # conditionals that handle different lengths and formats of player positions
                if player[2][0] == "D":
                    player_position = player[2][0:3]
                elif player[2][0] == "K":
                    player_position = player[2][0]
                else:
                    player_position = player[2][0:2]
                # edge cases where negative integers are parsed differently 
                if player[5] == "-":
                    edge_case_data = {
                        "name": player_name[0] + " " + player_name[1],
                        "team": player_name[2],
                        "position": player_position,
                        "ecr_rank": float(player[0]),
                        "positional_rank": player[2],
                        "current_adp": float(player[0]),
                        "difference": 0
                    }
                    # create a new instance of the Player class
                    Player.new(edge_case_data)
                # cases with positive integers - handle normally
                else:
                    player_data = {
                        "name": player_name[0] + " " + player_name[1],
                        "team": player_name[2],
                        "position": player_position,
                        "ecr_rank": float(player[0]),
                        "positional_rank": player[2],
                        "current_adp": float(player[0]) + float(player[5]),
                        "difference": float(player[5])
                    }
                    # create a new instance of the Player class
                    Player.new(player_data)

        return redirect("/dev_controls")

# admin login
@app.route("/admin/login", methods=['POST'])
def dev_login():
    data = {
            "email": request.form['email_login'],
            "password": request.form['password_login']
        }
    # confirm admin credentials
    if not Admin.validate_login(data):
        return redirect("/admin")
    else:
        admin = Admin.get_admin_by_email(data)
        session['user_id'] = admin.id
        session['is_admin'] = admin.is_admin
        return redirect ("/dev_controls")

# create new admin
@app.route("/new_admin", methods=['POST'])
def add_admin():
    # use bcrypt to hash password
    pw_hash = bcrypt.generate_password_hash(request.form['password_admin'])
    data = {
        "user_name": request.form['user_name_admin'],
        "email":request.form['email_admin'],
        "password": pw_hash
    }
    # create a new instance of the Admin class
    admin = Admin.new(data)
    print(admin)
    session['user_id'] = admin
    session['is_admin'] = "y"
    return redirect("/dev_controls")