"""
Basic skeleton of a mitmproxy addon.
Run as follows: mitmproxy -s anatomy.py
"""

import os
from mitmproxy import ctx



class StaticFile:
    """试试处理静态文件"""
    # def __init__(self):
    #     self.num = 0

    def request(self, flow):
        # self.num = self.num + 1
        # ctx.log.info("自定义计数器插件 %d flows：" % self.num)
        pass


addons = [
    StaticFile()
]