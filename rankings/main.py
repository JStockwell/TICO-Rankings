# Moss Ranking (Spelunky)
# 100k points per category max
# (R)ating points: WR/PB * 100k
# (C)ompletion points: 5k for submitting
# (P)erformance points: 5k for being within 20% of the WR (WR/PB <= 1.2)
# Non main categories get divided by 10 (max 10k points)
# Out of all categories, the lowest scoring is ignored for each player

# Game Names: ico, sotc, sotc_2018, the_last_guardian, team_ico_games

import json
from users import get_user_csv

GAME_URL = 'https://speedrun.com/api/v1/games/'

reference_json = {}
with open('reference.json') as json_file:
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
    get_user_csv(reference_json)

if __name__ == "__main__":
    main()