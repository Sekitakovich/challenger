from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import requests
import csv
import time
import zipfile

input_file = 'input.csv'
my_domain = 'https://boxil.jp/'
max_count = 10
current_time = datetime.now().strftime("%Y%m%d%H%M%S")
output_file1 = current_time + '_today_rank.xlsx'
output_file2 = current_time + '_my_rank.xlsx'
output_file3 = current_time + '.zip'


# 検索処理
def search_index(keyword):
    result = []
    try:
        search_url = 'https://www.google.co.jp/search?hl=ja&num=' + str(max_count) + '&q=' + keyword
        proxies = {
            'http': 'socks5://127.0.0.1:9050',
            'https': 'socks5://127.0.0.1:9050',
        }
        res_google = requests.get(search_url, proxies=proxies)
        bs4_google = BeautifulSoup(res_google.text, 'html.parser')
        articles = bs4_google.find_all("div", "ZINbbc xpd O9g5cc uUPGi")
        i = 0
        for article in articles:
            # タイトル
            title = article.find("div", "BNeawe vvjwJb AP7Wnd")
            if title is None:
                continue
            else:
                title = article.find("div", "BNeawe vvjwJb AP7Wnd").getText()
            # url
            url = (article.n.get("href").replace('/url?q=', '').split('&'))[0]
            if url is None:
                continue

            if title is not None and url is not None:
                i = i + 1
                work = []
                work.append(keyword)  # キーワード
                work.append(i)  # 順位
                work.append(title)  # タイトル
                work.append(url)
                result.append(work)
        return result
    except:
        pass


# ファイルのオープン
csvfile = open(input_file, 'r', encoding='utf-8')
reader = csv.reader(csvfile)
header = next(reader)
df = pd.DataFrame(columns=['keyword', 'rank', 'title', 'url'])
for row in reader:
    print(row)
    lists = search_index(row[0])
    for data in lists:
        series = pd.Series(data, index=df.columns)
        df = df.append(series, ignore_index=True)
    time.sleep(15)

from google.colab import files

print('キーワードのファイルを出力')
df.to_excel(output_file1)
df2 = df[df['url'].str.contains(my_domain)].sort_values(by="rank", ascending=True)
print('ドメインファイルを出力')
df2.to_excel(output_file2)
print('圧縮中')
with zipfile.ZipFile(output_file3, 'w', compression=zipfile.ZIP_DEFLATED) as new_zip:
    new_zip.write(output_file1, arcname=output_file1)
    new_zip.write(output_file2, arcname=output_file2)
print('処理終了')
