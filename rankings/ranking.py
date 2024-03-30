from utils.api_call import api_call
from datetime import datetime
import time
import json

CATEGORIES_URL = 'https://www.speedrun.com/api/v1/categories/'
RUNS_URL = 'https://www.speedrun.com/api/v1/runs?'
LEVELS_URL = 'https://www.speedrun.com/api/v1/levels/'
game_list = ["ico", "sotc", "sotc_2018", "the_last_guardian"]


def get_game_score(scores, game):
    score = 0
    score = scores[game_list.index(game)]
    return score


def save_game_score(score, scores, game):
    scores[game_list.index(game)] = score
    return scores

def calculate_user_rank_FG(reference_json, user, scores, game):
    score = get_game_score(scores, game)
    for board in reference_json[game]['categories']['full_game']:
        categories = reference_json[game]['categories']["full_game"][board]
        for category in categories:  # any%, boss_rush, etc.
            category_dict = reference_json[game]['categories']["full_game"][board][category]
            if category_dict['variations'] == None:
                data = api_call(f'{RUNS_URL}category={category_dict["id"]}&user={user}')
                if len(data) > 0:
                    record = api_call(f'{CATEGORIES_URL}{category_dict["id"]}/records?top=1')[0]['runs'][0]['run']
                    fastest_i = 0
                    fastest_time = 99999999999999
                    for i in range(len(data)):
                        if int(data[i]['times']['primary_t']) < fastest_time:
                            fastest_i = i
                            fastest_time = int(data[i]['times']['primary_t'])
                    run_time = int(data[fastest_i]['times']['primary_t'])
                    record_time = int(record['times']['primary_t'])

                    r_score = int(record_time/run_time * 100000)
                    c_score = 5000
                    p_score = 5000 if record_time/run_time >= 0.8 else 0

                    # TODO Save individual scores per category/variable/level
                    score += r_score + c_score + p_score

            else:
                for variation in category_dict['variations']:
                    url_values = ''
                    subcategory = category_dict['variations'][variation]
                    for var in subcategory["vars"]:
                        url_values += f'var-{var}={subcategory["vars"][var]}&'
                    data = api_call(f'{RUNS_URL}category={category_dict["id"]}&user={user}&{url_values}')
                    if len(data) > 0:
                        record = api_call(f'{CATEGORIES_URL}{category_dict["id"]}/records?top=1')[0]['runs'][0]['run']
                        fastest_i = 0
                        fastest_time = 99999999999999
                        for i in range(len(data)):
                            if int(data[i]['times']['primary_t']) < fastest_time:
                                fastest_i = i
                                fastest_time = int(
                                    data[i]['times']['primary_t'])
                        run_time = int(data[fastest_i]['times']['primary_t'])
                        record_time = int(record['times']['primary_t'])

                        r_score = int(record_time/run_time * 100000)
                        c_score = 5000
                        p_score = 5000 if record_time/run_time >= 0.8 else 0

                        # TODO Save individual scores per category/variable/level
                        score += r_score + c_score + p_score

    scores = save_game_score(score, scores, game)
    return scores


def calculate_user_rank_IL(reference_json, user, scores, game):
    score = get_game_score(scores, game)
    boards = ["main", "ce"]
    for board in boards:
        categories = reference_json[game]['categories']["il"][board]
        for category in categories:  # any%, boss_rush, etc.
            category_dict = reference_json[game]['categories']["il"][board][category]
            for level in reference_json[game]['categories']["il"]["levels"]:
                level_id = reference_json[game]['categories']["il"]["levels"][level]["id"]
                if category_dict['variations'] == None:
                    data = api_call(f'{RUNS_URL}category={category_dict["id"]}&level={level_id}&user={user}')
                    if len(data) > 0:
                        all_category_records = api_call(
                            f'{LEVELS_URL}{level_id}/records?top=1')
                        for category_record in all_category_records:
                            if category_record['category'] == category_dict["id"]:
                                record = category_record['runs'][0]['run']
                        fastest_i = 0
                        fastest_time = 99999999999999
                        for i in range(len(data)):
                            if int(data[i]['times']['primary_t']) < fastest_time:
                                fastest_i = i
                                fastest_time = int(
                                    data[i]['times']['primary_t'])
                        run_time = int(data[fastest_i]['times']['primary_t'])
                        record_time = int(record['times']['primary_t'])

                        r_score = int(record_time/run_time * 100000)
                        c_score = 5000
                        p_score = 5000 if record_time/run_time >= 0.8 else 0

                        # TODO Save individual scores per category/variable/level
                        score += r_score + c_score + p_score

    scores = save_game_score(score, scores, game)
    return scores


def calculate_user_rank(user, reference_json):
    # Score List: [ico_score, sotc_score, sotc_2018_score, tlg_score]
    scores = [0, 0, 0, 0]

    for game in reference_json:  # ico, sotc, sotc_2018, tlg
        types = reference_json[game]["categories"]

        for type in types:  # full_game and il
            if type == "il":
                scores = calculate_user_rank_IL(
                    reference_json, user, scores, game)
            else:
                scores = calculate_user_rank_FG(
                    reference_json, user, scores, game)

    return scores


def calculate_user_ranks(user_dict, reference_json):
    ranking_dict = {}
    total_time = 0.0
    user_counter = 0

    for user in user_dict.keys():
        start_time = datetime.now()
        user_scores = calculate_user_rank(user_dict[user], reference_json)

        ranking_dict[user] = {
            "user_id": user_dict[user],
            "scores": {
                "ico": user_scores[0],
                "sotc": user_scores[1],
                "sotc_2018": user_scores[2],
                "tlg": user_scores[3],
            }
        }

        timedelta = datetime.now() - start_time
        total_time += timedelta.total_seconds()
        user_counter += 1
        time_left = total_time / user_counter * (len(user_dict.keys())-user_counter)
        print(f'{user} Done in {timedelta.total_seconds()}. Approximate time left: {time.strftime("%H:%M:%S", time.gmtime(time_left))}')

        if user_counter % 10 == 0 and user_counter != 0:
            with open(f'./files/ranking_dict{user_counter}.json', 'w') as file:
                json.dump(ranking_dict, file)

    return ranking_dict
