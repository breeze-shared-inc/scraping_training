import math
import time
import datetime
import pandas as pd
from bs4 import BeautifulSoup as bs
import requests


class Scraper:

    def __init__(self,count,type,all_flg):
        self.ARTICLE_PER_PAGE = 10
        self.URL = 'https://breezegroup.co.jp'
        self.JST = datetime.timezone(datetime.timedelta(hours=+9), 'JST')
        self.WAIT_TIME = 5
        self.all_flg = all_flg
        self.count = count
        self.type = type
        self._finish_count = 0
        self._max_count = 0
        self._complete = 0
        self.observer = []

    def addObserver(self,observer):
        self.observer.append(observer)

    def notice_finish_data(self):
        for observer in self.observer:
            observer.send_finish()

    def notice_max(self):
        for observer in self.observer:
            observer.send_max(self._max_count)

    def notice_complete(self):
        for observer in self.observer:
            observer.complete()

    @property
    def finish_data_count(self):
        return self._finish_count

    @finish_data_count.setter
    def finish_data_count(self,count):
        if self._finish_count != count:
            self._finish_count = count
            self.notice_finish_data()
            print(self.finish_data_count)

    @property
    def max_count(self):
        return self._max_count

    @max_count.setter
    def max_count(self,count):
        if self._max_count != count:
            self._max_count = count
            self.notice_max()

    @property
    def complete(self):
        return self._complete

    @complete.setter
    def complete(self,flg):
        if self._complete != flg:
            self._complete = flg
            self.notice_complete()


    # 取得対象のURLを取得
    def setURLList(self,count):
        url_list = []
        page_count = math.ceil(count / self.ARTICLE_PER_PAGE)
        last_page_count = count % self.ARTICLE_PER_PAGE
        for i in range(1,page_count + 1):
            url = []
            get_per_page = self.ARTICLE_PER_PAGE
            page_url = self.URL + '/page/' + str(i)
            res = requests.get(page_url)
            soup = bs(res.text,'html.parser')
            elems = soup.find_all('a',attrs={'class': 'post-thumbnail'})
            if i == page_count:
                get_per_page = last_page_count

            for (elem,j) in zip(elems,range(1, get_per_page + 1)):
                url.append(elem.attrs['href'])
            url_list += url
            time.sleep(self.WAIT_TIME)

        self.max_count = len(url_list)
        return url_list
    # 記事データを取得
    def getArticleData(self,url):
        article_data = []
        res = requests.get(url)
        soup = bs(res.text,'html.parser')
        now = datetime.datetime.now(self.JST)
        date = soup.find_all(name='div',class_='post-date')

        create_date = date[0].contents[1].contents[0]
        update_date = date[1].contents[1].contents[0]

        article_data.append(url)
        article_data.append(soup.find(name='h1',class_='entry-title').contents[0])
        article_data.append(soup.find(name='a',class_='author-url').attrs['href'])
        article_data.append(soup.find(name='span',class_='total_like').contents[0])
        article_data.append(create_date)
        article_data.append(update_date)
        article_data.append(now.strftime('%Y-%m-%d %H:%M:%S'))
        self.finish_data_count = self._finish_count + 1

        time.sleep(self.WAIT_TIME)

        return article_data

    # 対象分だけ繰り返し
    def getArticleIterator(self,count):
        article_list = []
        url_list = self.setURLList(count)

        for url in url_list:
            article_list.append(self.getArticleData(url))

        return article_list

    # 吐き出し用データ整形処理
    def makeDataFrame(self,article_list):
        return pd.DataFrame(
            article_list,
            columns=[
                '記事URL',
                'タイトル',
                '作者URL',
                'いいね数',
                '作成日',
                '更新日',
                '取得日時',
            ]
        ).set_index('記事URL')

    def maxArticle(self):
        max_count = 0
        max_base_count = 0
        res = requests.get(self.URL)
        soup = bs(res.text,'html.parser')
        max_base = soup.find('a',class_='page-numbers')
        page_url = max_base.attrs['href']
        page_count = int(max_base.contents[0])
        max_base_count = (page_count - 1) * 10
        time.sleep(self.WAIT_TIME)
        res = requests.get(page_url)
        soup = bs(res.text,'html.parser')
        elems = soup.find_all('a',attrs={'class': 'post-thumbnail'})
        max_count = max_base_count + len(elems)
        print(max_count)
        time.sleep(5)

        return max_count

    def export(self,article_data_frame,file_path = ''):
        if self.type == 'csv':
            path = self.csvMaker(article_data_frame,file_path)
        elif self.type == 'excel':
            path = self.excelMaker(article_data_frame,file_path)

        return path

    def csvMaker(self,article_data_frame,file_path = ''):
        path = file_path
        article_data_frame.to_csv(path + 'result.csv')
        return path


    def excelMaker(self,article_data_frame,file_path = ''):
        path = file_path
        article_data_frame.to_excel(path + 'result.xlsx')
        return path

    def facade(self,path = ''):

        print(self.all_flg)
        if self.all_flg:
            self.count = self.maxArticle()

        print(self.count)
        data = self.getArticleIterator(self.count)
        data = self.makeDataFrame(data)
        self.export(data,path)
        self.complete = 1

    @staticmethod
    def fromWebMaker(number,format,all,ws):
        from backend.observer import Observer as ob
        path = './backend/dist/static/'
        observer = ob(ws)
        scraper = Scraper(number,format,all)
        scraper.addObserver(observer)
        scraper.facade(path)

    @staticmethod
    def fromCliMaker(number,format,all=False):
        scraper = Scraper(number,format,all)
        scraper.facade()

if __name__ in '__main__':
    Scraper.fromCliMaker(5,'csv')