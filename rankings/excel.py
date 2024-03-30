import os
import win32com.client as win32
import pandas as pd


def format_worksheet(wb, user_len, sheet_name):
    ws = wb.Worksheets(sheet_name)
    ws.Select
    ws.Range('A:C').Sort(Key1=ws.Range('C1'), Order1=2, Orientation=1)
    for i in range(user_len):
        ws.Range(f'A{i+2}').Value = i + 1
        if ws.Range(f'C{i+2}').Value == 0:
            ws.Range(f'A{i+2}:C{user_len+2}').EntireRow.Delete()
            break


def ranking_excel_generator(ranking_dict):
    excel = win32.Dispatch("Excel.Application")
    excel.Application.Quit()

    raw_csv_dict = {
        "user_id": [],
        "username": [],
        "ico": [],
        "sotc": [],
        "sotc_2018": [],
        "tlg": []
    }

    ico_csv_dict = {
        "Rank": [],
        "Player": [],
        "Score": []
    }

    sotc_csv_dict = {
        "Rank": [],
        "Player": [],
        "Score": []
    }

    sotc_2018_csv_dict = {
        "Rank": [],
        "Player": [],
        "Score": []
    }

    tlg_csv_dict = {
        "Rank": [],
        "Player": [],
        "Score": []
    }

    for user in ranking_dict.keys():
        # Generate Raw Dict
        raw_csv_dict["username"].append(user)
        raw_csv_dict["user_id"].append(
            ranking_dict[user]["user_id"])
        raw_csv_dict["ico"].append(
            ranking_dict[user]["scores"]["ico"])
        raw_csv_dict["sotc"].append(
            ranking_dict[user]["scores"]["sotc"])
        raw_csv_dict["sotc_2018"].append(
            ranking_dict[user]["scores"]["sotc_2018"])
        raw_csv_dict["tlg"].append(
            ranking_dict[user]["scores"]["tlg"])

        # Generate ICO Dict
        ico_csv_dict["Rank"].append(0)
        ico_csv_dict["Player"].append(user)
        ico_csv_dict["Score"].append(
            ranking_dict[user]["scores"]["ico"])

        # Generate SotC Dict
        sotc_csv_dict["Rank"].append(0)
        sotc_csv_dict["Player"].append(user)
        sotc_csv_dict["Score"].append(
            ranking_dict[user]["scores"]["sotc"])

        # Generate SotC 2018 Dict
        sotc_2018_csv_dict["Rank"].append(0)
        sotc_2018_csv_dict["Player"].append(user)
        sotc_2018_csv_dict["Score"].append(
            ranking_dict[user]["scores"]["sotc_2018"])

        # Generate TLG Dict
        tlg_csv_dict["Rank"].append(0)
        tlg_csv_dict["Player"].append(user)
        tlg_csv_dict["Score"].append(
            ranking_dict[user]["scores"]["tlg"])

    excel_path = './files/test_rankings.xlsx'

    df_raw = pd.DataFrame(raw_csv_dict)
    df_ico = pd.DataFrame(ico_csv_dict)
    df_sotc = pd.DataFrame(sotc_csv_dict)
    df_sotc_2018 = pd.DataFrame(sotc_2018_csv_dict)
    df_tlg = pd.DataFrame(tlg_csv_dict)

    with pd.ExcelWriter(excel_path) as excel_writer:
        df_ico.to_excel(excel_writer, sheet_name='ICO', index=False)
        df_sotc.to_excel(
            excel_writer, sheet_name='Shadow of the Colossus (2005)', index=False)
        df_sotc_2018.to_excel(
            excel_writer, sheet_name='Shadow of the Colossus (2018)', index=False)
        df_tlg.to_excel(
            excel_writer, sheet_name='The Last Guardian', index=False)
        df_raw.to_excel(excel_writer, sheet_name='Raw Data', index=False)

    # Clean up and order excel sheets
    wb = excel.Workbooks.Open(os.path.abspath(excel_path))

    format_worksheet(wb, len(ranking_dict.keys()), 'ICO')
    format_worksheet(wb, len(ranking_dict.keys()),
                     'Shadow of the Colossus (2005)')
    format_worksheet(wb, len(ranking_dict.keys()),
                     'Shadow of the Colossus (2018)')
    format_worksheet(wb, len(ranking_dict.keys()), 'The Last Guardian')

    wb.Save()
    excel.Application.Quit()
