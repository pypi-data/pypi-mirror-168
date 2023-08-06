import ssl
from email import header
from urllib.parse import urlencode
from urllib.request import Request, urlopen


def print_time():
    from datetime import datetime
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


while True:
    print(print_time())
    timeout = 40
    content_md5 = 'd9afde1daacceaf1a6b3c64584a6012f'
    url = 'http://172.29.200.206:8848/nacos/v1/cs/configs/listener?username=nacos&password=aaa123'
    data = {'Listening-Configs': f'BASE-CONFIG\x02public\x02{content_md5}\x0226b052f1-f8c9-4f31-8900-affd3c4c9e1c\x01'}
    headers = {"Long-Pulling-Timeout": 30000}
    req = Request(url, data=urlencode(data).encode(), headers=headers, method='POST')
    ctx = ssl.SSLContext()
    resp = urlopen(req, timeout=timeout, context=ctx)
    content = resp.read().decode()
    if content:
        print(content)
        break
