from email import header
from itertools import count
import re
from bs4 import BeautifulSoup
import requests
import json
from datetime import datetime


def collect_duxe():

    headers = {
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:104.0) Gecko/20100101 Firefox/104.0"
    }

    res_dict = {}
    res_dict_link = {}

    with open('index_duxe.html', 'r') as file:
        src = file.read()

    soup = BeautifulSoup(src, 'lxml')
    categs_hrefs = soup.find_all('li', class_='name')
    
    categs_hrefs_list = []
    categs_hrefs_list_1 = []
    categs_hrefs_list_2 = []
    categs_hrefs_list_3 = []
    categs_hrefs_list_4 = []
    res_dict_link = {}
    res_dict = {}
    count = 0

    for categ in categs_hrefs:
        categ_href = 'https://www.duxe.ru' + categ.find('a', class_='dark_link').get('href')
        categs_hrefs_list.append(categ_href)

    # Собираем все вложенные категории
    for categ_url in categs_hrefs_list:
        count += 1
        print(count)
        req_1 = requests.get(categ_url, headers=headers).text
        soup = BeautifulSoup(req_1, 'lxml')
        if soup.find_all('div', class_='name'):
            categ_hrefs_1 = soup.find_all('div', class_='name')
            for categ_1 in categ_hrefs_1:
                categ_href_1 = 'https://www.duxe.ru' + categ_1.find('a', class_='dark_link').get('href')
                if categ_href_1 not in categs_hrefs_list_1:
                    categs_hrefs_list_1.append(categ_href_1)
    categs_hrefs_list += categs_hrefs_list_1

    for categ_url in categs_hrefs_list_1:
        count += 1
        print(count)
        req_2 = requests.get(categ_url, headers=headers).text
        soup = BeautifulSoup(req_2, 'lxml')
        if soup.find_all('div', class_='name'):
            categ_hrefs_2 = soup.find_all('div', class_='name')
            for categ in categ_hrefs_2:
                categ_href = 'https://www.duxe.ru' + categ.find('a', class_='dark_link').get('href')
                if categ_href not in categs_hrefs_list_2:
                    categs_hrefs_list_2.append(categ_href)
    categs_hrefs_list += categs_hrefs_list_2

    for categ_url in categs_hrefs_list_2:
        count += 1
        print(count)
        req_3 = requests.get(categ_url, headers=headers).text
        soup = BeautifulSoup(req_3, 'lxml')
        if soup.find_all('div', class_='name'):
            categ_hrefs_3 = soup.find_all('div', class_='name')
            for categ in categ_hrefs_3:
                categ_href = 'https://www.duxe.ru' + categ.find('a', class_='dark_link').get('href')
                if categ_href not in categs_hrefs_list_3:
                    categs_hrefs_list_3.append(categ_href)
    categs_hrefs_list += categs_hrefs_list_3

    categs_hrefs_set = set(categs_hrefs_list)
    categs_hrefs_list = list(categs_hrefs_set)

    for categ_url in categs_hrefs_list:
        req_pg = requests.get(categ_url, headers=headers).text
        soup = BeautifulSoup(req_pg, 'lxml')
        if soup.find('div', class_='nums'):
            pages_num = int(soup.find('div', class_='nums').find_all('a', class_='dark_link')[-1].text)
            for page in range(2, pages_num+1):
                page_url = categ_url + '?PAGEN_1=' + str(page)
                if page_url not in categs_hrefs_list_4:
                    categs_hrefs_list_4.append(page_url)
    categs_hrefs_list += categs_hrefs_list_4

    categs_hrefs_list.sort()

    for link in categs_hrefs_list:
        req = requests.get(link, headers=headers).text
        soup = BeautifulSoup(req, 'lxml')
        if soup.find_all('div', class_='item_info TYPE_1'):
            cards = soup.find_all('div', class_='item_info TYPE_1')
            for card in cards:
                try:
                    name = card.find('div', class_='item-title').find('span').text
                    link_g = 'https://www.duxe.ru' + card.find('div', class_='item-title').find('a').get('href')
                    price = card.find('span', class_='price_value').text.replace(' ', '')
                except Exception as e:
                    print(e)
                    price = 'NoPrice'
                res_dict_link[name] = [price.strip(), link_g]
                res_dict[name] = price.strip()

    date_today = datetime.now().strftime('%d_%m_%y')

    with open(f'Datas/Data_duxe/duxe_{date_today}.json', 'w') as file:
        json.dump(res_dict, file, indent=4, ensure_ascii=False)

    with open(f'Datas/new/Data_duxe/duxe_{date_today}.json', 'w') as file:
        json.dump(res_dict_link, file, indent=4, ensure_ascii=False)
