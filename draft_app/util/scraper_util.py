from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.keys import Keys
from draft_app.controllers import general
import time
import json
import csv
# import re
import os

CHROME_DRIVER_PATH = os.getcwd() + '/draft_app/static/chromedriver.exe'
# CHROME_DRIVER_PATH = 'https://storage.googleapis.com/chrome-for-testing-public/127.0.6533.99/win64/chrome-win64.zip'
# FANTASY_PROS_URL = 'https://www.fantasypros.com/nfl/rankings/consensus-cheatsheets.php'
FANTASY_PROS_URL = 'https://www.fantasypros.com/nfl/rankings/half-point-ppr-cheatsheets.php'
ESPN_URL = 'https://fantasy.espn.com/football/players/projections'

# NAV_CLASS = 'Pagination inline-flex justify-center items-center mv6'
# LIST_CLASS = 'Pagination__list white-space-no-wrap'
# BUTTON_CLASS = 'Button Button--default Button--icon-noLabel Pagination__Button Pagination__Button--next'
NAV_CLASS = 'Pagination'
LIST_CLASS = 'Pagination__list'
BUTTON_CLASS = 'Pagination__Button--next'
TABLE_CLASS = 'ResponsiveTable'
ROW_CLASS = 'Table__TR'

PLAYERS_PER_PAGE = 50
MAX_PLAYERS = 600

ESPN_DATA_MAP = {
    'Rank': 'rank',
    'Each Pass Completed & Each Pass Attempted': 'pass_comp_and_att',
    'Passing Yards': 'pass_yds',
    'TD Pass': 'pass_td',
    'Interceptions Thrown': 'int',
    'Rushing Attempts': 'rush_att',
    'Rushing Yards': 'rush_yds',
    'TD Rush': 'rush_td',
    'Each reception': 'rec',
    'Receiving Yards': 'rec_yds',
    'TD Reception': 'rec_td',
    'Receiving Target': 'rec_tgt',
    'Average': 'avg_fpts',
}



def _get_chrome_driver():
    print('---------- setting up Selenium ----------')
    # Selenium Chrome service will get the right Chrome driver
    service = webdriver.ChromeService()
    # custom options
    options = webdriver.ChromeOptions()
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--incognito")
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=service, options=options)
    return driver


class ScraperUtil:
    def __init__(self):
        self.driver = _get_chrome_driver()


#
def scrape_and_parse_player_data():
    scraper_util = ScraperUtil()
    driver = scraper_util.driver
    
    print('---------- beginning Selenium SCRAPE ----------')
    url = FANTASY_PROS_URL
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
                if id.has_attr('data-player'):
                    player_ids.append(id['data-player'])
        # beautiful soup built-in to strip excess text
        columns = [element.text.strip() for element in columns]
        # add data to the "players" list
        players.append([element for element in columns if element])

    # @TODO get new data from UDK
    print('---------- fetching CONSISTENCY RATINGS ----------')
    consistency_ratings = {
        "QB": get_ballers_consistency_rating('qb'),
        "RB": get_ballers_consistency_rating('rb'),
        "WR": get_ballers_consistency_rating('wr'),
        "TE": get_ballers_consistency_rating('te')
    }

    print('---------- beginning DATA PARSING ----------')
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


def scrape_and_parse_espn_projections():
    scraper_util = ScraperUtil()
    driver = scraper_util.driver
    
    print('---------- beginning Selenium SCRAPE ----------')
    url = ESPN_URL
    driver.get(url)
    # let the page load
    time.sleep(2)
    # click the toggle for 'Sortable Projections'
    toggle = driver.find_element(By.CLASS_NAME, 'ButtonGroup').find_element(By.CLASS_NAME, 'Button')
    ActionChains(driver).move_to_element(toggle).pause(1).click(toggle).pause(1).perform()
    # let the page load then scroll down
    time.sleep(2)
    driver.execute_script("window.scrollTo(0, 1000)")
    
    html = driver.page_source
    
    soup = BeautifulSoup(html)
    
    navigation = soup.find('nav', attrs={'class': NAV_CLASS})
    pagination_list = navigation.find('ul', attrs={'class': LIST_CLASS})
    
    list_items = pagination_list.find_all('li')
    last_item = list_items[len(list_items) - 1]
    item_text = last_item.find('a').text.strip()
    print(f'TOTAL PAGES =====> (( {item_text} ))')
    total_pages = int(item_text)
    pages_to_scrape = MAX_PLAYERS / PLAYERS_PER_PAGE
    pages = min(total_pages, pages_to_scrape)
    print(f'PAGES TO SCRAPE =====> (( {int(pages)} ))')
    player_projections = {}
    for i in range(int(pages)):
        # let the page load new data
        time.sleep(5)
        driver.execute_script("window.scrollTo(0, 1000)")
        
        # get a fresh page source
        new_html = driver.page_source
        new_soup = BeautifulSoup(new_html)
        
        players_table = new_soup.find('div', attrs={'class': TABLE_CLASS}).find('div', attrs={'class': 'flex'})
        tables = players_table.find_all('table')
        players_list = {}
        for table in tables:
            body = table.find('tbody')
            rows = body.find_all('tr', attrs={'class': ROW_CLASS})
            print(f'NUM ROWS =====> (( {len(rows)} ))')
            for j in range(len(rows)):
                player = players_list.get(j, {})
                # 
                cells = rows[j].find_all('td')
                for data in cells:
                    formatted_dict = _extract_title_and_value(data)
                    if formatted_dict is not None:
                        formatted_keys = formatted_dict.keys()
                        for formatted_key in formatted_keys:
                            if formatted_key in player.keys():
                                raise ValueError(f'Duplicate key found trying to update player dict key "{formatted_key}" (value: "{player[formatted_key]}") with new value "{formatted_dict[formatted_key]}".')
                        player.update(formatted_dict)
                key = j
                players_list.update({key: player})
        
        for key, player in players_list.items():
            formatted_player = _format_espn_player(player)
            player_projections.update({formatted_player['name']: formatted_player})
        
        nav = driver.find_element(By.CLASS_NAME, NAV_CLASS)
        button = nav.find_element(By.CLASS_NAME, BUTTON_CLASS)
        
        if button.is_enabled():
            ActionChains(driver).move_to_element(button).pause(1).click(button).pause(1).perform()
        
    return player_projections


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
    # print(f'player = {player}')
    
    first_name = player[0]
    last_name = player[1]
    # name = ''
    team = ''
    
    # need to deal with this exception: ['Josh', 'Jacobs', '(LV)', 'Q']
    for i in range(len(player)):
        if i > 1:
            if player[i].endswith(')'):
                team = player[i].split('(')
                team = team[1].split(')')[0]
                break
            last_name += f' {player[i]}'
            
    name = f'{first_name} {last_name}'
    
    # exceptiopn, i.e. ['Amon-Ra', 'St.', 'Brown', '(DET)']
    # if len(player) == 4:
    #     first_name = player[0]
    #     last_name = f'{player[1]} {player[2]}'
    #     name = f'{first_name} {last_name}'
    #     team = player[3].split('(')
    #     team = team[1].split(')')[0]
    #     return name, team
    # # all other players, i.e. ['Trevor', 'Lawrence', '(JAX)']
    # first_name = player[0]
    # last_name = player[1]
    # name = f'{first_name} {last_name}'
    # team = player[2].split('(')
    # team = team[1].split(')')[0]
    
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


#
def _format_espn_player(player):
    if player is None:
        raise ValueError('Player is None')
    if len(player) == 0:
        raise ValueError('Player is empty')
    # return {
    #     'rank': player[0],
        
    # }
    return player

# NEEDS TO DO:
#   1. remove unnecessary cols
#       - stars with: [ 'Percent', 'Change in Percent' ]
#   
#   2. match 'title' to a map that gets desired value
#       ex: { 'TD Pass': 'pass_td' }
#   
#   3. ?
#
def _extract_title_and_value(data):
    title = data.get('title')
    if title is None:
        titles = data.select('div[title]')
        if len(titles) != 0:
            title = titles[0].get('title')
    return _filter_and_normalize_data(title, data)

def _filter_and_normalize_data(title, data):
    if title is None:
        return None
    if title == '' or title == 'Action':
        return None
    if title.startswith('Percent') or title.startswith('Change in Percent'):
        return None
    if title in ESPN_DATA_MAP.keys():
        return {
            ESPN_DATA_MAP.get(title): data.text.strip()
        }
    split_title = title.split(' ')
    if split_title[1] == 'points':
        return {
            'total_fpts': split_title[0]
        }
    return {
        'name': title
    }
