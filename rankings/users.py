# for every single category in every single game, export the whole leaderboard and write down the user IDs into a set
# and export into a csv

import requests
LEADERBOARD_URL = 'https://www.speedrun.com/api/v1/leaderboards/'

# Category Structure:
# Game: ico, sotc, sotc_2018, tlg
# Type: full_game, il
# Board: main, ce
# Category: any%, boss_rush, etc.

def get_user_csv(reference_json):
    for game in reference_json: # ico, sotc, sotc_2018, tlg
        types = reference_json[game]['categories']
        for type in types: # full_game and il
            boards = reference_json[game]['categories'][type]
            for board in boards: # main, ce
                categories = reference_json[game]['categories'][type][board]
                for category in categories: # any%, boss_rush, etc.
                    category_dict = reference_json[game]['categories'][type][board][category]
                    data = requests.get(f'{LEADERBOARD_URL}{game}/category/{category_dict["id"]}').json()
                    if category_dict['id'] == "jdz94eg2":
                        print(data)