from bs4 import BeautifulSoup
import requests
import re
import pandas as pd

URL = 'https://cnc-tehnologi.ru/komplektuyushchie-k-chpu'
HEADERS = {
	'accept': '*/*',
	'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'
}

names = []
prices = []

html_text = requests.get(URL, headers=HEADERS).text

# with open('index_cnc_1.html', 'w') as file:
# 	file.write(html_text)

with open('index_cnc_1.html') as file:
	html_text = file.read()

soup = BeautifulSoup(html_text, 'lxml')

categ_links = soup.find_all(class_='moduletable portlet shop_catalog2 expandable_menu expanded')[1].find_all('a')[1:]
for categ_link in categ_links:
	url = 'https://cnc-tehnologi.ru'+categ_link.get('href')
	html_text_categ = requests.get(url, headers=HEADERS).text
	soup_categ = BeautifulSoup(html_text_categ, 'lxml')
	categ_name = soup_categ.find('div', class_="jshop frame")

	if categ_name:

		good_names_table = categ_name.find_all('tr', class_=['row0', 'row1'])
		good_names_list = categ_name.find_all('div', class_=re.compile('product productitem_'))

		if good_names_table:
			for good_name_table in good_names_table:
				good_name = good_name_table.find('td', class_='name').find('a').text
				if good_name_table.find('td', class_='price'):
					good_price = good_name_table.find('td', class_='price').find('span', class_='value').text
				else:
					good_price = ' - '
				if good_name and good_price:
					names.append(good_name.strip())
					prices.append(good_price)
				# print(good_name.strip(), '  -  ', good_price.strip())

		elif good_names_list:
			for good_name_list in good_names_list:
				good_name = good_name_list.find('div', class_='name').find('a').text
				good_price = good_name_list.find('div', class_='jshop_price').find('span').text
				if good_name and good_price:
					names.append(good_name)
					prices.append(good_price)
				# print(good_name.strip(), '  -  ', good_price.strip())


res_d ={'name':names, 'price':prices}
df = pd.DataFrame(res_d)
df.to_excel('./cnc.xlsx', index=False)
