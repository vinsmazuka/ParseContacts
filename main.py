import requests
from bs4 import BeautifulSoup


class Parser:
    """
    предназначен для парсинга сайтов
    """
    pass

    @classmethod
    def parse_contacts(cls, soup):
        """
        предназначен для вычленения контактных данных организации из html страницы
        :param soup: class 'bs4.BeautifulSoup'
        :return: словарь с контактами организации
        """
        telephones = list(map(lambda x: x.get_text(), list(soup.h1.find_all('a'))))
        contacts = {
            'telephones': telephones
        }
        return contacts


response = requests.get('https://excheck.pro/company/4401116480/contacts')
new_soup = BeautifulSoup(response.text, 'html.parser')

result = Parser.parse_contacts(soup=new_soup)
print(result)






# try:
#     email = soup.find(itemprop="email").get_text()
# except AttributeError:
#     pass
# else:
#     print(email)
# try:
#     site = soup.find(itemprop="url").get_text()
# except AttributeError:
#     pass
# else:
#     print(site)



