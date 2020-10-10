import pathlib
from typing import List
import zipfile
from loguru import logger


class FileTree(object):
    def __init__(self, *, top: str = './'):

        self.top = pathlib.Path(top)
        self.useFolder = ['GPS', 'AV', 'MJ']
        self.useSuffix = ['.py', '.js', '.html']

    def zipCreate(self, *, src: List[pathlib.Path]) -> bool:
        success: bool = False
        dst = 'a.zip'
        try:
            with zipfile.ZipFile(dst, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
                for target in src:
                    logger.debug('+++ %s' % target)
                    zf.write(target)
        except zipfile.error as e:
            logger.error(e)
        else:
            success = True

        return success

    def listUp(self) -> List[pathlib.Path]:
        src: List[pathlib.Path] = []

        for f in list(self.top.glob('**/*')):
            doit = False
            if len(f.parts) > 1:
                if f.parts[0] in self.useFolder:
                    doit = True
            else:
                doit = True

            if doit:
                if f.is_dir():
                    src.append(f)
                elif f.is_file():
                    if f.suffix.lower() in self.useSuffix:
                        src.append(f)

            else:
                logger.warning('Exclude %s' % f)

        return src


if __name__ == '__main__':
    F = FileTree()

    s = F.listUp()
    F.zipCreate(src=s)
