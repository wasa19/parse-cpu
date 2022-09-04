import csv
from bs4 import BeautifulSoup
import requests
# import pandas as pd
import json
# import csv
from datetime import datetime


def collect_darxtron():
    headers = {
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:101.0) Gecko/20100101 Firefox/101.0"
    }

    res_dict = {}
    res_dict_link = {}

    # req = requests.get(url='https://darxton.ru/', headers=headers).text

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

    categs_hrefs_list = categs_hrefs_list[:-4]

    count = 0

    for categ_href in categs_hrefs_list:
        # для пагинации определить количество страниц в категории
        # for pagination determine the number of pages in a category
        req = requests.get(categ_href, headers=headers).text
        soup = BeautifulSoup(req, 'lxml')
        pages_no = soup.find_all('a', class_='pagination__link')[-1].text
        for page in range(1, (int(pages_no)+1)):
            page_url = categ_href + f'?PAGEN_1={page}'
            req = requests.get(page_url, headers=headers).text
            soup = BeautifulSoup(req, 'lxml')
            item_cards = soup.find_all('div', class_="item item_hand")
            for card in item_cards:
                name = card.find('h3').text
                price = card.find('div', class_="item__price item__pq-price").text
                link = 'https://darxton.ru' + card.get('data-url')
                res_dict_link[name] = [price.strip().strip(' р. / шт'), link]
                res_dict[name] = price.strip().strip(' р. / шт')
        count += 1
        print(count)

    date_today = datetime.now().strftime('%d_%m_%y')

    with open(f'Datas/Data_darxtron/darxtron_{date_today}.json', 'w') as file:
        json.dump(res_dict, file, indent=4, ensure_ascii=False)

    with open(f'Datas/new/Data_darxtron/darxtron_{date_today}.json', 'w') as file:
        json.dump(res_dict_link, file, indent=4, ensure_ascii=False)
    # writer = csv.writer(file)
    # writer.writerow(res_dict)