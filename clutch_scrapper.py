import requests
from bs4 import BeautifulSoup
import bs4 as bs
from tld import get_tld
from scraper_config import filters, alexa
import re
from time import sleep
from Task3.Class.company import Company


class Alexa:

    def get_root_url(url):

        try:
            res = get_tld(url, as_object=True)
        except:
            return ''
        return res.fld

    def from_string_to_int(string):

        if string != '':
            int_number = str(string).replace(",", "").replace(" ", "")
            return int(int_number)

    def get_stat(url):

        sleep(3)
        getting_rank = alexa + url
        print(getting_rank)
        try:
            r = requests.get(getting_rank)
            soup = BeautifulSoup(r.text, "html.parser")

            rank_get = soup.find('p', attrs={'class': 'big data'})  # page rank
            rank_dirty = rank_get.text.strip()
            clean_rank = rank_dirty[1:].strip()
        except Exception as ex:
            print("Error occurred: {}".format(str(ex)))
            return ''

        return clean_rank


class MainScraper:

    def __init__(self):
        self.filters = filters
        self.count = 0

    def get_amount_of_companies(self, url):

        try:
            page_url = str(url) + "?" + self.filters
            response = requests.get(page_url)
        except Exception as ex:
            print("Error occurred: {}".format(str(ex)))
            return 0

        t = bs.BeautifulSoup(response.content, 'lxml')
        total = t.find('div', {"class": "tabs-info"})
        total_firms = (total.text.strip()).split(' ')
        print(f'{total_firms[0]} in this list')
        number = int(total_firms[0].replace(',', '').strip())
        return number

    def scrape_company_lists(self, url, page_no):

        if page_no == 0:
            page_url = str(url) + "?" + self.filters
            print(f'Scraping data from : {page_url}, page number: {page_no}')
        else:
            page = "?page="
            page_url = str(url) + page + str(page_no) + "&" + self.filters

            print(f'Scraping data from : {page_url}, page number: {page_no}')

        try:
            response = requests.get(page_url)
        except Exception as ex:
            print('\n Current URL: ', url, ', page: ', page_no)
            print("Error occurred: {}".format(str(ex)))
            return ""
        return response

    def scrape_data(self, number, url):

        page_no = 0
        companies_1 = []

        while True and self.count < number:

            soup = bs.BeautifulSoup((MainScraper().scrape_company_lists(url, page_no)).content, 'lxml')

            directory_ul = soup.find("ul", {"class": "directory-list"})
            companies = directory_ul.find_all("li", {"class": "provider-row"})
            for i in range(5):
                link = companies[i].find('a', href=re.compile("^https://clutch.co/profile"))
                try:
                    comp_url = link.get('href')
                except:
                    pass
                name = companies[i].find("h3", {"class": "company-name"})
                info_list = companies[i].find_all('div', {"class": "list-item"})
                try:
                    location = info_list[3]
                    region = location.find('span', {"class": "region"})
                except:
                    pass
                website = companies[i].find('li', {"class": "website-link"})

                self.count += 1
                website_root = Alexa.get_root_url(website.a['href'].strip())
                rank = Alexa.get_stat(website_root)

                if rank != '':
                    print(f'Company number: {self.count}, {name.text.strip()}, {website_root}, website rank: {rank}')

                    companies_1.append(Company(name.text.replace('\n', '').strip(), comp_url.strip(), region.text.replace('\n', '').strip(), website_root, Alexa.from_string_to_int(rank)))
            page_no += 1

        return companies_1
