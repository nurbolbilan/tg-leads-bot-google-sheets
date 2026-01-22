import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

SHEET_NAME = "Leads from Telegram"  # название твоей таблицы 1-в-1

def save_to_sheets(name, phone, comment):
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]

    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)

    sheet = client.open(SHEET_NAME).sheet1
    sheet.append_row([name, phone, comment, datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
