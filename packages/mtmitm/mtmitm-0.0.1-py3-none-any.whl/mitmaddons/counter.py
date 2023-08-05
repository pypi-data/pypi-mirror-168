"""
Basic skeleton of a mitmproxy addon.
Run as follows: mitmproxy -s anatomy.py
"""
from mitmproxy import ctx
from mitmproxy import proxy, options
from mitmproxy.tools.dump import DumpMaster
from mitmproxy.script import concurrent
from mitmproxy import flowfilter
from mitmproxy import ctx, http
from mitmproxy.options import Options
# from mitmproxy.proxy.config import ProxyConfig
from mitmproxy import proxy, options

from mitmproxy.tools import main


import threading
import asyncio
import time
# import pymongo
import json

class Counter:
    def __init__(self):
        self.num = 0

    def request(self, flow):
        self.num = self.num + 1
        ctx.log.info("自定义计数器插件 %d flows：" % self.num)


addons = [
    Counter()
]



def start():

    opts = options.Options(listen_port=8090)
    # proxy.config
    # pconf = proxy.config.ProxyConfig(opts)
    
    config = proxy.ProxyConfig(opts)
    
    m = DumpMaster(opts)
    m.server = proxy.server.ProxyServer(config)
    
    # 添加插件
    m.addons.add(Counter())

    #启动
    try:
        m.run()
    except KeyboardInterrupt:
        m.shutdown()

class AdjustBody:
    def response(self, flow: http.HTTPFlow) -> None:
        if "google" in flow.request.url:
            print("Before intercept: %s" % flow.response.text)
            flow.response.content = bytes("This is replacement response", "UTF-8")
            print("After intercept: %s" % flow.response.text)


# see source mitmproxy/master.py for details
def loop_in_thread(loop, m):
    asyncio.set_event_loop(loop)  # This is the key.
    m.run_loop(loop.run_forever)
    
    
async def stop():
    # Sleep 10s to do intercept
    await asyncio.sleep(10)
    ctx.master.shutdown()
    
    
    
def start():
    add_on = AdjustBody()
    
    # options = Options(listen_host='0.0.0.0', listen_port=8080, http2=True)
    # m = DumpMaster(options, with_termlog=False, with_dumper=False)
    # config = ProxyConfig(options)
    # m.server = ProxyServer(config)
    # m.addons.add(Addon())

    # run mitmproxy in backgroud, especially integrated with other server
    
    
    options = main.options.Options(listen_host='0.0.0.0', listen_port=8000, http2=True)
    master = DumpMaster(options=options)
    
    master.addons.add(
            # // addons here
            add_on
    )
    
    master.run()
    

if __name__ == '__main__':
    # 用这种方式，勉强命令行的麻烦
    
    
    
    # try:
    #     asyncio.ensure_future(stop())
    #     master.run()
    # except KeyboardInterrupt:
    #     master.shutdown()
        

    loop = asyncio.get_event_loop()
    # t = threading.Thread( target=loop_in_thread, args=(loop,) )
    # t.start()
    
    # start()
    
    pending = asyncio.all_tasks(loop)