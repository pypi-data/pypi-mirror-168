"""域名从定向
"""
from mitmproxy import http
# import mitmproxy.addonmanager.Loader
class MtHttpRedirectRequest:
    def __init__(self):
        pass

    # def load(self, loader: mitmproxy.addonmanager.Loader):
        
    #     pass
    
    def request(self, flow: http.HTTPFlow) -> None:
        if flow.request.pretty_host == "mt.l":
            """转发到nextjs api 后台（此后台的功能，将会逐步迁移到mitmproxy 插件的形式实现）"""
            flow.request.host = "localhost"
            
        # 下面这个在正向代理中才能发货作用。
        if flow.request.pretty_host.endswith("baidu.com") and flow.request.path == "/hello":
            """范例：改写特定网址的路径内容"""
            flow.response = http.Response.make(
                200,  # (optional) status code
                # b"Hello World",  # (optional) content
                # foo(),
                {"Content-Type": "text/html"}  # (optional) headers
            )
        if flow.request.path == "/hello":
            flow.response = http.Response.make(
                200,  # (optional) status code
                b"Hello World",  # (optional) content
                # foo(),
                {"Content-Type": "text/html"}  # (optional) headers
            )
            
        # 在反向代理中，发挥作用，强行，让后面的流程请求的时候，是请求www.baidu.com站点
        # 这实际上，让 --mode reverse:https://httpbin.org 中的网址参数变得不重要了。
        else:
            flow.request.host = "www.baidu.com"

addons = [
    MtHttpRedirectRequest()
]
