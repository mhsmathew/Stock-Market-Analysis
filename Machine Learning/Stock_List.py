import bs4 as bs
import requests

class Access_Tickers:
    def __init__(self):
        self.tickers = []

    def save_sp500_tickers(self):
        resp = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
        soup = bs.BeautifulSoup(resp.text, 'lxml')
        table = soup.find('table', {'class': 'wikitable sortable'})
        tickers = []
        for row in table.findAll('tr')[1:]:
            ticker = row.findAll('td')[0].text
            tickers.append(ticker.strip())

        with open('S&P500.txt', 'w') as filehandle:
            filehandle.writelines("%s\n" % ticker for ticker in tickers)

    def save_top_etfs(self):
        resp = requests.get('https://etfdb.com/compare/volume/')
        soup = bs.BeautifulSoup(resp.text, 'lxml')
        tickers = []
        for n in soup.find_all(attrs={"data-th": "Symbol"}):
            tickers.append(n.find('a').contents[0])

        with open('TopETFs.txt', 'w') as filehandle:
            filehandle.writelines("%s\n" % ticker for ticker in tickers)

    def update_txt(self):
        self.save_top_etfs()
        self.save_sp500_tickers()

    def get_stocks(self):
        self.update_txt()
        self.tickers = []
        f = open("S&P500.txt", "r")
        for x in f:
            x=x.strip()
            if x.isalpha():
                self.tickers.append(x)
        return self.tickers
