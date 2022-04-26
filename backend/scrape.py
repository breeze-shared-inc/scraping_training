import math
import time
import datetime
import sys
import pandas as pd
from bs4 import BeautifulSoup as bs
import requests


class Scraper:
    """
    記事をスクレイピングして、CSVまたはExcelに吐き出すクラス

    Attributes
    ----------
    ARTICLE_PER_PAGE : int
        1ページ単位の記事数
    URL              : str
        スクレイピング対象のURL
    JST              : timezone
        日本時間
    WAIT_TIME        : int
        待ち時間
    all_flg          : bool
        全件取得フラグ
    count            : int
        取得記事数
    format             : str
        拡張子(csv or excel)
    """

    def __init__(self, count: int, format: str, all_flg: bool) -> None:
        """
        Parameters
        ----------
        count   : int
            記事取得数
        format  : str
            拡張子(csv or excel)
        all_flg : bool
            全件取得フラグ
        """
        self.ARTICLE_PER_PAGE = 10
        self.URL = 'https://breezegroup.co.jp'
        self.JST = datetime.timezone(datetime.timedelta(hours=+9), 'JST')
        self.WAIT_TIME = 5
        self.all_flg: bool = all_flg
        self.count: int = count
        self.format: str = format

    def setURLList(self,count: int) -> list:
        """
        取得対象のURLリストを取得

        Parameters
        ----------
        count : int
            取得する記事数

        Returns
        -------
        url_list : list
            指定した記事数分のURLリスト
        """
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

    def getArticleData(self,url: str) -> list[str, str, str, int, str, str, str]:
        """
        記事の詳細データを取得

        Parameters
        ----------
        url : str
            取得して欲しい記事詳細URL

        Returns
        -------
        article_data : list
            取得したデータのリスト。URL、タイトル、いいね数、記事作成日、記事更新日、取得日時
        """
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

        time.sleep(self.WAIT_TIME)

        return article_data

    def getArticleIterator(self,count: int) -> list[list[str, str, str, int, str, str, str]]:
        """
        指定した記事数分スクレピングを実施する

        Parameters
        ----------
        count : int
            取得したい記事の数

        Returns
        -------
        article_list : list
            取得した記事情報

        """
        article_list = []
        url_list = self.setURLList(count)

        for url in url_list:
            article_list.append(self.getArticleData(url))

        return article_list

    def makeDataFrame(self,article_list: list) -> pd.DataFrame:
        """
        list -> 吐き出し用データ(csv,excel)整形処理

        Parameters
        ----------
        article_list : list
            取得済みの記事リスト

        Returns
        -------
        pd : DataFrame
            データフレーム形式に変換されたデータ

        """
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

    def maxArticle(self) -> int:
        """
        最大件数の取得

        Returns
        -------
        max_count : int
            サイト内に存在する記事の数
        """
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
        time.sleep(5)

        return max_count

    def export(self, article_data_frame: pd.DataFrame, file_path = '') -> None:
        """
        exportの総合受付

        Parameters
        ----------
        article_data_frame: Dataframe
            データフレーム整形後の記事データ

        file_path: str
            保存先のパス
        """
        if self.format == 'csv':
            article_data_frame.to_csv(file_path + 'result.csv')

        elif self.format == 'excel':
            article_data_frame.to_excel(file_path + 'result.xlsx')


    @staticmethod
    def fromCliMaker(count: int, format='excel', all_flg=False) -> None:
        """
        記事取得から吐き出しまで一気に実行する関数。
        利用者は基本的にこのメソッドのみ知っていれば問題なし。

        Parameter
        ---------
        count  : int
            取得したい記事の数
        format : str
            吐き出す拡張子。csvまたはExcel。初期値はExcel
        all_flg: bool
            全件取得するかどうかのフラグ。
            Trueにした場合は、引数countは無視され、
            記事全件取得される
        """
        scraper = Scraper(count,format,all_flg)
        print(scraper.all_flg)
        if scraper.all_flg:
            scraper.count = scraper.maxArticle()

        print(scraper.count)
        data = scraper.getArticleIterator(scraper.count)
        data = scraper.makeDataFrame(data)
        scraper.export(data)

if __name__ in '__main__':
    args = ['',1,'excel',False]
    for (arg,i) in zip(sys.argv,range(len(args))):
        args[i] = arg
    Scraper.fromCliMaker(int(args[1]),args[2],args[3])