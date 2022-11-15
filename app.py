from __future__ import print_function

import os.path
import time

import requests
from bs4 import BeautifulSoup
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Início do tratamento das credenciais
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
creds = None
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    with open('token.json', 'w') as token:
        token.write(creds.to_json())
# Fim do tratamento das credenciais

SHEET = '' #ID of your Google Sheet
TITLE_1 = '' #Title for product 1
PRODUCT_1 = '' #cell reference of your 1st product (ex: 'Page1!A1')

TITLE_2 = '' #Title for product 2
PRODUCT_2 = '' #cell reference of your 2nd product (ex: 'Page1!E1')

exec_time = 3600 #in seconds (1hour = 3600; 12hours = 43200; 1day = 86400)

def tracker_1():
    URL_1 = '' #Product Link from Amazon
    page_1 = requests.get(URL_1, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"})
    soup_1 = BeautifulSoup(page_1.content, 'html.parser')
    
    try:
        price_1 = soup_1.find(class_="a-price-whole").get_text(strip=True)
        price_1_converted = str(price_1[0:5])
    except:
        price_1_converted = "PRICE_ERROR"

    return price_1_converted

def tracker_2():
    URL_2 = '' #Product Link from Amazon
    page_2 = requests.get(URL_2, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"})
    soup_2 = BeautifulSoup(page_2.content, 'html.parser')
    
    try:
        price_2 = soup_2.find(class_="a-price-whole").get_text(strip=True)
        price_2_converted = str(price_2[0:5])
    except:
        price_2_converted = "PRICE_ERROR"

    return price_2_converted

try:
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()

    list_tracker_1 = [["Title", "Price", "Date/Hour"],]
    list_tracker_2 = [["Title", "Price", "Date/Hour"],]

    while(True):
        time.sleep(exec_time)
        list_tracker_1.append([TITLE_1, tracker_1(), time.ctime()])
        result = sheet.values().update(spreadsheetId=SHEET, range=PRODUCT_1, valueInputOption="RAW", 
                                    body={'values': list_tracker_1}).execute()
        list_tracker_2.append([TITLE_2, tracker_2(), time.ctime()])
        result = sheet.values().update(spreadsheetId=SHEET, range=PRODUCT_2, valueInputOption="RAW", 
                                    body={'values': list_tracker_2}).execute()


except HttpError as err:
    print(err)







