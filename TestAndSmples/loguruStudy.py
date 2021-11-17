import pathlib
from loguru import logger

'''
前々から気になっていたこと、それはどこかのメソッド内でtry-exceptで特定の例外を捕捉した時、
それはメソッドを呼び出した側にも伝わるのか? 今回試してみたところ、答えは「否」と判明。
つまりメソッド内で捕捉されなかった例外のみが呼び出し側で捕捉された。
これは全体テストの時に有効だ。
'''


class Sample(object):
    def __init__(self, *, file: str = ''):
        self.isReady = False
        try:
            self.f = open(file=file, mode='rt')
            if self.f:
                raise TimeoutError('KKK')
        except FileNotFoundError as e:  # 捕捉の対象はFNFだけ
            logger.error(e)  # この場合は.error(ファイル名と行番号が出るので)
        else:
            self.isReady = True
            logger.info(file)


if __name__ == '__main__':

    # @logger.catch  # どうやらこれは不要な模様
    def paopao():
        raise ValueError('NG')

    try:
        # paopao()
        sample = Sample(file='loguruStudy.py2')
    except Exception as e:  # 捕捉されなかった全ての例外がこれで拾える
        logger.exception(e)  # ここではどこで例外が発生したのかを知るために.exceptionでスタックフレーム表示
        # logger.error(e)
