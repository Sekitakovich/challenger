import csv
import logging

from loguru import logger

if __name__ == '__main__':
    '''
    csv.DictReaderはファイルの先頭行をcolumn毎の要素名として2行目以降をDictのリストとして返す
    そもそもCSV自体が嫌いで気に食わんがこれは助かる
    '''
    def main():
        with open(file='address.csv', mode='rt', encoding='cp932') as f:
            reader = csv.DictReader(f)
            for row in reader:
                logger.debug(row)
        pass

    main()