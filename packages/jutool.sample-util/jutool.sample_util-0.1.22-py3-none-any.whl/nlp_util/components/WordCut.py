import time

from ml_util.MLComponentBase import MLComponentBase
from code_util.structures import func_check


class default_jieba(MLComponentBase):
    def __init__(self):
        super().__init__(["jieba"])
        self.cut = getattr(self['jieba'], 'cut')

    @func_check
    def call(self, linked_item: str, ori_item=None):
        return [word for word in self.cut(linked_item)]


