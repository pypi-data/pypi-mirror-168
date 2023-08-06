"""
    作者：mldsh
    日期：2022年09月21日16:07
    使用工具：PyCharm
"""
import re

from toollib.snowflake import SnowFlake
from word_filter import DFAFilter
import json


class SendText:
    """
    1.需要一个send text 方法，
    2.判断参数

    """

    def __init__(self, text, wx_id, send_url):
        """

        :param text: 文本
        :param wx_id: 接收人
        :param send_url: 后端服务
        """
        if not isinstance(text, (str, type(None))):
            raise TypeError('"text" only supported: str')
        if not isinstance(wx_id, (str, type(None))):
            raise TypeError('"wx_id" only supported: str')
        if not isinstance(send_url, (str, type(None))):
            raise TypeError('"send_url" only supported: str')
        if self._re_send_url():
            raise TypeError(
                "send_ The url is required to be a url and must start with https or http. Complete connection")
        if self._check_text():
            raise TypeError("Message non-compliance")
        self.snow = SnowFlake()
        self.uid = self.snow.guid()
        self.send_url = send_url
        self.wx_id = wx_id
        self.text = text

    @staticmethod
    def from_dict(obj, algorithm=None):
        return SendText(obj, algorithm)

    @staticmethod
    def from_json(data, algorithm=None):
        obj = json.loads(data)
        return SendText.from_dict(obj, algorithm)

    def _check_text(self):
        """
        验证发送文本消息，是否正常。
        :return: bool
        """
        gfw = DFAFilter()
        result = gfw.word_replace(self.text)
        if "*" in result:
            return True

    def _re_send_url(self):
        """
        验证 url 的是否合格
        :param self:
        :param send_url:
        :return: bool
        """
        regular = re.compile(r'[a-zA-Z]+://[^\s]*[.com|.cn]')
        result = re.findall(regular, self.send_url)
        if result:
            return False
        else:
            return True

    def bot_send_text(self):
        """

        :return:
        """

        pass