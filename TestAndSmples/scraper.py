import requests
from typing import Dict
from bs4 import BeautifulSoup


class Scraper(object):

    def __init__(self):

        self.proxies: Dict[str, str] = {
            'http': 'socks5://127.0.0.1:9050',
            'https': 'socks5://127.0.0.1:9050',
        }

        self.error: str = ''

    def get(self, *, url: str, tor: bool = False) -> str:

        result: str = ''
        self.error = ''

        try:
            content: requests.Response = requests.get(url=url, proxies=self.proxies if tor else {})
        except Exception as e:
            self.error = e
        else:
            result = content.text

        return result


class Analyzer(object):

    def __init__(self):
        pass

    def get(self, *, src: str):
        bs = BeautifulSoup(src, 'html.parser')
        print(bs.prettify())
        span = [tag.text for tag in bs.find_all(class_='entry-content')]
        print(span)


if __name__ == '__main__':

    s = Scraper()
    a = Analyzer()

    target: str = 'https://www.google.com/search?biw=1218&bih=718&sxsrf=ALeKk01hk1lnVzFNgnZpRAUIgjgy2Y9PbA%3A1585104000760&ei=gMR6Xr__LdPm-AaKq5WACQ&q=%E9%96%A2%E5%8B%9D%E6%88%90&oq=%E9%96%A2%E5%8B%9D%E6%88%90&gs_l=psy-ab.3..0i8i7i30.60103.68918..69772...2.0..2.106.2332.28j1......0....1..gws-wiz.....10..35i39j0j0i7i30j0i5i30j35i362i39j35i39i19j0i131j0i4j0i131i4j0i4i37.B3fvKBPJ8vM&ved=0ahUKEwi_v5bHzLToAhVTM94KHYpVBZA4ChDh1QMICw&uact=5'
    text = s.get(url=target, tor=True)

    if s.error:
        print(s.error)
    else:
        a.get(src=text)
