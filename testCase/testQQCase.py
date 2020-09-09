import unittest
from page.page import Page
import time


class QQDemo(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.page = Page()
    @classmethod
    def tearDownClass(cls):
        cls.page.quit()

    def test_a_qq_login(self):
        self.page.reset_package()
        self.page.login()
        self.page.username()
        self.page.passwd()
        self.page.login()
        self.assertTrue(self.page.login_check(self.test_a_qq_login.__name__), 'msg')

    def test_b_set_device_lock_qq(self):
        self.page.photo()
        self.page.set_up()
        self.page.set_up_of_account()
        self.page.set_gesture_passwd()
        self.page.create_gesture()
        self.page.set_gesture()
        self.assertTrue(self.page.set_lock_check(self.test_b_set_device_lock_qq.__name__), 'msg')

if __name__ == '__main__':
    unittest.main()