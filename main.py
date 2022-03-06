from bs4 import BeautifulSoup
import pandas
import requests


class Parser:
    """
    предназначен для парсинга сайтов
    """
    pass

    @classmethod
    def parse_excheck_pro(cls, soup):
        """
        предназначен для вычленения контактных данных организации из html страницы
        :param soup: class 'bs4.BeautifulSoup'
        :return: словарь с контактами организации(тип- dict)
        """
        telephones_list = list(map(lambda x: x.get_text(),
                                   list(soup.h1.find_all('a'))))
        telephones = ",".join(telephones_list)
        email_or_site = list(map(lambda x: x.get_text(),
                                 soup.find_all(target="_blank")))
        if len(email_or_site) == 0:
            email = ''
            site = ''
        elif len(email_or_site) == 2:
            email, site = email_or_site
        elif len(email_or_site) == 1 and '@' in email_or_site[0]:
            email = email_or_site[0]
            site = ''
        else:
            email = ''
            site = email_or_site[0]

        contacts = {
            'telephones': telephones,
            'email': email,
            'site': site
        }
        return contacts

    @classmethod
    def parse_find_org_com(cls, soup):
        """
        предназначен для вычленения контактных данных организации из html страницы
        :param soup: class 'bs4.BeautifulSoup'
        :return: словарь с контактами организации(тип- dict)
        """
        try:
            element1 = soup.find(text='Телефон(ы): ').parent
            unuseful_text = element1.get_text()
            telephones = element1.parent.get_text()[len(unuseful_text):]
        except AttributeError:
            telephones = ''
        try:
            element2 = soup.find(text='Сайт: ').parent
            unuseful_text = element2.get_text()
            site = element2.parent.get_text()[len(unuseful_text):]
        except AttributeError:
            site = ''
        contacts = {
            'telephones': telephones,
            'site': site,
        }
        return contacts


def excheck_pro_handler():
    """
    парсит файл эксель,
    парсит сайт excheck.pro по инн организаций из файла
    и добавляет в файл контактные данные организации c сайта
    :return: none
    """
    organizations = pandas.read_excel('organizations.xlsx')
    found_telephones = []
    found_emails = []
    found_sites = []
    counter = 0
    for inn in list(organizations['ИНН']):
        response = requests.get(f'https://excheck.pro/company/{inn}/contacts')
        new_soup = BeautifulSoup(response.text, 'html.parser')
        result = Parser.parse_excheck_pro(soup=new_soup)
        found_telephones.append(result['telephones'])
        found_emails.append(result['email'])
        found_sites.append(result['site'])
        counter += 1
        print(counter)
    organizations['telephone'] = found_telephones
    organizations['email'] = found_emails
    organizations['site'] = found_sites
    organizations.to_excel('organizations.xlsx')


def find_org_com_handler():
    """
    парсит файл эксель,
    парсит сайт find-org.com по инн организаций из файла
    и добавляет в файл контактные данные организации c сайта
    :return: none
    """
    organizations = pandas.read_excel('organizations.xlsx')
    found_telephones = []
    found_sites = []
    counter = 0
    for inn in list(organizations['ИНН']):
        response = requests.get(f'https://www.find-org.com/search/inn/?val={inn}')
        soup = BeautifulSoup(response.text, 'html.parser')
        link = 'https://www.find-org.com/' + soup.p.a.get('href')
        new_response = requests.get(link)
        new_soup = BeautifulSoup(new_response.text, 'html.parser')
        result = Parser.parse_find_org_com(soup=new_soup)
        found_telephones.append(result['telephones'])
        found_sites.append(result['site'])
        counter += 1
        print(counter)
    organizations['telephone'] = found_telephones
    organizations['site'] = found_sites
    organizations.to_excel('organizations.xlsx')


if __name__ == "__main__":
    find_org_com_handler()






