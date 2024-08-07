from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from draft_app.controllers import general
import time
import json
import csv
# import re
import os


# @TODO refactor this into a class
#
def scrape_and_parse_player_data():
    print('---------- setting up Selenium ----------')
    # > SELENIUM SETUP <
    # use Chrome driver options
    options = webdriver.ChromeOptions()
    # custom options
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--incognito")
    options.add_argument("--headless")
    # path to Chrome driver
    path = os.getcwd() + '/draft_app/static/chromedriver.exe'
    # path = url_for("static", filename="chromedriver.exe")
    print(path)
    driver = webdriver.Chrome(path, chrome_options=options)

    print('---------- beginning Selenium SCRAPE ----------')
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

    print('---------- beginning BeautifulSoup EXTRACTION ----------')
    # > BEAUTIFUL SOUP EXTRACTION <
    # creates a Beautiful Soup document
    soup = BeautifulSoup(html)
    # player table
    table = soup.find("table", attrs={"id":"ranking-table"})
    # body of table
    body = table.find("tbody")
    # all rows containing player data
    rows = body.find_all("tr", attrs={"class":"player-row"})
    # empty array that will store player's unique id
    player_ids = []
    # empty array that will store players
    players = []
    # iterate through table rows 
    for row in rows:
      columns = row.find_all("td")
      for column in columns:
        player_id = column.find_all("div")
        for id in player_id:
          # print(f'PLAYER_ID: {id}')
          # print('--------------------')
          if id.has_attr('data-player'):
            player_ids.append(id['data-player'])
      # beautiful soup built-in to strip excess text
      columns = [element.text.strip() for element in columns]
      # add data to the "players" list
      players.append([element for element in columns if element])

    print('---------- fetching CONSISTENCY RATINGS ----------')
    # > CONSISTENCY RATINGS <
    consistency_ratings = {
        "QB": get_ballers_consistency_rating('qb'),
        "RB": get_ballers_consistency_rating('rb'),
        "WR": get_ballers_consistency_rating('wr'),
        "TE": get_ballers_consistency_rating('te')
    }

    print('---------- beginning DATA PARSING ----------')
    # > DATA PARSING <
    players_list = []
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
            current_adp = 0
            # edge cases where ecr and adp are equal 
            if player[5] == "-":
                current_adp = float(player[0])
            else:
              current_adp = float(player[0]) + float(player[5])
              name, team = _parse_player_name(player_name)
              consistency_t1, consistency_t2 = _get_player_consistency_rating(name, player_position, consistency_ratings)
              player_data = {
                  "name": name,
                  "team": team,
                  "position": player_position,
                  "ecr_rank": float(player[0]),
                  "positional_rank": player[2],
                  "current_adp": current_adp,
                  "f_pros_id": player_ids.pop(0),
                  "consistency_t1": _percentage_string_to_float(consistency_t1),
                  "consistency_t2": _percentage_string_to_float(consistency_t2)
              }
              players_list.append(player_data)
    return players_list


#
def _percentage_string_to_float(percentage_string):
    if percentage_string is None or not percentage_string.endswith('%'):
        return None
    percentage = float(percentage_string[:-1]) / 100
    return percentage


#
def _parse_player_name(player):
    if player is None:
        raise ValueError('Player is None')
    # exceptiopn, i.e. ['Amon-Ra', 'St.', 'Brown(DET)']
    if len(player) == 3:
        first_name = player[0]
        last_name = player[1]
        team = player[2].split('(')
        last_name = f'{last_name} {team[0]}'
        team = team[1].split(')')[0]
        name = f'{first_name} {last_name}'
        return name, team
    # all other players, i.e. ['Trevor', 'Lawrence(JAX)']
    first_name = player[0]
    last_name = player[1].split('(')
    team = last_name[1].split(')')[0]
    last_name = last_name[0]
    name = f'{first_name} {last_name}'
    return name, team


#
def _get_player_consistency_rating(player, position, consistency_ratings):
    if player is None:
        raise ValueError('Player is None')
    if position not in consistency_ratings.keys():
        return None, None
    player_consistency = consistency_ratings.get(position, {}).get(player, {})
    if player_consistency is None:
        return None, None
    return player_consistency.get('t1'), player_consistency.get('t2')


#
def get_ballers_consistency_rating(position):
    file_path = os.getcwd() + f'/draft_app/static/consistency/{position}.csv'
    with open(file_path, encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        #
        result = {}
        for row in csv_reader:
            # for key, value in row.items():
            player = row.get('Name')
            t1 = _get_t1_consistency(row)
            t2 = _get_t2_consistency(row)
            result[player] = {
                't1': t1,
                't2': t2
            }
        return result


#
def _get_t1_consistency(row):
    t1 = row.get('QB 1-6')
    if t1 is None:
        t1 = row.get('TE 1-6')
    if t1 is None:
        t1 = row.get('RB1')
    if t1 is None:
        t1 = row.get('WR1')
    return _remove_quotes(t1)


#
def _get_t2_consistency(row):
    t2 = row.get('Top 12')
    if t2 is None:
        t2 = row.get('Top 24')
    return _remove_quotes(t2)


#
def _remove_quotes(value):
    if value is None:
        return None
    return value.replace('"', '')


#
# def _preprocess_json(json_string):
#     if json_string is None:
#         return None
#     return json_string.replace('\\', '')
