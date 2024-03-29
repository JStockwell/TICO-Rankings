from utils.api_call import api_call

CATEGORIES_URL = 'https://www.speedrun.com/api/v1/categories/'
RUNS_URL = 'https://www.speedrun.com/api/v1/runs?'
game_list = ["ico", "sotc", "sotc_2018", "the_last_guardian"]

def get_game_score(scores, game):
    score = 0
    score = scores[game_list.index(game)]
    return score

def save_game_score(score, scores, game):
    scores[game_list.index(game)] = score
    return scores

def calcualte_user_rank_FG(reference_json, user, scores, game):
    score = get_game_score(scores, game)
    for board in reference_json[game]['categories']['full_game']:
        categories = reference_json[game]['categories']["full_game"][board]
        for category in categories: # any%, boss_rush, etc.
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
                    score += r_score+c_score+p_score

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
                                fastest_time = int(data[i]['times']['primary_t'])
                        run_time = int(data[fastest_i]['times']['primary_t'])
                        record_time = int(record['times']['primary_t'])
                        
                        r_score = int(record_time/run_time * 100000)
                        c_score = 5000
                        p_score = 5000 if record_time/run_time >= 0.8 else 0

                        # TODO Save individual scores per category/variable/level
                        score += r_score+c_score+p_score

    scores = save_game_score(score, scores, game)
    return scores

def calculate_user_rank_IL(reference_json, user, scores, game):
    print("IL")

    return scores

def calculate_user_rank(user, reference_json):
    # Score List: [ico_score, sotc_score, sotc_2018_score, tlg_score]
    scores = [0, 0, 0, 0]

    for game in reference_json: # ico, sotc, sotc_2018, tlg
        types = reference_json[game]["categories"]
        
        for type in types: #full_game and il
            if type == "il":
                scores = calculate_user_rank_IL(reference_json, user, scores, game)
            else:
                scores = calcualte_user_rank_FG(reference_json, user, scores, game)

    print(scores)