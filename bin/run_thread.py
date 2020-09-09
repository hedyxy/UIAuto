from lib.appData import Controller, device_name_queue
from testCase.testQQThreadCase import threadDemo
from lib.logger import logger
from lib.result import Result
from lib import HTMLTestAppRunner
from lib.path import APPREPORT
import threading
import unittest

local = threading.local()


class App(object):
    def __init__(self):
        self.c = Controller()

    def case(self):
        suite = unittest.TestLoader().loadTestsFromTestCase(threadDemo)
        local.result = Result()

        res = suite.run(local.result)

        logger.debug('当前线程的的名字：%s' % threading.current_thread().getName())
        result = {threading.current_thread().getName(): res}

        for deviceName, result in result.items():
            html = HTMLTestAppRunner.HTMLTestRunner(stream=open(APPREPORT.format('{}.html'.format(deviceName)), "wb"),
                                                    verbosity=2,
                                                    title='测试')

            html.generateReport('', result)

    def run(self):
        threads = []
        self.c.server()
        if self.c.test_server():
            drivers = self.c.driver()
            logger.info('开始执行CASE！当前启动[%s]个DRIVER！' % drivers.qsize())
            for case in range(drivers.qsize()):
                t = threading.Thread(target=self.case, name=device_name_queue.get())
                threads.append(t)
                t.start()
            for t in threads:
                t.join()


if __name__ == '__main__':
    App().run()
