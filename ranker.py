import requests
from typing import Dict, List
from bs4 import BeautifulSoup
from dataclasses import dataclass
from datetime import datetime as dt


@dataclass()
class Entry(object):
    title: str
    url: str


@dataclass()
class Result(object):
    status: int
    kw: str
    at: dt
    entry: List[Entry]


class Ranker(object):

    def __init__(self):

        self.urlBase: str = 'https://www.google.co.jp/search'
        self.proxies: Dict[str, str] = {
            'http': 'socks5://127.0.0.1:9050',
            'https': 'socks5://127.0.0.1:9050',
        }

    def checkTor(self):

        res = requests.get('https://ipinfo.io', proxies=self.proxies).json()
        print(res)

    def get(self, *, kw: str, count: int = 10, tor: bool = False) -> Result:

        result: Result = Result(kw='', at=dt.now(), entry=[], status=0)
        if kw:
            result.kw = kw
            option: Dict[str, any] = {
                'hl': 'ja',
                'num': count,
                'q': kw,
            }

            url = self.urlBase + '?' + '&'.join(['%s=%s' % (k, v) for k, v in option.items()])

            content = requests.get(url=url, proxies=self.proxies if tor else {})
            text = content.text
            result.status = content.status_code

            bs = BeautifulSoup(text, 'html.parser')
            entry = bs.find_all("div", "ZINbbc xpd O9g5cc uUPGi")
            for item in entry:
                title = item.find("div", "BNeawe vvjwJb AP7Wnd")
                if title:
                    url = (item.a.get("href").replace('/url?q=', '').split('&'))[0]
                    result.entry.append(Entry(title=title.string, url=url))

        return result


if __name__ == '__main__':
    french: List[str] = ['Debussy', 'Ravel', 'Poulenc', 'Honegger', 'Satie', 'Chabrier', 'Delibes',
                         'Faure', 'Pierne', 'Offenbach']
    other: List[str] = ['shostakovich', ]

    collector = Ranker()
    collector.checkTor()

    for name in french:
        try:
            ranking = collector.get(kw=name, tor=True)
        except KeyboardInterrupt as e:
            break
        else:
            print(ranking)
