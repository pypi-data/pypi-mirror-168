import qrunner
from qrunner import WebElement


class PatentPage:
    search_input = WebElement(tid='driver-home-step1', desc='查专利首页输入框')
    search_submit = WebElement(tid='driver-home-step2', desc='查专利首页搜索确认按钮')


@qrunner.story('专利检索')
class TestClass(qrunner.WebTestCase):
    
    def start(self):
        self.pp = PatentPage()
    
    @qrunner.title('专利简单检索')
    def testcase(self):
        self.open_url()
        self.pp.search_input.set_text('无人机')
        self.pp.search_submit.click()
        self.assertTitle('无人机专利检索-企知道')
