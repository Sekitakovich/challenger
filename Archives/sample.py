from typing import List, Dict
import pathlib
from natsort import natsorted
from loguru import logger


class Archiver(object):
    def __init__(self):
        self.path = pathlib.Path('files')
        self.dateFormat = f'%Y-%m-%d'

    def equipment(self) -> List[str]:
        result = []
        for f in self.path.iterdir():
            if f.is_dir():
                result.append(f.stem)
        return result

    def tree(self, *, path: pathlib.Path, file: List[str]):
        for f in path.iterdir():
            if f.is_dir():
                file = self.tree(path=f, file=file)
                pass
            else:
                file.append(f.stem)
                pass
        return file

    def toc(self, *, reverse: bool = False) -> Dict[str, any]:  # return List['YYYY-MM-DD']
        result = {}
        for sfi in self.equipment():
            result[sfi] = {}
            basepath = self.path / sfi
            flat = natsorted(self.tree(path=basepath, file=[]), reverse=reverse)

            ooo = {}
            for f in flat:
                YYYY = int(f[0:4])
                MM = int(f[4:6])
                DD = int(f[6:8])
                if YYYY not in ooo.keys():
                    ooo[YYYY] = {}
                if MM not in ooo[YYYY].keys():
                    ooo[YYYY][MM] = []
                ooo[YYYY][MM].append(DD)
            result[sfi] = ooo

        return result

    def load(self, *, equipment: str, ymd: str) -> List[str]:
        result = []

        try:
            YYYY = ymd[0:4]
            MM = ymd[4:6]
            name = f'{ymd}.txt'
            target = self.path / equipment / YYYY / MM / name

            with open(file=target, mode='rt') as f:
                body = f.read()
                for row in body.split('\n'):
                    if row:
                        result.append(row)
        except (FileNotFoundError, IndexError, KeyError) as e:
            logger.error(e)

        return result


if __name__ == '__main__':

    import json


    def main():
        A = Archiver()

        equipment = A.equipment()
        logger.info(equipment)

        toc = A.toc()
        logger.debug(toc)
        ooo = json.dumps(toc)
        logger.info(ooo)

        body = A.load(equipment='SD0001', ymd='20210621')
        for b in body:
            logger.info(b)

        logger.info('fin')


    main()
