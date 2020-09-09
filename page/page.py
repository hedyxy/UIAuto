from lib.appData import driver_queue
from lib.pyapp import Pyapp
import threading
from appium.webdriver.common.touch_action import TouchAction
from lib.logger import logger
import time
local = threading.local()


class BasePage(object):
    def __init__(self, driver=None):
        if driver is None:
            local.driver = driver_queue.get()
            local.pyapp = Pyapp(local.driver)
        else:
            local.driver = driver
            local.pyapp = Pyapp(driver)

    def quit(self):
        local.pyapp.quit()

    def reset_package(self):
        local.pyapp.reset()


    def move(self, a=1, b=2):
        befor = self.source[a]
        after = self.source[b]
        r = (None, after[1] - befor[1], after[2] - befor[2])
        return r


    def relieve_device_lock_qq(self, num):

        element = local.pyapp.get_elements('class=>android.view.View')[num]
        location = element.location
        logger.debug('location: %s' % location)
        size = element.size
        logger.debug('size: %s' % size)
        self.source = {1: (None, location["x"] + size["width"] / 6, location["y"] + size["height"] / 6),
                       2: (None, location["x"] + size["width"] / 6 * 3, location["y"] + size["height"] / 6),
                       3: (None, location["x"] + size["width"] / 6 * 5, location["y"] + size["height"] / 6),
                       4: (None, location["x"] + size["width"] / 6, location["y"] + size["height"] / 6 * 3),
                       5: (None, location["x"] + size["width"] / 6 * 3, location["y"] + size["height"] / 6 * 3),
                       6: (None, location["x"] + size["width"] / 6 * 5, location["y"] + size["height"] / 6 * 3),
                       7: (None, location["x"] + size["width"] / 6, location["y"] + size["height"] / 6 * 5),
                       8: (None, location["x"] + size["width"] / 6 * 3, location["y"] + size["height"] / 6 * 5),
                       9: (None, location["x"] + size["width"] / 6 * 5, location["y"] + size["height"] / 6 * 5)}
        logger.debug('拆分后的9个图：%s' % self.source)
        TouchAction(local.driver).press(*self.source[1]).wait(300).move_to(*self.move(1, 2)).wait(300).move_to(
            *self.move(2, 3)).wait(300).move_to(*self.move(3, 5)).wait(300).move_to(*self.move(5, 7)).wait(
            300).move_to(
            *self.move(7, 8)).wait(300).move_to(*self.move(8, 9)).wait(300).release().perform()

class QQ_Login_Page(BasePage):
    def login(self):
        local.pyapp.click('android=>new UiSelector().text("登 录")')

    def username(self):
        local.pyapp.type('content=>请输入QQ号码或手机或邮箱', 3408467505)

    def passwd(self):
        local.pyapp.type('content=>密码 安全', 'besttest123')

    def left_close(self):
        css = 'android=>new UiSelector().text("关闭")'
        local.pyapp.click(css)

    def login_check(self, name):
        return local.pyapp.wait_and_save_exception('android=>new UiSelector().text("登 录")', name)


class SetLock(QQ_Login_Page):
    def photo(self):
        local.pyapp.click('content=>帐户及设置')

    def set_up(self):
        local.pyapp.click('content=>设置')

    def set_up_of_account(self):
        local.pyapp.click('android=>new UiSelector().text("帐号、设备安全")')

    def set_gesture_passwd(self):
        local.pyapp.click('content=>手势密码锁定')

    def create_gesture(self):
        local.pyapp.click('android=>new UiSelector().text("创建手势密码")')

    # def set_gesture(self):
    #     self.relieve_device_lock_qq(12)
    #     time.sleep(1)
    #     self.relieve_device_lock_qq(12)
    def set_gesture(self):
        element = local.pyapp.get_elements('class=>android.view.View')[12]
        location = element.location
        x = location['x']
        y = location['y']
        size = element.size
        width = size['width']
        height = size['height']
        sample_width = width/3/2
        sample_height = height/3/2
        onex= x+sample_width
        oney= y+sample_height
        twox = x + sample_width * 3
        twoy = y +sample_height
        threex = x + sample_width * 5
        threey = y + sample_width
        fourx = x + sample_width * 3
        foury = y + sample_width * 3
        TouchAction(local.driver).press(x=onex,y=oney).wait(300).move_to(x=twox-onex,y=twoy-oney).wait(300).move_to(x=threex-twox,y=threey-twoy).wait(300).move_to(x=fourx-threex,y=foury-threey).perform()

    def set_lock_check(self, name):
        return local.pyapp.wait_and_save_exception('android=>new UiSelector().text("修改手势密码")', name)

class Page(SetLock):
    pass
