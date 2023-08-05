"""
Select which responses should be streamed.

Enable response streaming for all HTTP flows.
This is equivalent to passing `--set stream_large_bodies=1` to mitmproxy.
"""

from mitmproxy.script import concurrent


@concurrent
def responseheaders(flow):
    """
    Enables streaming for all responses.
    This is equivalent to passing `--set stream_large_bodies=1` to mitmproxy.
    """
    flow.response.stream = True