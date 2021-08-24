'''
$ sftp -i .\LightsailDefaultKey-ap-northeast-1.pem -p 22 ubuntu@jmf.magneticsquare.biz
'''

import paramiko
import fnmatch
import pathlib
import socket
from loguru import logger


class SFTPSession(object):  # use only key authentication, no need password
    def __init__(self, *, hostname: str, port: int = 22, username: str, keyFile: str, remotePath: str = './',
                 localPath: str = './', pattern: str = '*.*', overwrite: bool = True, name: str = 'unknown'):
        self.isReady = False
        self.timeoutSecs = 5

        self.name = name
        self.hostname = hostname
        self.port = port
        self.username = username
        self.account = f'{username}@{hostname}'
        self.basePath = pathlib.Path(remotePath)  # service's root directory
        self.localPath = pathlib.Path(localPath)
        self.pattern = pattern
        self.overwrite = overwrite

        try:
            self.pkey = paramiko.RSAKey.from_private_key_file(filename=keyFile)
        except (FileNotFoundError, paramiko.BadHostKeyException, paramiko.SSHException, UnicodeDecodeError) as e:
            logger.error(e)
        else:
            self.isReady = True
            logger.debug(f'+++ SFTP instance [{self.name}] was made as bellows')
            logger.debug(f'+++ sftp -i {keyFile} -p {self.port} {self.account}')
            logger.debug(f'+++ remotePath = [{self.basePath}] localPath = [{self.localPath}]')

    def cbEntry(self, sA: int, sW: int):
        if sA != sW:
            logger.warning(f'Accepted/Written not match [{sA}/{sW}] ???')

    def get(self) -> bool:
        success = False
        if self.isReady:
            try:
                logger.debug(f'+++ start SSH session')
                with paramiko.SSHClient() as ssh:
                    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    ssh.connect(hostname=self.hostname, port=self.port, username=self.username, pkey=self.pkey, timeout=self.timeoutSecs)
                    logger.debug(f'+++ connected')
                    with ssh.open_sftp() as sftp:
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
                                    logger.debug(f'+++ GET [{self.basePath / src}] to [{dst}]')
                                else:
                                    logger.warning(f'=== {target} is already exists')
                            else:
                                logger.warning(f'--- {src}')
            except (socket.gaierror, socket.timeout,
                    PermissionError, FileNotFoundError, paramiko.AuthenticationException,
                    paramiko.BadAuthenticationType) as e:
                logger.error(e)
            else:
                success = True
                logger.debug(f'+++ fin')
        return success

    def __del__(self):
        if self.isReady:
            logger.debug(f'--- Good bye!')


if __name__ == '__main__':
    def main():
        keyFile = './PEMs/LightsailDefaultKey-ap-northeast-1.pem'
        S = SFTPSession(name='INFOX', hostname='jmf.magneticsquare.biz', username='ubuntu', keyFile=keyFile,
                        remotePath='temp', port=22,
                        localPath='./LOGs', pattern='????????.data', overwrite=True)
        S.get()


    main()
