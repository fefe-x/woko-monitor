from bs4 import BeautifulSoup
import requests
#import json
import os
import dotenv
import re
import time

# take environment variables from .env.
dotenv.load_dotenv()

# take webhook_url from .env file
webhook_url = os.getenv('WEBHOOK')

monitor_url = "https://woko.ch/en/zimmer-in-zuerich"

def send_embed(duration, url, price, date, address):
    webhook_data = {
        "embeds": [
            {
                "title": "New WOKO room found!",
                "color": 55144,
                "fields": [
                    {
                        "name": "URL",
                        "value": url
                    },
                    {
                        "name": "Duration",
                        "value": duration,
                    },
                    {
                        "name": "Price",
                        "value": price
                    },
                    {
                        "name": "Address",
                        "value": address,
                    },
                    {
                        "name": "Date",
                        "value": date
                    }
                ]
            }
        ],
        "username": "woko-monitor",
        "avatar_url": "https://www.woko.ch/images/favicons/apple-touch-icon-114x114.png"
    }
    
    embed = requests.post(webhook_url, json=webhook_data)
    if embed.status_code == 204:
        print("successfully sent webhook")
    else:
        print(embed.content)

# send get request to monitor_url
html_text = requests.get(monitor_url).text


# filter html for room ads
soup = BeautifulSoup(html_text, 'html.parser')



found = []

# extract values from inserate and send to discord webhook
def monitor():
    print("Monitoring...")
    inserate = soup.find_all("div", {"class": "inserat"})
    for inserat in inserate:
        link = inserat.find("a")
        url = "https://www.woko.ch"+link["href"]
        duration = inserat.find(string=re.compile("as from"))
        date = inserat.find("span").string
        price = inserat.find("div", "preis").string + " CHF"
        address = inserat.find(string=re.compile("Zürich"))
        if url not in found:
            if duration == "as from 01.07.2022													" or duration == "as from 01.08.2022													" or duration == "as from 01.09.2022													":
                print("found new room")
                found.append(url)
                send_embed(duration, url, price, date, address)


while True:
    monitor()
    time.sleep(1800.0)