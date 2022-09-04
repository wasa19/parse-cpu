import requests
from time import sleep


headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:101.0) Gecko/20100101 Firefox/101.0"
}

url = "https://3d-diy.ru/catalog/cnc-components/"

req = requests.get(url=url, headers=headers).text

with open('index_3ddiy.html', 'w') as file:
    file.write(req)
sleep(7)



URL = 'https://cnc-tehnologi.ru/komplektuyushchie-k-chpu'
HEADERS = {
	'accept': '*/*',
	'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'
}
html_text = requests.get(URL, headers=HEADERS).text

with open('index_cnc_1.html', 'w') as file:
	file.write(html_text)



headers = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:101.0) Gecko/20100101 Firefox/101.0"
}

req = requests.get(url='https://darxton.ru/', headers=headers).text

with open("index_daxtron.html", "w") as file:
    file.write(req)


HEADERS = {
    'Accept': 'image/avif,image/webp,*/*',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0'
    }
URL = 'https://purelogic.ru/'

req = requests.get(URL, headers=HEADERS).text
with open('index_purelogic.html', 'w') as file:
    file.write(req)


headers = {
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:104.0) Gecko/20100101 Firefox/104.0"
    }
url = 'https://www.duxe.ru/catalog/'

req = requests.get(url, headers=headers).text
with open('index_duxe.html', 'w') as file:
    file.write(req)
