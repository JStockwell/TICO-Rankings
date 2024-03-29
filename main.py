# Moss Ranking (Spelunky)
# 100k points per category max
# (R)ating points: WR/PB * 100k
# (C)ompletion points: 5k for submitting
# (P)erformance points: 5k for being within 20% of the WR (WR/PB <= 1.2)
# Non main categories get divided by 10 (max 10k points)
# Out of all categories, the lowest scoring is ignored for each player

# Game Names: ico, sotc, sotc_2018, the_last_guardian, team_ico_games

import json
import pandas as pd
from rankings.users import get_user_csv
from rankings.ranking import calculate_user_rank

from utils.csv import save_csv_from_list

GAME_URL = 'https://speedrun.com/api/v1/games/'
CSV_GEN_FLAG = False

reference_json = {}
with open('./files/reference.json') as json_file:
        reference_json = json.load(json_file)

# Category Structure:
# Game: ico, sotc, sotc_2018, tlg
# Type: full_game, il
# Board: main, ce
# Category: any%, boss_rush, etc.

# UTILITY FUNCTIONS


# LOGIC FUNCTIONS


# TEST FUNCTIONS
def test_print_categories(game, type, board, category):
    return reference_json[game]['categories'][type][board][category]

# MAIN FUNCTIONS
def main():
    #print(test_print_categories('sotc_2018','full_game','main','ng+'))
    if CSV_GEN_FLAG:
        user_list = get_user_csv(reference_json)

    else:
        data = pd.read_csv("./files/users.csv")
        user_list = data['Username'].tolist()
        user_id_list = data['User ID'].tolist()

    user_dict = {}
    for i in range(len(user_list)):
        user_dict[user_list[i]] = user_id_list[i]

    calculate_user_rank(user_dict["SableDragonRook"], reference_json)

if __name__ == "__main__":
    main()