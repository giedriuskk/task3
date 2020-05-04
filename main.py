from clutch_scrapper import MainScraper
from scraper_config import urls
from Task3.Class.american import American
from Task3.Class.company import Company
from Task3.Class.other import Other
from read_write import write_to_json
from threading import Thread
import threading
import time

count = 0
page_no = 0
american_list = []
other_list = []


class MainRun:

    def __init__(self):
        self.companies = []
        self.number = 3

    def multi1(self, url):

        self.number = MainScraper().get_amount_of_companies(url)

    def multi2(self, url, lock):

        lock.acquire()
        self.companies = MainScraper().scrape_data(self.number, url)
        lock.release()

    def run_multi(self):

        threads = []

        for url in urls:
            lock = threading.Lock()
            t = Thread(target=self.multi2, args=(url, lock))
            t.start()
            threads.append(t)
            t1 = Thread(target=self.multi1, args=(url,))
            t1.start()
            threads.append(t1)

            for thread in threads:
                thread.join()

            for item in self.companies:
                item.print_company_info()
                if Company.is_american(Company, item.country):
                    american_list.append(item)
                else:
                    if Other.is_not_banned(Other, item.country):
                        other_list.append(item)

            write_to_json(self.companies, 'test.json')

    def run(self):

        global companiess
        for url in urls:
            number = MainScraper().get_amount_of_companies(url)
            companiess = MainScraper().scrape_data(self.number, url)

            for item in companiess:
                item.print_company_info()
                if Company.is_american(Company, item.country):
                    american_list.append(item)
                else:
                    if Other.is_not_banned(Other, item.country):
                        other_list.append(item)

        write_to_json(companiess, 'test.json')


if __name__ == '__main__':

    def single():
        st = time.perf_counter()
        MainRun().run()
        fn = time.perf_counter()
        print(f'Single-thread clutch_scraper finished in {round(fn - st, 2)} seconds')


    def multi():
        st = time.perf_counter()
        MainRun().run_multi()
        fn = time.perf_counter()
        print(f'Multi-thread clutch_scraper finished in {round(fn - st, 2)} seconds')


    threads = []

    t = Thread(target=single)
    t.start()
    threads.append(t)

    t1 = Thread(target=multi)
    t1.start()
    threads.append(t1)

    for thread in threads:
        thread.join()

    try:
        Other.avg_rank(Other, other_list)
        American.avg_rank(American, american_list)
    except:
        pass
