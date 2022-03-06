import requests
from bs4 import BeautifulSoup


response = requests.get('https://sbis.ru/contragents/2723034157')
soup = BeautifulSoup(response.text, 'html.parser')

try:
    telephone = soup.find(itemprop="telephone").get_text()
except AttributeError:
    pass
else:
    print(telephone)
try:
    email = soup.find(itemprop="email").get_text()
except AttributeError:
    pass
else:
    print(email)
try:
    site = soup.find(itemprop="url").get_text()
except AttributeError:
    pass
else:
    print(site)



