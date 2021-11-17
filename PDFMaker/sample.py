import pdfkit
import pathlib
from loguru import logger


class PDFMaker(object):
    def __init__(self, *, outputPath: str = './'):
        wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
        self.config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf)
        self.options = {
            'orientation': 'Portrait',  # notice
            'page-size': 'A4',
            'margin-top': '1.0in',
            'margin-right': '0.1in',
            'margin-left': '0.1in',
            'margin-bottom': '1.0in',
            'encoding': 'UTF-8',
            'no-outline': None,
            'header-right': '[date] [time]',
            'footer-center': ' [page]/[topage]',  # '1/3' 2020-10-09
            'enable-local-file-access': None,  # orz ...
        }
        self.outputPath = pathlib.Path(outputPath)
        self.isReady = True
        if self.outputPath.exists() is False or self.outputPath.is_dir() is False:
            self.isReady = False
            logger.error('no outputPath %s' % (self.outputPath))

    def create(self, *, url: str, name: str = 'pdf.pdf') -> bool:
        success = True
        if self.isReady:
            dst = self.outputPath / name
            try:
                pdfkit.from_url(url, str(dst), configuration=self.config, options=self.options)
            except (IOError) as e:
                success = False
                logger.error(e)
            else:
                logger.success('%s was created' % (≤dst))
        else:
            success = False
        return success


if __name__ == '__main__':
    def main():
        P = PDFMaker(outputPath='work')
        P.create(url='https://as-web.jp', name='sample.pdf')
        pass


    main()
