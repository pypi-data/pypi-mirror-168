import qrunner
from qrunner import AndroidElement


class HomePage:
    ad_close_btn = AndroidElement(rid='id/bottom_btn', desc='首页广告关闭按钮')
    bottom_my = AndroidElement(rid='id/bottom_view', index=3, desc='首页底部我的入口')


@qrunner.story('首页')
class TestClass(qrunner.AndroidTestCase):
    
    def start(self):
        self.hp = HomePage()
    
    @qrunner.title('从首页进入我的页')
    def testcase(self):
        self.hp.ad_close_btn.click()
        self.hp.bottom_my.click()
        self.assertText('我的订单')
