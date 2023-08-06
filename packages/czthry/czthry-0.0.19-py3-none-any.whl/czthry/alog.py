import logging
import datetime
import os


class Logger(object):
    __msgfmt = '%(asctime)s.%(msecs)03d | %(filename)s:%(funcName)s[%(lineno)d] | %(levelname)s : %(message)s'
    __datefmt = '%Y-%m-%d %H:%M:%S'

    def __init__(self, filename=None):
        if filename is None:
            filename = ''
        logname = '{:%Y%m%d%H%M%S%f}'.format(datetime.datetime.now())+filename
        self.logger = logging.getLogger(logname)
        self.__checkFilePath(filename)
        self.__setupFileLog(filename)
        self.__setupConsoleLog()
        self.__setupAlias()

    def __setupFileLog(self, file):
        if file is None or len(file) == 0:
            return
        formatter = logging.Formatter(self.__msgfmt)
        formatter.datefmt = self.__datefmt
        file_handler = logging.FileHandler(file)
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.INFO)
        self.logger.addHandler(file_handler)

    def __setupConsoleLog(self):
        formatter = logging.Formatter(self.__msgfmt)
        formatter.datefmt = self.__datefmt
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(console_handler)

    def __setupAlias(self):
        self.d = self.logger.debug
        self.i = self.logger.info
        self.w = self.logger.warning
        self.e = self.logger.error
        self.x = self.logger.critical

    def __checkFilePath(self, filename):
        arr = filename.split('/')
        if len(arr) == 1:
            return
        makeFilePath(filename)


def makeFilePath(path):
    arr = path.split('/')
    if len(arr) == 1:
        return
    filepath = os.path.join(*arr[:-1])
    if os.path.exists(filepath):
        return
    paths = filepath.split('/')
    for i in range(len(paths)):
        folder = '/'.join(paths[:i + 1])
        if not os.path.exists(folder):
            os.mkdir(folder)
    return filepath


def test():
    log = Logger('./a/b/c/test.log')
    log.d('debug')
    log.i('info')
    # log.w('warning')
    # log.e('error')
    # log.x('critical')
    pass


if __name__ == '__main__':
    test()
