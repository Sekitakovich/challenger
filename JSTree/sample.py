import json
import pathlib
from loguru import logger
from natsort import natsorted
import os
from dataclasses import dataclass, asdict
from pprint import pprint

@dataclass()
class Fileinfo(object):
    name: str
    fullpath: str

class Directory(object):

    @classmethod
    def take(self, *, path: pathlib.Path) -> dict:
        result = {}
        file = []
        for f in path.iterdir():
            logger.debug(f'parent=[{f.parent}] name=[{f.name}]')
            name = f.name
            parent = f.parent
            fullpath = f'{parent}{os.sep}{name}'
            if f.is_dir():
                if 'next' not in result.keys():
                    result['next'] = {}
                result['next'][name] = self.take(path=f)
                pass
            else:
                file.append(asdict(Fileinfo(name=name, fullpath=fullpath)))
                pass
        # result['this'] = natsorted(file)
        result['this'] = file
        return result


class Sample(object):
    def __init__(self):
        self.basePath = pathlib.Path('../')

    def tree(self):
        result = Directory.take(path=self.basePath)
        return result


if __name__ == '__main__':
    def main():
        S = Sample()
        tree = S.tree()
        # logger.info(tree)
        pprint(tree)
        ooo = json.dumps(tree)
        pprint(ooo)


    main()
