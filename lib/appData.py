from lib.tool import Tool
from appium import webdriver
from lib.logger import logger
from lib.path import LOGPATH,APPPICTUREPATH
import os
import threading
import subprocess
import time
import queue

local = threading.local()
driver_queue = queue.Queue()
device_name_queue = queue.Queue()

class Controller(object):
    def __init__(self):
        self.tool = Tool()
        self.yml = self.tool.app_data
        self.devices = self.yml.get('devices')
        self.app = self.yml.get('tester')
        self.device_type = self.yml.get('device_type')
        self.ports = []

    def kill_server(self):

        logger.debug('执行[KILL SERVER]操作:%s' % subprocess.getoutput("taskkill /F /IM node.exe /t"))
        logger.debug('重启ADB服务！%s' % subprocess.getoutput("adb kill-server"))

    def server_command(self, **kwargs):
        commond = 'appium -a {ip} -p {port} -U {deviceName} -g {log}'.format(ip=kwargs.get('ip'),
                                                                             port=kwargs.get('port'),
                                                                             deviceName=kwargs.get(
                                                                                 'deviceName'),
                                                                             log=kwargs.get('log_path'))
        logger.debug('启动服务执行的命令：%s' % commond)
        subprocess.Popen(commond, stdout=open(kwargs.get('log_path'), 'a+'), stderr=subprocess.PIPE, shell=True)

    def server(self):
        self.kill_server()
        threads_server = []
        for device in self.devices.get(self.device_type):
            device.update({'log_path': os.path.join(LOGPATH, '%s.log' % device.get('name'))})
            logger.debug("每个手机的信息：%s" % device)
            self.ports.append(device.get('port'))
            t = threading.Thread(target=self.server_command, kwargs=device)
            threads_server.append(t)
            t.start()
        for i in threads_server:
            i.join()

    def test_server(self):
        while True:
            for port in self.ports:
                test_out_put = subprocess.getoutput("netstat -ano | grep %s" % port)

                if test_out_put:
                    logger.debug('检验服务启动：%s' % test_out_put)
                    self.ports.remove(port)
                else:
                    logger.debug('端口 [%s] 服务启动失败5秒钟后尝试' % port)
            if not self.ports:
                break
            time.sleep(5)
        logger.debug('全部服务启动成功！')
        return True

    def driver_commend(self, **kwargs):
        local.desired_caps = {'platformName': '', 'platformVersion': '', 'deviceName': '',
                              "unicodeKeyboard": "True",
                              "resetKeyboard": "True", 'udid': '', 'noReset': 'True'}
        local.desired_caps.update(kwargs)
        url = 'http://{ip}:{port}/wd/hub'.format(port=local.desired_caps.get('port'),
                                                 ip=local.desired_caps.get('ip'))
        logger.debug('启动的Url：%s' % url)
        driver = webdriver.Remote(url, local.desired_caps)

        driver_queue.put(driver)
        device_name_queue.put(local.desired_caps.get('name'))
        app = APPPICTUREPATH.format(local.desired_caps.get('name'))
        if os.path.exists(app):
            self.tool.app_clear(app)
        else:
            os.makedirs(app)

    def driver(self):
        thread_driver = []
        for device_app in self.devices.get(self.device_type):
            device_app.update(self.app)
            d = threading.Thread(target=self.driver_commend, kwargs=device_app)
            thread_driver.append(d)
            d.start()
        for i in thread_driver:
            i.join()
        return driver_queue


if __name__ == '__main__':
    Controller().server()
