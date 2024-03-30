import pandas as pd


def save_csv_from_list(list, headers, path_to_csv):
    csv_dict = {}
    i = 0

    for header in headers:
        csv_dict[header] = list[i]
        i += 1

    df = pd.DataFrame(csv_dict)
    df.to_csv(path_to_csv)
