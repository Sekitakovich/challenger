import pathlib
from loguru import logger
from natsort import natsorted
from pprint import pprint


class Sample(object):
    def __init__(self):
        self.basePath = pathlib.Path('../useResponder')
        # for f in self.basePath.iterdir():
        #     logger.info(f'parent=[{f.parent}] name=[{f.name}]')

    def take(self, *, path: pathlib.Path) -> dict:
        logger.debug(f'path = [{path}]')
        result = {}
        file = []
        for f in path.iterdir():
            name = f.name
            if f.is_dir():
                if 'next' not in result.keys():
                    result['next'] = {}
                result['next'][name] = self.take(path=f)
                pass
            else:
                file.append(f.name)
                pass
        result['this'] = natsorted(file)
        return result

    def tree(self):
        result = self.take(path=self.basePath)
        return result

if __name__ == '__main__':
    def main():
        S = Sample()
        tree = S.tree()
        # logger.info(tree)
        pprint(tree)


    main()
