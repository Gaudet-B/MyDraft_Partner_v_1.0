from draft_app.models.player import DATABASE
from draft_app.config.mysqlconnection import connectToMySQL


# data structure for autocomplete search
class trieNode:
    def __init__(self):
        self.next = {}
        self.leaf = False
    # 
    def add_item(self, item):
        i = 0
        while i < len(item):
            k = item[i]
            if not k in self.next:
                node = trieNode()
                self.next[k] = node
            self = self.next[k]
            if i == len(item) - 1: 
                self.leaf = True
            else:
                self.leaf = False
            i += 1
    # 
    def search(self, item):
        if self.leaf and len(item) == 0:
            return True
        first = item[:1]  
        str = item[1:]  
        if first in self.next:
            return self.next[first].search(str)
        else:
            return False
    # 
    def traversal(self, item):
        if self.leaf:
            print (item)
        for i in self.next:
            s = item + i
            self.next[i].traversal(s)
    # 
    def autocomplete(self, item):
        i = 0
        s = ''
        while i < len(item):
            k = item[i]
            s += k
            if k in self.next:
                self = self.next[k]
            else:
                return 'NOT FOUND'
            i += 1
        self.traversal(s)
        return 'END'

# function that gets all player names and returns an alphabetized list
def get_player_names():
    query = "SELECT name FROM players"
    results = connectToMySQL(DATABASE).query_db(query)
    names_list = []
    for i in range(len(results)):
        names_list.append(results[i]['name'])
    # json_names = json.dumps(names_list)
    # print(json_names)
    # return json_names
    return names_list

# function that returns a list the overall picks to be drafted
def draft_order(teams, spot, rounds):

    # set global variables for function
    picks = []
    round = 1
    pick = 1

    # number of iterations based on user-provided "rounds"
    for p in range(int(rounds)):

        # a "snake" draft runs in ascending order on odd rounds, and descending order on even rounds
        # odd rounds
        if round % 2 != 0:

            # start at first pick (pick #1) and increment
            i = 1
            while i <= int(teams):

                # when each round's pick matches user-provided "spot", add the corresponding overall pick to the "picks" list
                if i == int(spot):
                    picks.append(pick)
                
                # increment overall pick
                pick += 1
                # increment round order
                i += 1
        
        # even rounds
        elif round % 2 == 0:
            
            # start at last pick (pick #{number of teams}) and decrement
            j = int(teams)
            while j > 0:
                
                # when each round's pick matches user-provided "spot", add the corresponding overall pick to the "picks" list
                if j == int(spot):
                    picks.append(pick)

                # increment overall pick
                pick +=1
                # decrement round order
                j -= 1
        
        # increment to next round
        round += 1

    return picks


# function to find the lowest ECR rank in the given list
def find_max_ecr(player_list):
    # start at first index
    max_ecr = player_list[0]
    # loop through
    for i in range(len(player_list)):
        # check current max against next index
        if player_list[i]['ecr_rank'] < max_ecr['ecr_rank']:
            # reset max
            max_ecr = player_list[i]
    
    return max_ecr


# function that, given an unsorted list and an empty list, removes all elements from the first list and appends them to the second list in order 
def sort_by_ecr(unsorted_players, sorted_players):
    # call find_max_ecr function to get the lowest ECR rank from the list
    max_ecr = find_max_ecr(unsorted_players)
    # add that player to the sorted list
    sorted_players.append(max_ecr)
    # and remove from the unsorted list
    unsorted_players.remove(max_ecr)
    # base case for recursive calls
    if len(unsorted_players) < 1:
        sorted = sorted_players
        return sorted

    else:
        # recursively calls itself until base case is met
        sort_by_ecr(unsorted_players, sorted_players)


# function that sets options for pick_recs()
def set_options(settings):
    options = {
        "positions": {
        "qb": { "min": 1, "max": 2 }, 
        "rb": { "min": 5, "max": 6 },
        "wr": { "min": 5, "max": 6 },
        "te": { "min": 1, "max": 2 },
        "dst": { "min": 1, "max": 1 },
        "k": { "min": 1, "max": 1 }
        },
        "priorities": {
            0: False,
            1: "rb",
            2: "wr",
            3: "te",
            4: "qb"
        }
    }

    

    return options


# ==========================================================================================================================================
# ==========================================================================================================================================

def get_player_position(pos_rank):
    position = ''
    if pos_rank[0] == 'D':
        position += pos_rank[0:3].lower()
    elif pos_rank[0] == 'K':
        position += pos_rank[0].lower()
    else:
        position += pos_rank[0:2].lower()
    # print(f'184 {position}')
    return position

# determines the number of draft rounds based on the roster settings
def get_num_of_rounds(roster):
    num_of_rounds = 0
    positions = roster.keys()
    for position in positions:
        if position == 'bench':
            num_of_rounds += roster[position]['max']
        else :
            num_of_rounds += roster[position]['starters']
    return num_of_rounds

def new_sort_by_value(players, values):
    new_players = players[:]
    # print(f'PLAYERS =======> {players}')
    new_values = values[:]
    # print(f'VALUES =======> {values}')
    max_value = get_max_value(players)
    new_values.append(max_value)
    new_players.remove(max_value)
    if len(new_players) < 1:
        # print(f'SORTED RECS =======> {new_values}')
        return new_values
    else:
        new_sort_by_value(new_players, new_values)

def new_pick_recs(picks, teams, settings):
# default options if none are specified
# settings = { 
#     "positions": {
#         "qb": { "min": 1, "max": 2 }, 
#         "rb": { "min": 5, "max": 6 },
#         "wr": { "min": 5, "max": 6 },
#         "te": { "min": 1, "max": 2 },
#         "dst": { "min": 1, "max": 1 },
#         "k": { "min": 1, "max": 1 }
#     },
#     "priorities": {
#         0: False,
#         1: "rb",
#         2: "wr",
#         3: "te",
#         4: "qb"
#     }
#     }):

    # set global variables for function
    recs = []
    selected = {
        "qb": 0,
        "rb": 0,
        "wr": 0,
        "te": 0,
        "dst": 0,
        "k": 0
    }

    # if "qb_select" in settings.keys():
    #     options = set_options(settings)
    # else:
    #     options = settings
        

    # print(settings)
    # print(options)

    # for each pick, a query will be made to the database, a range will be created/sorted, and one recommendation will be given
    for i in range(len(picks)):
        # set local variables for each iteration
        player_range = []
        sorted_range = []
        # MySQL query
        query = "SELECT * FROM players WHERE current_adp > " + str(picks[i]-1) + " AND current_adp < " + str(picks[i]+(teams*2)+2) + " ;"
        results = connectToMySQL(DATABASE).query_db(query)

        # iterate through results, creating a range of players
        for result in results:
            # print(f'##### POSITION: {result["positional_rank"]}')
            player_position = get_player_position(result['positional_rank'])
            # print(f'##### POSITION: {player_position}')
            # if this is the first pick, we need to look at all players
            if len(recs) == 0:
                player_range.append(result)
            # check to see if a player already exists in the "recs" list, if so skip
            elif result in recs:
                pass
            # check to see if a position has already reached it's max value (from user-provided "settings"), if so skip
            elif selected[player_position] == settings[player_position]['max']:
                pass
            else:
                # add player to the range
                player_range.append(result)

        # call sort_by_ecr function to sort the range
        sort_by_ecr(player_range, sorted_range)

        # set local variables to move through the range
        count = 0
        rec = sorted_range[count]

        # check one more time for duplicates
        while rec in recs:
            # skip any duplicate players
            count += 1
            rec = sorted_range[count]

        player_position = get_player_position(rec['positional_rank'])
        # print(f'##### POSITION: {player_position}')

        # towards the end of the draft, prioritize positions that have not had minimum requirements met
        # qb after rd 7
        # te, dst, k last 4 rounds
        if i >= len(picks) - 4:
            # boolean variable that will determine if all minimum requirements have been met - default is True
            minReqs = True
            # check each position to see if minimum requirements have ben met
            for position in selected:
                if selected[position] >= settings[position]['starters']:
                    pass
                # if any one of the positions doesn't meet this check, the boolean variable is set to false
                else:
                    minReqs = False

            # when there are still minimums to meet
            if minReqs == False:

                # check to see if the position of the current player has had it's minimum met
                while selected[player_position] >= settings[player_position]['starters'] and count < len(sorted_range):
                    # skip players with positions that have had their minimum met
                    rec = sorted_range[count]
                    count += 1
            
            # increment the value from the "selected" dict who's key matches the position of the current player
            selected[player_position] += 1

            # add the current player to the "recs" list
            recs.append(rec)
            # reset local variables for next iteration
            player_range = []
            sorted_range = []
            # move to next iteration, ignore all of the following code
            continue

        # @NOTE use the following logic to build the fine-tuned recommendation algorithm (i.e. weights determined by user input)
        # current version usually doesn't select QB until the end (last 4 rounds), which is... fine?

        # ======================================================================================================
        # ======================================================================================================

        # # after round 7, prioritize qb ==> sometimes a QB was not selected
        # # @NOTE this is just a bandaid... need to dial in the logic of this recommendation algorithm
        # if i > 6:
        #     position_to_find = get_player_position(rec['positional_rank'])
        #     # @NOTE *** a way to "weight" the selection of a specific position over a number of rounds would be to change how "far" into the selected_rage we look for a QB
        #     # (at some point we have to look through the entire range, essentially focing a QB to be selected)

        #     # @NOTE this is imperfect because if an eligeble player is "skipped" when looking for a QB, K or DST we don't go back and select them

        #     if i > 8:

        #         if i > 10:
        #             # after round 11 force qb by going through entire range until one is selected
        #             while position_to_find != "qb" and count < len(sorted_range):
        #                 # skip any non-QBs
        #                 count += 1
        #                 rec = sorted_range[count]
        #                 position_to_find = get_player_position(rec['positional_rank'])
        #         # after round 9 go through the first half, making sure we don't give up too much "value" by focing QB
        #         while position_to_find != "qb" and count < len(sorted_range) / 2:
        #             # skip any non-QBs
        #             count += 1
        #             rec = sorted_range[count]
        #             position_to_find = get_player_position(rec['positional_rank'])
        #     # after round 7 go through the first quarter, making sure we still select a high "value" player and
        #     while position_to_find != "qb" and count < len(sorted_range) / 4:
        #         # skip any non-QBs
        #         count += 1
        #         rec = sorted_range[count]
        #         position_to_find = get_player_position(rec['positional_rank'])

        #     selected[player_position] += 1
        #     recs.append(rec)
        #     player_range = []
        #     sorted_range = []
        #     continue

        # ======================================================================================================
        # ======================================================================================================


        # early rounds, prioritize best player (biggest difference between adp and ecr)
        else:

            # do not select kickers or defenses unless it is one of the final 5 rounds
            while player_position == "dst" or player_position == "k":
                # skip any kickers or defenses
                count += 1
                rec = sorted_range[count]

            # increment the value from the "selected" dict who's key matches the position of the current player
            # print(f' ?????? {selected} ?????? {player_position} ?????? ')
            selected[player_position] += 1

            # add the current player to the "recs" list
            recs.append(rec)
            # reset local variables for next iteration
            player_range = []
            sorted_range = []
    print(f'RECOMMENDATIONS {recs}')
    return recs

# ==========================================================================================================================================
# ==========================================================================================================================================

# function to determine the recommended players, round-by-round, based on user-provided options or the default options
def pick_recs(picks, teams, 
# default options if none are specified
settings = { 
    "positions": {
        "qb": { "min": 1, "max": 2 }, 
        "rb": { "min": 5, "max": 6 },
        "wr": { "min": 5, "max": 6 },
        "te": { "min": 1, "max": 2 },
        "dst": { "min": 1, "max": 1 },
        "k": { "min": 1, "max": 1 }
    },
    "priorities": {
        0: False,
        1: "rb",
        2: "wr",
        3: "te",
        4: "qb"
    }
    }):

    # set global variables for function
    recs = []
    selected = {
        "qb": 0,
        "rb": 0,
        "wr": 0,
        "te": 0,
        "dst": 0,
        "k": 0
    }

    if "qb_select" in settings.keys():
        options = set_options(settings)
    else:
        options = settings
        

    print(settings)
    print(options)

    # for each pick, a query will be made to the database, a range will be created/sorted, and one recommendation will be given
    for i in range(len(picks)):
        # set local variables for each iteration
        player_range = []
        sorted_range = []
        # MySQL query
        query = "SELECT * FROM players WHERE current_adp > " + str(picks[i]-1) + " AND current_adp < " + str(picks[i]+(teams*2)+2) + " ;"
        results = connectToMySQL(DATABASE).query_db(query)

        # iterate through results, creating a range of players
        for result in results:
            # if this is the first pick, we need to look at all players
            if len(recs) == 0:
                player_range.append(result)
            # check to see if a player already exists in the "recs" list, if so skip
            elif result in recs:
                pass
            # check to see if a position has already reached it's max value (from user-provided "options"), if so skip
            elif selected[result['position'].lower()] == options['positions'][result['position'].lower()]['max']:
                pass
            else:
                # add player to the range
                player_range.append(result)

        # call sort_by_ecr function to sort the range
        sort_by_ecr(player_range, sorted_range)

        # set local variables to move through the range
        count = 0
        rec = sorted_range[count]

        # check one more time for duplicates
        while rec in recs:
            # skip any duplicate players
            count += 1
            rec = sorted_range[count]

        # towards the end of the draft, prioritize positions that have not had minimum requirements met
        if i >= len(picks) - 5:
            # boolean variable that will determine if all minimum requirements have been met - default is True
            minReqs = True

            # check each position to see if minimum requirements have ben met
            for position in selected:
                if selected[position] >= options[position]['min']:
                    pass
                # if any one of the positions doesn't meet this check, the boolean variable is set to false
                else:
                    minReqs = False

            # when there are still minimums to meet
            if minReqs == False:
            
                # check to see if the position of the current player has had it's minimum met
                while selected[rec['position'].lower()] >= options[rec['position'].lower()]['min']:
                    # skip players with positions that have had their minimum met
                    count += 1
                    rec = sorted_range[count]
            
            # increment the value from the "selected" dict who's key matches the position of the current player
            selected[rec['position'].lower()] += 1

            # add the current player to the "recs" list
            recs.append(rec)
            # reset local variables for next iteration
            player_range = []
            sorted_range = []
            # move to next iteration, ignore all of the following code
            continue

        # all picks, excluding the final 5, which were handled above
        else:

            # do not select kickers or defenses unless it is one of the final 5 rounds
            while rec['position'].lower() == "dst" or rec['position'].lower() == "k":
                # skip any kickers or defenses
                count += 1
                rec = sorted_range[count]

            # increment the value from the "selected" dict who's key matches the position of the current player
            selected[rec['position'].lower()] += 1

            # add the current player to the "recs" list
            recs.append(rec)
            # reset local variables for next iteration
            player_range = []
            sorted_range = []

    return recs


# function to sort recommendations by value
def sort_by_value(players, values):
    # call get_max_value function to return the player from the list with the max value
    max_value = get_max_value(players)
    # add that player to the values list
    values.append(max_value)
    # and remove from players list
    players.remove(max_value)
    # base case for recursive calls
    if len(players) < 1:
        # make a copy of the list
        targets = values[:]
        return targets
    else:
        # recursively calls itself until base case it met
        sort_by_value(players, values)

# function to determine the value of a player
def get_value(player):
    value = int(player['current_adp']) - int(player['ecr_rank'])
    # print(f'$$$$$$ VALUE $$$ {value}')
    return value


# function to determine which player from the list has the greatest value
def get_max_value(players):
    # set the max as the first index
    max_value = players[0]
    # loop through the list
    for i in range(len(players)):
        current_value = get_value(max_value)
        # print(f'$$$$$$ CURRENT VALUE $$$ {current_value}')
        new_value = get_value(players[i])
        # print(f'$$$$$$ NEW  VALUE $$$ {new_value}')
        # check current max against the next index
        if new_value > current_value:
            max_value = players[i]
    
    return max_value


def split_string(str):
    return str.split()