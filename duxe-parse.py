from bs4 import BeautifulSoup
import requests
import re
from re import sub
from decimal import Decimal
import io
from datetime import datetime
import pandas as pd

url = 'https://www.duxe.ru/'
html_text = requests.get(url).text
soup = BeautifulSoup(html_text, 'lxml')

categ = soup.find('ul', class_='dropdown').find_all('a')[2:]

names = []
prices = []

for i in categ:
	link = i.get('href')
	full_link = url+link
	categ_top = requests.get(full_link).text
	soup_categ = BeautifulSoup(categ_top, 'lxml')
	inner_categ = soup_categ.find_all('div', class_='name')
	for j in inner_categ:
		print(j.text)
# 		low_categ = j.find('a', class_='dark_link')
# 		low_link = low_categ.get('href')
# 		res_link = url+low_link
# 		items_html = requests.get(res_link).text
# 		soup_items = BeautifulSoup(items_html, 'lxml')
# 		item_descr = soup_items.find_all('div', class_='item_info TYPE_1') # TODO all pages
# 		for k in item_descr:
# 			item_name = k.find('a', class_='dark_link').find('span').text
# 			item_price = k.find('span', class_='price_value')
# 			if item_price:
# 				item_price_exist = item_price.text
# 			else:
# 				item_price_exist = '---'
# 			names.append(item_name)
# 			prices.append(item_price_exist)

# d ={'name':names, 'price':prices}
# df = pd.DataFrame(d)
# df.to_excel('./duxe.xlsx', index=False)