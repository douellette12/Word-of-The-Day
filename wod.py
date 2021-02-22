import requests
from bs4 import BeautifulSoup
import json
import smtplib
from smtplib import SMTPException
import datetime
import mariadb
import sys


def get_wod():
    url = "https://www.merriam-webster.com/word-of-the-day"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    wod = soup.find_all('div', class_="word-and-pronunciation")
    wod = wod[0].find('h1').text
    wod = str(wod)
    return wod


def get_wod_info(wod):
    url = f"https://www.dictionaryapi.com/api/v3/references/collegiate/json/{wod}?key=secret"
    r = requests.get(url)
    r = json.loads(r.text)
    short_def = str(r[0]['shortdef'][0])
    pronunciation = str(r[0]['hwi']['prs'][0]['mw'])
    word_type = str(r[0]['fl'])
    return short_def, pronunciation, word_type


def send_email(wod, word_type, pronunciation, short_def):
    gmail_user = 'email@gmail.com'
    gmail_password = 'secret'
    receiver = ['email@gmail.com', 'email@protonmail.com']
    message = f"""From: Python Script <email@gmail.com>
To: NAME <email@gmail.com>, NAME <email@protonmail.com>
IME-Version: 1.0
Content-type: text/html; charset="UTF8"
Subject: Merriam Webster's Word of the Day 
<html>
<head>
    <meta http-equiv="Content-Type"  content="text/html charset=UTF-8" />
</head>
<body>
<div style="padding-bottom: 50px; padding-top: 50px; background: #375c71;">
    <div style="font-size: 50px; color: white; text-align:center;">
        <p style="font-size: 20px;">
            Word of the day : {datetime.date.today().strftime("%B %d, %Y")}
        </p>
        <hr style="width: 50%; margin: 0 auto;">
        <p style="font-size: 55px; color: white; font-family: Georgia, serif;">{wod}</p>
        <p style="font-size: 20px;"><i>{word_type}</i> | {pronunciation}</p>
        <hr>
        <p style="font-size: 20px;">{short_def}</p>
    </div>  
</div>  
</body>
</html>"""
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(gmail_user, receiver, message.encode('utf8'))
        server.close()
        print('Email sent!')
    except SMTPException:
        print('Something went wrong...')

    return None
    
 
 def db_conn():
    try:
        conn = mariadb.connect(
            user="pi",
            password="secret",
            host="localhost",
            port=3306,
            database="dbname"

        )
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)

    # Get Cursor
    cursor = conn.cursor()
    return conn, cursor


def insert_row(conn, cursor, day, word, word_type, pronunciation, definition):
    cursor.execute(
        """INSERT INTO word_of_the_day.wod_tbl (Day, Word, WordType, Pronunciation, Definition) VALUES 
        (?, ?, ?, ?, ?)""", (day, word, word_type, pronunciation, definition))
    conn.commit()

