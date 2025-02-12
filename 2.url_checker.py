'''
Author     : S1g0day
Creat time : 2024/3/15
Introduce  : 用于检测query_url的可用性
'''
import os
import yaml
import random
import time
from urllib.parse import urlparse
from lib.log_functions import api_logger
from lib.Requests_func import req_get

def export_available_url(url):
    """
    导出可用URL到文件
    :param url: 要导出的URL
    """
    filename = 'log/available_urls.txt'
    try:
        # 检查文件是否已存在并包含该URL
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                if url in f.read().splitlines():
                    api_logger.info(f"URL already exists in {filename}: {url}")
                    return
        
        # 如果URL不存在，则追加写入
        with open(filename, 'a') as f:
            f.write(f"{url}\n")
            api_logger.success(f"Exported URL to {filename}: {url}")
    except Exception as e:
        api_logger.error(f"Failed to export URL {url}: {str(e)}")

def check_url_availability(url):
    """
    检测URL的可用性
    :param url: 要检测的URL
    :return: 如果URL可用返回True，否则返回False
    """
    max_retries = 3
    retries = 0
    
    try:
        # 验证URL格式
        parsed_url = urlparse(url)
        if not all([parsed_url.scheme, parsed_url.netloc]):
            api_logger.error(f"Invalid URL format: {url}")
            return False

        while retries < max_retries:
            try:
                # 构造测试请求URL
                test_url = f"{url.rstrip('/')}/query/web?search=baidu.com"
                
                # 发送请求
                response = req_get(test_url, params=None)
                
                # 检查响应
                if response and response.status_code == 200:
                    try:
                        json_data = response.json()
                        if isinstance(json_data, dict) and 'params' in json_data:
                            api_logger.success(f"API is working properly: {url}")
                            export_available_url(url)
                            return True
                    except ValueError:
                        api_logger.warning(f"Invalid JSON response from {url}")
                else:
                    api_logger.warning(f"API returned status code {response.status_code if response else 'No response'}: {url}")

                retries += 1
                time.sleep(random.randint(1, 3))

            except Exception as e:
                api_logger.error(f"Failed to connect to {url}: {str(e)}")
                retries += 1
                time.sleep(random.randint(1, 3))

        api_logger.error(f"Max retries ({max_retries}) exceeded for URL: {url}")
        return False

    except Exception as e:
        api_logger.error(f"Unexpected error checking URL {url}: {str(e)}")
        return False

def validate_query_url(query_url):
    """
    验证query_url的可用性
    :param query_url: 要验证的URL
    :return: 如果URL可用返回True，否则返回False
    """
    if not query_url:
        api_logger.error("No query URL provided")
        return False
    return check_url_availability(query_url)

if __name__ == "__main__":
    with open('config/config.yaml', 'r', encoding='utf-8') as file:
        config = yaml.safe_load(file)
    for url in config['query_url']:
        if not validate_query_url(url):
            api_logger.error(f"Invalid query URL: {url}")