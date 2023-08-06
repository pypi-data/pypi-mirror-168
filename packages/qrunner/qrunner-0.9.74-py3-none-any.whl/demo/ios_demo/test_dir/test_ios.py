import qrunner
from qrunner import IosElement


class HomePage:
    ad_close_btn = IosElement(label='close white big', desc='首页广告关闭按钮')
    bottom_my = IosElement(label='我的', desc='首页底部我的入口')


@qrunner.story('首页')
class TestClass(qrunner.IosTestCase):

    def start(self):
        self.hp = HomePage()

    @qrunner.title('从首页进入我的页')
    def testcase(self):
        self.hp.ad_close_btn.click()
        self.hp.bottom_my.click()
        self.assertText('我的订单')
