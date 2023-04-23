import requests
import bs4

class ExchangeRateCrawler:
    def __init__(self, url):
        self.url = url

    def get_html(self):
        '''獲取html'''
        response = requests.get(self.url)
        response.encoding = "utf-8"
        self.soup = bs4.BeautifulSoup(response.text, "lxml")

    def get_bank_rate_table(self):
        '''獲取銀行匯率表格'''
        self.bank_rate_list = self.soup.find('div',class_ = 'cubre-o-table').find_all('div', class_ = 'cubre-o-table__item')

    def get_left_top_cell(self, index):
        '''獲取左上角的單元格'''
        title = self.bank_rate_list[index].find('div', class_ = 'cubre-a-rateName__ch').text.replace(" ", "")
        return title

    def get_header_row(self, index):
        '''獲取表頭'''
        headers = self.bank_rate_list[index].find('thead').find_all('th')
        return [header.text.replace('\n', '') for header in headers]

    def get_exchange_rates(self, index):
        '''獲取匯率'''
        rows = self.bank_rate_list[index].find('tbody').find_all('tr')
        exchange_rates = [[cell.text.replace('\n', '') for cell in row.find_all('td')] for row in rows]
        return exchange_rates

    def print_exchange_rates(self):
        '''印出匯率'''
        for index in range(len(self.bank_rate_list)):
            print(self.get_left_top_cell(index), end=" ")
            headers = self.get_header_row(index)
            for header in headers:
                print(header, end=" ")
            print()
            exchange_rates = self.get_exchange_rates(index)
            for exchange_rate in exchange_rates:
                print(' '.join(exchange_rate))

    def run(self):
        '''執行爬蟲'''
        self.get_html()
        self.get_bank_rate_table()
        self.print_exchange_rates()



def main():
    scraper = ExchangeRateCrawler('https://www.cathaybk.com.tw/cathaybk/personal/product/deposit/rate/#twrate')
    scraper.run()

if __name__ == '__main__':
    main()