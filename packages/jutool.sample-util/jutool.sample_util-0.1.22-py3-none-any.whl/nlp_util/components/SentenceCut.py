from ml_util.MLComponentBase import MLComponentBase
from code_util.structures import func_check
import re


class default_sentencecut(MLComponentBase):
    def __init__(self):
        super().__init__([])
        self.cut = getattr(self['jieba'], 'cut')

    @func_check
    def call(self, linked_item: str, ori_item=None):
        return [x for x in re.split('。|, |，|\n', linked_item) if x.strip() != ""]
