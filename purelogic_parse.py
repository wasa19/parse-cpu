import re
from bs4 import BeautifulSoup
import json
import requests
from datetime import datetime
from time import sleep


HEADERS = {
    'Accept': 'image/avif,image/webp,*/*',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0'
    }

count = 0
res_dict = {}
URL = 'https://purelogic.ru/'

# req = requests.get(URL, headers=HEADERS).text
# with open('index_purelogic.html', 'w') as file:
#     file.write(req)

with open('index_purelogic.html', 'r') as file:
    src = file.read()

soup = BeautifulSoup(src, 'lxml')
categ_hrefs = soup.find_all('a', class_='sidebar-nav__link')

categ_links = []
for categ_href in categ_hrefs:
    categ_link = URL + categ_href.get('href')
    categ_links.append(categ_link)

for categ_link in categ_links[:-2]:
    req = requests.get(categ_link, headers=HEADERS).text
    soup = BeautifulSoup(req, 'lxml')
    pages_no = soup.find_all('a', class_='pagination-list__link')[-1].text

    for page in range(1, (int(pages_no)+1)):
        page_url = categ_link + f'?PAGEN_1={page}'
        req = requests.get(page_url, headers=HEADERS).text
        soup = BeautifulSoup(req, 'lxml')
        item_cards = soup.find_all('div', class_="catalog-list__item")
        for card in item_cards:
            name = card.find('div', class_='product-name').text
            if card.find('div', class_="price__discount"):
                price = card.find('div', class_="price__discount").text
            else:
                price = '-'
            link = 'https://purelogic.ru' + card.find('a', class_='catalog-item__link').get('href')
            # res_dict[name] = [price.strip().strip(' руб.с НДС'), link]
            res_dict[name] = price.strip().strip(' руб.с НДС')
    count += 1
    print(count)

date_today = datetime.now().strftime('%d_%m_%y')

with open(f'Datas/Data_purelogic/purelogic_{date_today}.json', 'w') as file:
    json.dump(res_dict, file, indent=4, ensure_ascii=False)
