#!/usr/bin/env python
# coding=utf-8
import os
import time
import json
import random
import requests
from lib.hander_random import requests_headers

headers = requests_headers()

def req_get(url, params):

    proxies = {
        # 用sock协议时只能用socks5h 不能用socks5,或者用http协议
        'http':'socks5h://192.168.88.21:8443',
        'https':'socks5h://192.168.88.21:8443'
    }
    try:
        res = requests.get(url=url, headers=headers, params=params, verify=False, proxies=proxies)
        res.encoding = res.apparent_encoding # apparent_encoding比"utf-8"错误率更低
        return res
    except:
        print("req_get error")
        pass

def req_post(url, data=None, header=None):
    try:
        if header:
            header['Cookie'] = header
        res = requests.post(url=url, headers=headers, verify=False, data=data, allow_redirects=False, timeout=(4,20))
        res.encoding = res.apparent_encoding # apparent_encoding比"utf-8"错误率更低
        return res
    except:
        print("req_post error")
        pass

# 检查要写入的内容是否已存在于文件中
def is_output_in_log(log_file_path, output):

    if not os.path.exists(log_file_path):
        with open(log_file_path, 'a+', encoding='utf-8'):
            pass

    with open(log_file_path, 'r', encoding='utf-8') as log_file:
        log_contents = log_file.read()
        return output in log_contents
    
# 异常重试
def make_request(urls, params, search_data):
    if isinstance(urls, str):
        urls = [urls]  # 如果urls是字符串，转换为包含该字符串的列表
    elif not isinstance(urls, list):
        raise ValueError("urls must be a string or a list of strings")

    max_retries = 10  # 最大重试次数
    retries = 0
    while retries < max_retries:
        for url in urls:
            url = url.strip()
            print(f"Query url: {url}")
            try:
                response = requests.get(url +'/query/web', params=params, headers=headers, allow_redirects=False)
                response.encoding = response.apparent_encoding # apparent_encoding比"utf-8"错误率更低
                if response.status_code == 200:
                    '''
                        {"code": 101, "msg": "参数错误,请指定search参数"}
                        {"code": 122, "msg": "查询失败"}
                        {"success": false, "code": 415, "msg": "参数异常,content_type_not_supported"}
                        {"code": 201, "error": "验证码识别失败"}
                        {"success": false, "code": 429, "msg": "您目前访问频次过高[访问ip：55.24.61.23], 请稍后再试。"}
                    '''
                    req = json.loads(response.text)
                    if req.get('code') == 200:
                        success_sleep = random.randint(5, 15)
                        print(f"Query was successful. wait {success_sleep}s ...")
                        # time.sleep(success_sleep)  # 间隔重试
                        return req
                    else:
                        print("Request failed. Retrying...")
                        if req.get('code') == 201:
                            jsondumpdata = f"search_data:{search_data}, code:{req['code']}, msg:{req['error']}"
                        else:
                            jsondumpdata = f"search_data:{search_data}, code:{req['code']}, msg:{req['msg']}"
                        print(jsondumpdata)
                        error_log_file_path = 'log/error.log'
                        if not is_output_in_log(error_log_file_path, jsondumpdata):
                            open(error_log_file_path, 'a+', encoding='utf-8').write(f"{jsondumpdata}\n")
                        if req.get('code') == 429:
                            error_sleep = random.randint(60, 120)  # 间隔重试
                            print(f"Frequency too high. Switching to next URL. wait {error_sleep}s ...")
                            # time.sleep(error_sleep)
                            continue  # 跳出当前URL的循环
                else:
                    error_sleep = random.randint(5, 15)  # 间隔重试
                    print(f"Request status_code is {response.status_code}. Retrying{error_sleep}s ...")
                    error_status_code_log_file_path = 'log/error_status_code.log'
                    if not is_output_in_log(error_status_code_log_file_path, search_data):
                        open(error_status_code_log_file_path, 'a+', encoding='utf-8').write(f"{search_data}\n")
                    # time.sleep(error_sleep)
            except Exception as e:
                print("Exception occurred:", str(e))
                # time.sleep(random.randint(5, 10))  # 异常发生时等待一段时间再继续
        retries += 1
    print("Max retries exceeded. Failed to get successful response.")
    error_Max_log_file_path = 'log/error_max.log'
    if not is_output_in_log(error_Max_log_file_path, search_data):
        open(error_Max_log_file_path, 'a+', encoding='utf-8').write(f"{search_data}\n")
    return None
