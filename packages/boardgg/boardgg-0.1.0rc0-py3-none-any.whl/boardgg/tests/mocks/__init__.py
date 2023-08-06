from json import JSONDecodeError


class MockedResponse(object):
    def __init__(self, data=None, status_code=200, text=""):
        self.data = data
        self.status_code = status_code
        self.status = status_code
        self.content = data
        self.text = text
        self.headers = {}
