# Moss Ranking (Spelunky)
# 100k points per category max
# (R)ating points: WR/PB * 100k
# (C)ompletion points: 5k for submitting
# (P)erformance points: 5k for being within 20% of the WR (WR/PB >= 0.8)
# Non main categories get divided by 10 (max 10k points)

# Game Names: ico, sotc, sotc_2018, the_last_guardian, team_ico_games

import json
import pandas as pd

from rankings.users import get_user_csv
from rankings.ranking import calculate_user_ranks, calculate_user_rank
from rankings.excel import ranking_excel_generator

from utils.csv import save_csv_from_list

GAME_URL = 'https://speedrun.com/api/v1/games/'

USER_CSV_GEN_FLAG = False
RANKING_CSV_GEN_FLAG = False

reference_json = {}
with open('./files/reference.json') as json_file:
    reference_json = json.load(json_file)

# LOGIC FUNCTIONS
def stitch_ranking_dict():
    result_json = {}

    for i in range(17):
        with open(f'./files/backup/ranking_dict{(i+1)*10}.json', 'r') as file:
            ranking_dict_temp = json.load(file)
            result_json.update(ranking_dict_temp)

    with open('./files/ranking_dict.json', 'w') as file:
        json.dump(result_json, file)


# TEST FUNCTIONS
def test_print_categories(game, type, board, category):
    return reference_json[game]['categories'][type][board][category]


def test_excel_saving():
    test_ranking_dict = {'TikTak': {'user_id': 'qj25qv6j', 'scores': {'ico': 479633, 'sotc': 837748, 'sotc_2018': 1111454, 'tlg': 90202}}, 'Stockie': {'user_id': '5j51vgn8', 'scores': {
        'ico': 569820, 'sotc': 306760, 'sotc_2018': 759945, 'tlg': 0}}, 'SableDragonRook': {'user_id': '7j4nyrwx', 'scores': {'ico': 169560, 'sotc': 0, 'sotc_2018': 220313, 'tlg': 696214}}}

    ranking_excel_generator(test_ranking_dict)

def test_ranking_json(user_dict):
    with open('./files/temp.json') as json_file:
        ranking_dict = json.load(json_file)

    ranking_users = ranking_dict.keys()
    user_users = user_dict.keys()

    for user in ranking_users:
        if user not in user_users:
            print(f'{user} is not present')
        else:
            print(f'{user} is present')

    print(len(ranking_dict.keys()))

def test_ranking_dict_len(ranking_dict, user_dict):
    return len(ranking_dict.keys()) == len(user_dict.keys())

def test_ranking_dict_users(ranking_dict, user_dict):
    for ranking_user in ranking_dict.keys():
        if ranking_user not in user_dict.keys():
            return False
        
    return True

# MAIN FUNCTIONS


def main():
    # print(test_print_categories('sotc_2018','full_game','main','ng+'))
    if USER_CSV_GEN_FLAG:
        user_list = get_user_csv(reference_json)

    else:
        data = pd.read_csv("./files/users.csv")
        user_list = data['Username'].tolist()
        user_id_list = data['User ID'].tolist()

    user_dict = {}
    for i in range(len(user_list)):
        user_dict[user_list[i]] = user_id_list[i]

    if RANKING_CSV_GEN_FLAG:
        calculate_user_ranks(user_dict, 140, reference_json)

    with open('./files/ranking_dict.json') as json_file:
        ranking_dict = json.load(json_file)

    # TODO Automatic WR updater
    print("Ranking json is valid") if test_ranking_dict_len(ranking_dict, user_dict) and test_ranking_dict_users(ranking_dict, user_dict) else print("Ranking json not valid")
    ranking_excel_generator(ranking_dict)

if __name__ == "__main__":
    main()
