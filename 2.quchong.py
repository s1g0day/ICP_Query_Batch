import re
import sys
import idna
import socket

# 中文域名转ASCII
def convert_to_ascii(domain):
    try:
        ascii_domain = idna.encode(domain).decode('ascii')
        return ascii_domain
    except Exception as e:
        print("转换失败:", e)
        return None

def is_chinese_domain(domain):
    for char in domain:
        if ord(char) > 127:  # 如果字符的 ASCII 编码大于 127，则说明是非 ASCII 字符，可能是中文字符
            return True
    return False

# url ip 排序
def ip_url_output(ips_list, IP_vaild, domain_vaild):
    for i in ips_list:
        for j in IP_vaild:
            ipList = re.findall(r'[0-9]+(?:\.[0-9]+){3}', j)
            if i == ipList[0]:
                if j and j not in domain_vaild:
                    domain_vaild.append(j)
    return domain_vaild

# IP排序
def IP_sort(ip_addresses):

    # 使用set()函数进行去重
    unique_ips = set(ip_addresses)

    # 使用socket库中的inet_aton函数将IP地址转换为32位二进制数，然后再将其转换为整数
    ip_integers = [socket.inet_aton(ip) for ip in unique_ips]
    ip_integers.sort()

    # 使用socket库中的inet_ntoa函数将整数转换回IP地址格式
    sorted_ips = [socket.inet_ntoa(ip) for ip in ip_integers]

    # print(sorted_ips)
    return sorted_ips

# 提取纯粹的IP地址
def get_ip(IP_vaild):
    ips = set() # 使用集合来存储已经添加数据
    for i in IP_vaild:
        ipList = re.findall(r'[0-9]+(?:\.[0-9]+){3}', i)
        ips.add(ipList[0])  # 使用集合来存储已经添加
    sorted_ips = IP_sort(list(ips)) # 将集合转换为列表并排序返回
    return  sorted_ips
    
# 区分IP和域名
def domain_or_ip(urls):
    IP_vaild = []
    domain_vaild = []
    ascii_domain = []
    res = r'((2[0-4]\d|25[0-5]|[01]?\d\d?)\.){3}(2[0-4]\d|25[0-5]|[01]?\d\d?)'
    for i in range(len(urls)):
        if re.search(res, urls[i]):
            IP_vaild.append(urls[i])
        else:
            if is_chinese_domain(urls[i]):
                domain_ascii = convert_to_ascii(urls[i])     # 转换为 ASCII 格式
                if domain_ascii:
                    # print(f"Domain:{urls[i]}, domain_ascii:{domain_ascii}")
                    ascii_domain.append(domain_ascii)
            else:
                domain_vaild.append(urls[i])
    return IP_vaild, domain_vaild, ascii_domain

# url去重
def url_quchong(file_name):
    urls = []
    texts = []
    with open(file_name, 'r', encoding='utf-8') as files:
        filelist = files.readlines()
        for i in filelist:
            if "//" in i.split()[0]:
                url = i.split()[0].split("//")[1]
                if url and url not in urls:
                    urls.append(url)
                    texts.append(i.split()[0])
            else:
                url = i.split()[0]
                if url and url not in urls:
                    urls.append(url)
                    texts.append(i.split()[0])
                else:
                    print(url)
    return urls, texts

def save(output, data):
    savedata = []
    with open(output, 'w', encoding='utf-8') as fs:
        for i in data:
            if i and i not in savedata:
                fs.write(i + '\n')

def main(files):
    # 去重
    urls, texts = url_quchong(files)

    # 提取域名和IP
    IP_vaild, domain_vaild, ascii_domain = domain_or_ip(texts)

    # 提取纯粹IP
    ips = get_ip(IP_vaild)

    # IP 排序
    ips_list = sorted(ips, key=socket.inet_aton)
    url_set = ip_url_output(ips_list, IP_vaild, domain_vaild)

    # 保存结果

    ips_output = 'log/' + files + '_output_ips.txt'
    save(ips_output, ips)
    ascii_domain_output = 'log/' + files + '_output_ascii_domain.txt'
    save(ascii_domain_output, ascii_domain)
    all_output = 'log/' + files + '_output_all.txt'
    save(all_output, url_set)
    print('纯IP已保存到: ', ips_output)
    print('Ascii结果已保存到: ', ascii_domain_output)
    print('去重结果已保存到: ', all_output)

if __name__ == '__main__':

    main(sys.argv[1])
