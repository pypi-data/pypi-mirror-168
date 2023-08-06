#-*- encoding=utf8 -*-
import requests
import json

if __name__ == '__main__':
    cookie = "token=code_space;"
    header = {
        "cookie": cookie,
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"
    }

    post_json = json.dumps({'some': 'data'})

    r3 = requests.post("http://127.0.0.1:8888/pray", data=post_json, headers=header)
    print("r3返回的内容为-->" + r3.text)
