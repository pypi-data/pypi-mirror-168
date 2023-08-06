import time
from qrunner.utils.log import logger


class Page(object):

    def __init__(self, driver):
        self.driver = driver

    @staticmethod
    def sleep(n):
        logger.info(f'休眠 {n} 秒')
        time.sleep(n)

