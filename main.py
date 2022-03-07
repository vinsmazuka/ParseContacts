from bs4 import BeautifulSoup
import pandas
import requests
import time


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


def excel_handler(func_to_deco, path):
    """
    Читает данные из файла эксель,
    сохраняет результаты работы функций-обработчиков
    сайтов в файл эксель
    :param func_to_deco: функция-обработчик сайта
    :param path: путь к файлу, кот необходимо обработать(тип -str)
    :return: функцию-обертку write
    """
    def wrapper():
        def write():
            try:
                organizations.to_excel(path)
                print('Данные были записаны в файл')
            except PermissionError:
                print('Данные не были записаны, так как файл был открыт '
                      'закроте файл')
                time.sleep(5)
                return write()
        organizations = pandas.read_excel(path)
        result = func_to_deco(organizations)
        organizations['telephone'] = result['found_telephones']
        organizations['email'] = result['found_emails']
        organizations['site'] = result['found_sites']
        write()
    return wrapper


def excheck_pro_handler(organizations):
    """
    парсит сайт excheck.pro по инн организации
    :param organizations: объект класса pandas.DataFrame, содержащий
    информацию об организациях, в т.ч. их инн
    :return: словарь с контактными данными организаций(телефоны, email, сайт)
    """
    found_telephones = []
    found_emails = []
    found_sites = []
    counter = 0
    for inn in list(organizations['ИНН']):
        try:
            response = requests.get(f'https://excheck.pro/company/{inn}/contacts')
        except requests.exceptions.ConnectionError:
            print('Произошла ошибка соединения, ожидайте')
            time.sleep(10)
            response = requests.get(f'https://excheck.pro/company/{inn}/contacts')
            print('Соединение было восстановлено')
            new_soup = BeautifulSoup(response.text, 'html.parser')
            parsing_results = Parser.parse_excheck_pro(soup=new_soup)
            found_telephones.append(parsing_results['telephones'])
            found_emails.append(parsing_results['email'])
            found_sites.append(parsing_results['site'])
            counter += 1
            print(f'количество обработанных строк: {counter}')
        else:
            new_soup = BeautifulSoup(response.text, 'html.parser')
            parsing_results = Parser.parse_excheck_pro(soup=new_soup)
            found_telephones.append(parsing_results['telephones'])
            found_emails.append(parsing_results['email'])
            found_sites.append(parsing_results['site'])
            counter += 1
            print(f'количество обработанных строк: {counter}')
    result = {
        'found_telephones': found_telephones,
        'found_emails': found_emails,
        'found_sites': found_sites
    }
    return result


def find_org_com_handler(path):
    """
    парсит файл эксель,
    парсит сайт find-org.com по инн организаций из файла
    и добавляет в файл контактные данные организации c сайта
    :param path: путь к файлу, кот необходимо обработать(тип -str)
    :return: none
    """
    organizations = pandas.read_excel(path)
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
    organizations.to_excel(path)


def sbis_ru_handler(path):
    """
    парсит сайт find-org.com по инн организаций из файла
    и добавляет в файл контактные данные организации c сайта
    :param path: путь к файлу, кот необходимо обработать(тип -str)
    :return: none
    """


if __name__ == "__main__":
    excel_handler(excheck_pro_handler, 'organizations.xlsx')()
    # response = requests.get(f'https://sbis.ru/contragents/2724243851')
    # print(response.status_code)






