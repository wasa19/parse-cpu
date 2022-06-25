from asyncore import read
import re
from bs4 import BeautifulSoup
import requests
import pandas as pd
import json
import csv
from datetime import datetime

headers = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:101.0) Gecko/20100101 Firefox/101.0"
}

req = requests.get(url='https://darxton.ru/', headers=headers).text


# with open("index_daxtron.html", "w") as file:
#     file.write(req)

with open('index_daxtron.html', 'r') as file:
    src = file.read()

soup = BeautifulSoup(src, 'lxml')
categs_hrefs = soup.find_all('div', class_='header__catalog-menu-item')

categs_hrefs_list = []

for categ in categs_hrefs:
    categs_href = 'https://darxton.ru' + categ.find('a').get('href')
    categs_hrefs_list.append(categs_href)

for 