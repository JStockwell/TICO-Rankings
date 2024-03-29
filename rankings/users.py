# for every single category in every single game, export the whole leaderboard and write down the user IDs into a set
# and export into a csv

from utils.api_call import api_call
from utils.csv import save_csv_from_list
LEADERBOARD_URL = 'https://www.speedrun.com/api/v1/leaderboards/'
USER_URL = 'https://www.speedrun.com/api/v1/users/'

# Category Structure:
# Game: ico, sotc, sotc_2018, tlg
# Type: full_game, il
# Board: main, ce
# Category: any%, boss_rush, etc.

def process_full_game(reference_json, game, user_id_list):
    for board in reference_json[game]['categories']['full_game']: # main, ce
        categories = reference_json[game]['categories']["full_game"][board]
        for category in categories: # any%, boss_rush, etc.
            category_dict = reference_json[game]['categories']["full_game"][board][category]
            if category_dict['variations'] == None:
                data = api_call(f'{LEADERBOARD_URL}{game}/category/{category_dict["id"]}')
                for run in data['runs']:
                    for player in run['run']['players']:
                        if 'id' in player.keys():
                            user_id = player["id"]
                            user_id_list.append(user_id)

            else:
                for variation in category_dict['variations']:
                    url_values = ''
                    subcategory = category_dict['variations'][variation]
                    for var in subcategory["vars"]:
                        url_values += f'var-{var}={subcategory["vars"][var]}&'
                    data = api_call(f'{LEADERBOARD_URL}{game}/category/{category_dict["id"]}?{url_values}')
                    for run in data['runs']:
                        for player in run['run']['players']:
                            if 'id' in player.keys():
                                user_id = player["id"]
                                user_id_list.append(user_id)

    return user_id_list

def process_il(reference_json, game, user_id_list):
    boards = ["main", "ce"]
    for board in boards: # main, ce
        categories = reference_json[game]['categories']["il"][board]
        for category in categories: # any%, boss_rush, etc.
            category_dict = reference_json[game]['categories']["il"][board][category]
            for level in reference_json[game]['categories']["il"]["levels"]:
                level_id = reference_json[game]['categories']["il"]["levels"][level]["id"]
                if category_dict['variations'] == None:
                    data = api_call(f'{LEADERBOARD_URL}{game}/level/{level_id}/{category_dict["id"]}')
                    for run in data['runs']:
                        for player in run['run']['players']:
                            if 'id' in player.keys():
                                user_id = player["id"]
                                user_id_list.append(user_id)

    return user_id_list

def get_user_csv(reference_json):
    user_id_list = []
    for game in reference_json: # ico, sotc, sotc_2018, tlg
        types = reference_json[game]['categories']
        for type in types: # full_game and il
            if type == "il":
                user_id_list = process_il(reference_json, game, user_id_list)
            else:
                user_id_list = process_full_game(reference_json, game, user_id_list)

    user_id_list = list(dict.fromkeys(user_id_list))
    user_list = []
    
    for user_id in user_id_list:
        data = api_call(f'{USER_URL}{user_id}')
        user_list.append(data['names']['international'])

    csv_list = [user_id_list, user_list]
    save_csv_from_list(csv_list, ['User ID','Username'], "./files/users.csv")
    return user_list