import gspread
import pandas as pd
import duckdb


def to_csv(
    credential_json=None,
    spreadsheet_name=None,
    worksheet_name=None,
    sqlstr="",
    out_csv="",
):
    try:
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ]
        google_client = gspread.service_account(credential_json, scopes)
        spreadsheet = google_client.open(spreadsheet_name)
        worksheet = spreadsheet.worksheet(worksheet_name)
        worksheet_df = pd.DataFrame(worksheet.get_all_records())
        filtered_df = __filter(worksheet_df, worksheet_name, sqlstr)
        filtered_df.to_csv(out_csv, index=False)
    except gspread.SpreadsheetNotFound:
        print(f"Not found spreadsheet: {spreadsheet_name}")
    except gspread.WorksheetNotFound:
        print(f"Not found worksheet: {worksheet_name}")
    except Exception as e:
        print(e)


def __filter(df, worksheet_name, sqlstr):
    tablename = worksheet_name

    con = duckdb.connect()
    con.execute(f"CREATE TABLE {tablename} AS SELECT * from df")

    if sqlstr == "":
        sqlstr = f"SELECT * FROM {tablename}"

    return con.execute(sqlstr).df()
