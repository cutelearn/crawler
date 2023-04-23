import requests
import bs4

class ReleaseMovieCrawler:
    def __init__(self, url):
        self.url = url

    def get_html(self):
        '''獲取html'''
        response = requests.get(self.url)
        response.encoding = "utf-8"
        self.soup = bs4.BeautifulSoup(response.text, "lxml")

    def get_movie_list(self):
        '''獲取電影列表'''
        self.movie_list = self.soup.find('ul', class_ = 'release_list')

    def get_movie_title(self, index):
        '''獲取電影名稱'''
        info_list = self.movie_list.find_all('li')
        title = info_list[index].find('div', class_ = 'release_movie_name').find('a').text.replace(" ", "")
        return title

    def get_movie_release(self, index):
        '''獲取電影上映日期'''
        info_list = self.movie_list.find_all('li')
        release_time = info_list[index].find('div', class_ = 'release_movie_time').text.replace(" ", "")
        return release_time

    def loop_movie_info(self):
        '''印出電影資訊'''
        for index in range(len(self.movie_list.find_all('li'))):
            print(self.get_movie_title(index), end="")
            print(self.get_movie_release(index), end="")

    def run(self):
        '''執行爬蟲'''
        self.get_html()
        self.get_movie_list()
        self.loop_movie_info()


def main():
    scraper = ReleaseMovieCrawler('https://movies.yahoo.com.tw/movie_comingsoon.html')
    scraper.run()


if __name__ == '__main__':
    main()