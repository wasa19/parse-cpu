import requests
import lxml
from bs4 import BeautifulSoup
import json
import csv
import pandas as pd
from datetime import datetime


CATEGS = {}
res_dict = {}

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:101.0) Gecko/20100101 Firefox/101.0"
}

url = "https://3d-diy.ru/catalog/cnc-components/"

req = requests.get(url=url, headers=headers).text

# пишем в файл, чтоб не тыркать сайт
# with open('index.html', 'w') as file:
#     file.write(req)

with open('index.html', 'r') as file:
    src = file.read()

soup = BeautifulSoup(src, 'lxml')
categs_hrefs = soup.find(class_='list items').find_all(class_='name')

for i in categs_hrefs:
    categ_name = i.text
    categ_href = 'https://3d-diy.ru' + i.find('a').get('href')
    CATEGS[categ_name] = categ_href

count = 0
for k, v in CATEGS.items():
    if count == 0:
        res_dict[k] = ''
        for i in range(1, 8):
            url = v + f'?PAGEN_1={i}'
            req = requests.get(url=url, headers=headers).text
            soup = BeautifulSoup(req, 'lxml')
            item_infos = soup.find_all(class_='item_info TYPE_1')
            for item_info in item_infos:
                item_name = item_info.find(class_='item-title').text
                try:
                    item_price = item_info.find('span', class_='price_value').text
                except(Exception) as e:
                    item_price = 'No Price'
                    print(e)
                if item_name not in res_dict:
                    res_dict[item_name] = item_price
        count += 1
        print(count)

names = []
prices = []
for k,v in res_dict.items():
    names.append(k)
    prices.append(v)

res_d = {'name':names, 'price':prices}
date_today = dt = datetime.now().strftime('%d_%m_%y')
df = pd.DataFrame(res_d)
df.to_excel(f'3ddiy_{date_today}.xlsx' ,index=False)

# mid_categs = []
# for categ_top_name in CATEGS[0:2]:
#     req = requests.get(url=categ_top_name, headers=headers).text
#     soup = BeautifulSoup(req, 'lxml')
#     try:
#         categ_mid_names = soup.find(class_='list items').find_all(class_='name')
#         for i in categ_mid_names:
#             mid_categ_href = 'https://3d-diy.ru' + i.find('a').get('href')
#             mid_categs.append(mid_categ_href)
#     except(Exception) as e:
#         print('No Mid Categ for  ' + categ_top_name)
#         print(e)


# print(mid_categs)