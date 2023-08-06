# tkitScrapyMiddleware
tkitScrapyMiddleware

# 安装
```bash
pip install tkitScrapyMiddleware
```



# 使用

设置自动获取代理，使用

在settings设置

```python
DOWNLOADER_MIDDLEWARES = {
    #默认方法
    'tkitScrapyMiddleware.proxy.RandomProxyMiddleware': 610,

}
POOL_PROXY = "http://192.168.1.18:5010"
```