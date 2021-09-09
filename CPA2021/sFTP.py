'''
$ sftp -i .\LightsailDefaultKey-ap-northeast-1.pem -p 22 ubuntu@jmf.magneticsquare.biz
'''

import paramiko
import fnmatch
import pathlib
import socket
from dataclasses import dataclass
from common import Constants

import logging
import logzero
from logzero import logger

formatS = '%(color)s[%(levelname)1.1s %(asctime)s %(module)s:%(lineno)d:%(funcName)s]%(end_color)s %(message)s'
formatF = '%(name)s - %(asctime)-15s - %(levelname)s:: %(message)s'

logzero.loglevel(level=logging.DEBUG)
formatter = logzero.LogFormatter(fmt=formatS, datefmt='%H:%M:%S')
logzero.setup_default_logger(formatter=formatter)

logzero.logfile(filename='./LOGs/cpa.log', loglevel=logging.INFO, backupCount=60)


@dataclass()
class Server(object):
    host: str  # サーバホスト名
    port: int  # ポート番号
    user: str  # SSHアカウント
    code: str  # お客様コード
    selfClean: bool  # Trueなら取得後にファイルを消去
    remoteBase: str  # サーバ側のルートフォルダ
    localBase: str  # こちら側のルートフォルダ
    prefix: str  # こちらで予め指定するファイル接頭文字列


class SFTPSession(object):  # use only key authentication, no need password
    def __init__(self, *, hostname: str, port: int = 22, username: str, keyFile: str, remotePath: str = './',
                 localPath: str = './', pattern: str = '*.*', overwrite: bool = True, cleanUp: bool = True,
                 sessionName: str = 'unknown'):
        self.isReady = False
        self.timeoutSecs = 5

        self.sessionName = sessionName
        self.hostname = hostname
        self.port = port
        self.username = username
        self.account = f'{username}@{hostname}'
        self.basePath = pathlib.Path(remotePath)  # service's root directory
        self.localPath = pathlib.Path(localPath)
        self.pattern = pattern
        self.overwrite = overwrite
        self.cleanUp = cleanUp
        self.newCommer = []

        logger.info(f'--------------------------------')
        logger.info(f'start {Constants.sysName} version {Constants.sysVersion}')
        logger.info(f'--------------------------------')

        try:
            self.pkey = paramiko.RSAKey.from_private_key_file(filename=keyFile)
        except (FileNotFoundError, paramiko.BadHostKeyException, paramiko.SSHException, UnicodeDecodeError) as e:
            logger.error(e)
        else:
            self.isReady = True
            logger.debug(f'+++ SFTP instance [{self.sessionName}] was made as bellows')
            logger.debug(f'+++ sftp -i {keyFile} -p {self.port} {self.account}')
            logger.debug(f'+++ remotePath = [{self.basePath}] localPath = [{self.localPath}]')

    def cbEntry(self, sA: int, sW: int):
        if sA != sW:
            logger.warning(f'Accepted/Written not match [{sA}/{sW}] ???')

    def retrieve(self) -> bool:
        success = False
        if self.isReady:
            try:
                logger.debug(f'+++ start SSH session')
                with paramiko.SSHClient() as ssh:
                    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    ssh.connect(hostname=self.hostname, port=self.port, username=self.username, pkey=self.pkey,
                                timeout=self.timeoutSecs)
                    logger.debug(f'({self.sessionName}) connected')
                    with ssh.open_sftp() as sftp:
                        self.newCommer = []
                        sftp.chdir(path=str(self.basePath))
                        # cwd = sftp.getcwd()
                        # logger.debug(f'remote cwd = {cwd}')
                        dir = sftp.listdir()
                        for src in dir:
                            if fnmatch.fnmatch(src, self.pattern):
                                target = (self.localPath / src)
                                if target.exists() is False or self.overwrite is True:
                                    dst = str(target)
                                    sftp.get(remotepath=src, localpath=dst, callback=self.cbEntry)
                                    self.newCommer.append(src)
                                    logger.debug(f'({self.sessionName}) +++ GET [{self.basePath / src}] to [{dst}]')
                                    if self.cleanUp:
                                        sftp.remove(path=src)
                                        logger.debug(f'({self.sessionName}) --- {src} was removed')
                                else:
                                    logger.warning(f'({self.sessionName}) === {target} is already exists')
                            else:
                                logger.warning(f'({self.sessionName}) ignore [{src}]')
            except (socket.gaierror, socket.timeout,
                    PermissionError, FileNotFoundError, paramiko.AuthenticationException,
                    paramiko.BadAuthenticationType) as e:
                logger.error(e)
            else:
                success = True
                logger.debug(f'({self.sessionName}) fin')
        return success

    def __del__(self):
        if self.isReady:
            logger.debug(f'--- Good bye!')


if __name__ == '__main__':
    def main():
        keyFile = './PEMs/LightsailDefaultKey-ap-northeast-1.pem'
        S = SFTPSession(sessionName='INFOX', hostname='jmf.magneticsquare.biz', username='ubuntu', keyFile=keyFile,
                        remotePath='temp', port=22,
                        localPath='./Files/INFOX', pattern='????????.data', overwrite=True, cleanUp=False)
        if S.retrieve():
            logger.info(S.newCommer)


    main()
