import requests
from typing import Dict, List
from bs4 import BeautifulSoup


class Ranker(object):

    def __init__(self):

        self.urlBase: str = 'https://www.google.co.jp/search'
        self.proxies: Dict[str, str] = {
            'http': 'socks5://127.0.0.1:9050',
            'https': 'socks5://127.0.0.1:9050',
        }

    def get(self, *, kw: str, count: int = 10, tor: bool = False) -> str:

        result: str = ''
        if kw:
            option: Dict[str, any] = {
                'hl': 'ja',
                'num': count,
                'q': kw,
            }

            url = self.urlBase + '?' + '&'.join(['%s=%s' % (k, v) for k, v in option.items()])

            content = requests.get(url=url, proxies=self.proxies if tor else {})
            result = content.text

            bs = BeautifulSoup(result, 'html.parser')
            articles = bs.find_all("div", "ZINbbc xpd O9g5cc uUPGi")
            for index, item in enumerate(articles, 1):
                title = item.find("div", "BNeawe vvjwJb AP7Wnd")
                print('index[%d] = [%s]' % (index, title))

        return result


if __name__ == '__main__':
    ranker = Ranker()
    text = ranker.get(kw='阿弖流為')
    print(text)
