from bs4 import BeautifulSoup
import pandas
import requests


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
        telephones_list = list(map(lambda x: x.get_text(), list(soup.h1.find_all('a'))))
        telephones = ",".join(telephones_list)
        email_or_site = list(map(lambda x: x.get_text(), soup.find_all(target="_blank")))
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


def main():
    """
    парсит файл эксель,
    парсит сайт по инн организаций из файла
    и добавляет в файл контактные данные организации
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
        result = Parser.parse_contacts(soup=new_soup)
        found_telephones.append(result['telephones'])
        found_emails.append(result['email'])
        found_sites.append(result['site'])
        counter += 1
        print(counter)
    organizations['telephone'] = found_telephones
    organizations['email'] = found_emails
    organizations['site'] = found_sites
    organizations.to_excel('organizations.xlsx')


if __name__ == "__main__":
    main()
# response = requests.get('https://www.find-org.com/cli/1376165_ooo_ic_sapr')



