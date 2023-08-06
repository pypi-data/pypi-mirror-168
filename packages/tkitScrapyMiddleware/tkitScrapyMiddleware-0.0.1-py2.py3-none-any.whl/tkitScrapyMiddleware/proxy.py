# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
"""
设置自动获取代理，使用

在settings设置

    ```python
    DOWNLOADER_MIDDLEWARES = {
        #默认方法
        'tkitScrapyMiddleware.proxy.RandomProxyMiddleware': 610,

    }
    POOL_PROXY = "http://192.168.1.18:5010"
    ```

"""

import requests
from scrapy import signals

class GetIP(object):
    """
    用于随机获取代理ip
    代理池构建 参考 https://git.jetbrains.space/terrychanorg/crawler/proxy_pool.git
    服务器地址填写上面采用

    """

    def __init__(self, host="https://api.maomihezi.com/proxypool"):
        self.api = host
        pass

    def get_random_ip(self, proxy_type="all"):
        """
        获取一个代理
        proxy_type 可选择 all 或者https

        :return:
        """
        if proxy_type == "all":
            json_resp = requests.get(self.api + "/get/").json()
        else:
            json_resp = requests.get(self.api + "/get/?type=https").json()
        if json_resp.get("proxy"):
            if not json_resp.get("https"):
                # return  json_resp.get("proxy")
                return "http://{}".format(json_resp.get("proxy"))
            else:
                return "https://{}".format(json_resp.get("proxy"))

    def delete_proxy(self, proxy):
        """
        删除无效的代理

        :param proxy:
        :return:
        """
        requests.get(self.api + "/delete/?proxy={}".format(proxy))

class RandomProxyMiddleware(object):
    """
    对应代理方案1
    # 代理池构建 参考 https://git.jetbrains.space/terrychanorg/crawler/proxy_pool.git

    """

    # 动态设置ip代理
    def process_request(self, request, spider):
        # get_ip = GetIP()
        # print("settings",spider.settings.get("POOL_PROXY"))
        get_ip = GetIP(host=spider.settings.get("POOL_PROXY"))

        # print(request.url)
        # 根据链接的协议进行自动判别是否使用https
        if "https:" in request.url:
            proxy = get_ip.get_random_ip(proxy_type="https")
        else:
            proxy = get_ip.get_random_ip(proxy_type="all")
            # if
        # print("use proxy：", proxy, "url:", request.url)
        # spider.logger.info('Spider use proxy:' ,proxy, request.url)
        spider.logger.info(f'Spider use proxy: {proxy} url: {request.url}' )
        # 修改代理信息
        request.meta["proxy"] = proxy
        # request.meta["proxy"] = to_bytes("http://%s" % proxy)
        # request.meta["http_proxy"] = proxy
        # request.meta["https_proxy"] = proxy

