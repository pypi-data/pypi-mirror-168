import qrunner


@qrunner.story('PC站首页')
class TestClass(qrunner.TestCase):

    @qrunner.title('查询PC站首页banner列表')
    @qrunner.file_data('card_type', 'data.json')
    def test_getToolCardListForPc(self, card_type):
        path = '/api/qzd-bff-app/qzd/v1/home/getToolCardListForPc'
        load = {"type": card_type}
        self.post(path, json=load)
        self.assertEq('code', 0)
