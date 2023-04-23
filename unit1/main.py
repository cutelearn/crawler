import requests
import bs4

class ExchangeRateCrawler:
    def __init__(self, url):
        self.url = url

    def __get_html(self):
        '''獲取html'''
        response = requests.get(self.url)
        response.encoding = "utf-8"
        self.soup = bs4.BeautifulSoup(response.text, "lxml")

    def __get_left_top_cell(self):
        '''獲取左上角的單元格'''
        table = self.soup.find_all('table')
        lefttop = table[4].find('tr').find('tr').find('td')
        return lefttop.text

    def __get_header_row(self):
        '''獲取表頭'''
        table = self.soup.find_all('table')
        headers = table[4].find('tr').find_all('a', 'bodytablehead')
        return [header.text for header in headers]

    def __get_exchange_rates(self):
        '''獲取匯率'''
        table = self.soup.find_all('table')
        rows = table[4].find_all('tr', 'bodytabletr1')
        exchange_rates = []
        for row in rows:
            exchange_rate = []
            for td in row.find_all('td'):
                exchange_rate.append(td.text.strip())
            exchange_rates.append(exchange_rate)
        return exchange_rates

    def __print_exchange_rates(self):
        '''印出匯率'''
        print(self.__get_left_top_cell(), end="　")
        headers = self.__get_header_row()
        for header in headers:
            print(header, end=" ")
        print()
        exchange_rates = self.__get_exchange_rates()
        for exchange_rate in exchange_rates:
            print(' '.join(exchange_rate))

    def run(self):
        '''執行爬蟲'''
        self.__get_html()
        self.__print_exchange_rates()


def main():
    scraper = ExchangeRateCrawler('http://www.taiwanrate.com')
    scraper.run()


if __name__ == "__main__":
    main()