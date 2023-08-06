"""
    作者：mldsh
    日期：2022年09月21日16:07
    使用工具：PyCharm
"""
import re

import requests
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

        print(text,wx_id,send_url)
        if not isinstance(text, (str, type(None))):
            raise TypeError('"text" only supported: str')
        if not isinstance(wx_id, (str, type(None))):
            raise TypeError('"wx_id" only supported: str')
        if not isinstance(send_url, (str, type(None))):
            raise TypeError('"send_url" only supported: str')
        if self._re_send_url(send_url):
            raise TypeError(
                "send_ The url is required to be a url and must start with https or http. Complete connection")
        if self._check_text(text):
            raise TypeError("Message non-compliance")
        self.snow = SnowFlake()
        self.uid = self.snow.guid()
        self.send_url = send_url
        self.wx_id = wx_id
        self.text = text
        self.headers = {'Content-Type': 'application/json;charset=UTF-8'}


    @staticmethod
    def from_dict(obj, algorithm=None):
        return SendText(obj, algorithm)

    @staticmethod
    def from_json(data, algorithm=None):
        obj = json.loads(data)
        return SendText.from_dict(obj, algorithm)

    def _check_text(self,text):
        """
        验证发送文本消息，是否正常。
        :return: bool
        """
        gfw = DFAFilter()
        result = gfw.word_replace(text)
        if "*" in result:
            return True

    def _re_send_url(self, send_url):
        """
        验证 url 的是否合格
        :param self:
        :param send_url:
        :return: bool
        """
        result = re.search('(https?|ftp|file)://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]', send_url).group()
        print('222',result)
        if result:
            return False
        else:
            return True

    def bot_send_text(self,text,wx_id, send_url):
        """
        实现调用服务端接口，发送请求。
        :return:
        """
        super.__init__(text, wx_id, send_url)
        json_data = {
            "text": self.text,
            "snow_id": self.uid,
            "wx_id": self.wx_id
        }
        result = requests.post(url=self.send_url, headers=self.headers, json=json_data).json()
        return result




