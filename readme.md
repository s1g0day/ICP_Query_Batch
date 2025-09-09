# 简介

从工业和信息化部政务服务平台进行的ICP备案查询，核心是`HG-ha`师傅的 [ICP_Query 项目](https://github.com/HG-ha/ICP_Query) ，虽然慢，但好用

# 搭建

不折腾了，直接docker部署 20250906版本

```
# 拉取镜像
docker pull yiminger/ymicp
# 运行并转发容器16181端口到本地所有地址
docker run -d -p 16181:16181 yiminger/ymicp
```

# 项目

## 目录

```
.
├── 0.icp_query.py
├── 1.icp_query_result_processor.py
├── 2.url_checker.py
├── config
│   ├── config.yaml
│   └── domain.txt
├── lib
│   ├── Requests_func.py
│   ├── hander_random.py
│   ├── logo.py
│   ├── log_functions.py
├── log

│   └── application.log
│   └── available_urls.log
│   └── error_max.log
│   └── error_occurred.log
│   └── error_status_code.log
│   └── error_icp.log
│   └── no_req_list.log
│   └── processing_Domain.log
│   └── success.log
```

## 配置

 `config.yaml`  

```
version: "0.0.7"

# 测试平台地址
query_url:
  # - http://192.168.1.1:16181
  # - http://192.168.1.2:16181
  # - http://192.168.1.3:16181
  
# 目标文件
domains_file: "config/domain.txt"
```

检测query_url可用性，可用url输出到logs目录`available_urls.log`

```
python3 2.url_checker.py
```

测试平台地址使用的是多个服务器搭建组成负载均衡的效果。为什么用多个服务器搭建？

一是因为处理报错。

- 主要是解决频次问题，常见查询报错如下：

```
{"code": 101, "msg": "参数错误,请指定search参数"}
{"code": 122, "msg": "查询失败"}
{"success": false, "code": 415, "msg": "参数异常,content_type_not_supported"}
{"code": 201, "error": "验证码识别失败"}
{"success": false, "code": 429, "msg": "您目前访问频次过高[访问ip：x.x.x.x], 请稍后再试。"}
```

二是测试拥有的几个订阅及免费代理池，代理可用但均无法正常访问到`beian.miit.gov.cn`

三是有这么多的吃灰VPS，任性。

- 建议本地运行，这样就多一套运行环境

- 一般本地搭建一套，然后再从两个VPS搭建后组成负载环境，基本上就能自动处理所有报错了



 `domain.txt` 

```
北京百度网讯科技有限公司
浙江淘宝网络有限公司
```

当然也可以是域名

```
baidu.com
taobao.com
```

不管是域名还是公司名称，只要确认无误，都会遍历出所有备案域名

## 使用方法

```
python3 0.icp_query.py -h

 ____  _        ___  ____
/ ___|/ | __ _ / _ \|  _ \  __ _ _   _
\___ \| |/ _` | | | | | | |/ _` | | | |
 ___) | | (_| | |_| | |_| | (_| | |_| |
|____/|_|\__, |\___/|____/ \__,_|\__, |
         |___/                   |___/

Powered by S1g0Day
--------------------------------------

usage: 0.icp_query.py [-h] [-d QUERY_URL] [-u DOMAIN] [-uf DOMAINS_FILE] [-s START_INDEX]

options:
  -h, --help        show this help message and exit
  -d QUERY_URL      请输入测试平台地址
  -u DOMAIN         请输入目标
  -uf DOMAINS_FILE  请输入目标文件
  -s START_INDEX    请输入起始位置，第一个数据的下标为0
```

命令示例

```
# 1、使用配置文件内的平台地址及目标文件
python3 0.icp_query.py

# 2、使用配置文件内的平台地址，指定其他目标或目标文件
python3 0.icp_query.py -u baidu.com
python3 0.icp_query.py -u 浙江淘宝网络有限公司
python3 0.icp_query.py -uf conf/domain.txt

# 3、指定平台地址、使用配置文件内的目标文件
python3 0.icp_query.py -d http://192.168.1.1:16181

# 4、指定平台地址、目标或目标文件
python3 0.icp_query.py -d http://192.168.1.1:16181 -u baidu.com
python3 0.icp_query.py -d http://192.168.1.1:16181 -uf conf/domain.txt

# 5、断点继续，以上4点都可以使用。假设 processing_Domain 日志为："4/10: 浙江淘宝网络有限公司"，想从第4个继续，命令如下
python3 0.icp_query.py -s 4
```

## 输出日志

```
.
├── application.log				# 运行日志，代码初期调试用的(可忽略)
├── available_urls.log			# 可用平台地址列表
├── error_max.log				# 关键日志(需重新测试), 代码中对domains中的每行数据最多遍历10次，如果10次都查询错误，会写入到这个日志，方便对其重新测试
├── error_occurred.log			# 关键日志(需重新测试)，查询异常，原因需要通过debug查看
├── error_status_code.log		# 报错日志, 测试平台地址请求失败日志(可忽略)，通过error_Max.log查询失败的记录
├── error_icp.log         		# 查询异常日志(需重新测试)，主要是记录总量与实际数据不符的问题
├── no_req_list.log				# 关键日志(需重新测试)，存储了查询正常但没有数据回显的情况，需要注意是否是domians信息填错，如公司名称为简写等
├── processing_Domain.log		# 进度日志，如果Ctrl+c中断的话，可以从这里看到定义起始位置
└── success.log					# 关键日志, 查询成功且获取到所有备案域名信息
```

## 数据处理

这里处理的是`success.log`日志

```
# 提取出域名
[root@localhost icp_query_s1g0day]# python3 1.icp_query_result_processor.py log/success.log 

# 导出为xlsx文件
# 将域名保存到 1.txt
# 运行代码，结果保存到log目录下。这个代码的妙用还请亲身体验
[root@localhost icp_query_s1g0day]# python3 2.quchong.py 1.txt
```

`quchong.py`日志

```
.
├── _output_ascii_domain.txt	# 筛选出所有中文域名并将其转为ascii的结果
├── _output_ips.txt				# 筛选出所有IP并将其排序后的结果
└── _output_all.txt				# 所有域名及IP结果，其中中文域名及转换结果已打印在输出行，并未写入当前日志
```

也可以使用 [data_processor](https://github.com/s1g0day/data_processor) 进行数据处理

# Lssuse

该项目只适合分享、学习、交流，不得用于商业及非法用途。觉得项目不错的小伙伴，可以在右上角Star一下，后期项目会不断优化，在使用过程中什么建议与BUG ，欢迎大家提交Lssuse

# 后续

20240621-更新

没事的时候还是要想想怎么解决代理或代理池问题，针对本地和远程服务器分别有几种方案

- 本地
  - [x] 修改代码使aiohttp走代理
  - [ ] ~~linux环境走全局代理~~
  - [ ] ~~docker容器启动时走socks~~
  - [ ] ~~利用proxychains使python走代理~~
- 远程
  - [x] 修改代码使aiohttp走代理
  - [ ] ~~合理购买代理池~~

本次使用的是 [Rain-kl/glider_guid41asd4asd](https://github.com/Rain-kl/glider_guid41asd4asd) 组成的代理池

**协议选择**: 我的订阅有两个协议：ss和trojan，之前一直用的是ss，但存在一些未知的问题无法应用到aiohttp上面。今天稍微做了一些修改，改为使用trojan协议，发现竟然可以用，多走多少弯路。

修改`订阅转换.py`，生成`forward=trojan://pass@host:port[?serverName=SERVERNAME][&skipVerify=true][&cert=PATH]`

```
def parse_config(array: list):
    ss = []
    # {'name': '泰国', 'type': 'ss', 'server': 'xxx.cn', 'port': 123, 'cipher': 'chacha20-ietf-poly1305', 'password': 'password', 'udp': True}
    vmess = []
    # { name: '香港', type: vmess, server: 'xxx.cn', port: 123, uuid: ac005860, alterId: 0, cipher: auto, udp: true }
    trojan = []
    # { name: '[trojan] 香港 01', type: trojan, server: ixxx.xxx.cn, port: 50002, password: xxxxx, udp: true, skip-cert-verify: true }
    # { name: 香港02, type: trojan, server: xxx.xxx.cn, port: 50002, password: xxxxx, udp: true, sni: xxxx-cert.com, skip-cert-verify: true }

    keywords = ['最新', '流量', '重置', '到期']
    for node in array:
        if any(keyword in node['name'] for keyword in keywords):
            pass
        else:
            if node['type'] == 'ss':
                node = f"{node['type']}://{node['cipher']}:{node['password']}@{node['server']}:{node['port']}#{node['name']}"
                ss.append(node)
            elif node['type'] == 'vmess':
                node = f"{node['type']}://none:{node['uuid']}@{node['server']}:{node['port']}?alterID={node['alterId']}"
                vmess.append(node)
            elif node['type'] == 'trojan':
                if 'sni'in node:
                    node = f"{node['type']}://{node['password']}@{node['server']}:{node['port']}?serverName={node['sni']}&skipVerify={node['skip-cert-verify']}#{node['name']}"
                else:
                    node = f"{node['type']}://{node['password']}@{node['server']}:{node['port']}?skipVerify={node['skip-cert-verify']}#{node['name']}"
                trojan.append(node)
    for node in ss:
        print(f'forward={node}')
    for node in vmess:
        print(f'forward={node}')
    for node in trojan:
        print(f'forward={node}')
```

根据实际情况修改原本`ymicp-socks.py`代码，后续详情阅读 `icpApi/readme.md`

---

20240522-更新

- 最近有师傅使用相同的技术栈重写了一个查询工具[ICP-spider](https://github.com/ravizhan/ICP-spider/)，尝试了下速度和准确度确实比当前的速度快，应该是重新训练了数据模型，感兴趣的可以试用一下。
- 当前项目稳定运行，近段时间也比较忙，暂时不进行合并了。下个大版本重新训练一下，搞个查询过程中自动添加数据并进行训练的功能，感兴趣的师傅可以自己二开一下。

---

20240408-补充

朋友给了一个[快代理](https://www.kuaidaili.com/)的账号，我测试了一下可以正常使用，确实比我免费的好使。

如果使用代理池的话需要将`icpApi/ymicp_socks_proxys.py`的内容替换到docker环境中的`ymicp.py`，其中需要修改以下信息

```
        # 隧道域名:端口号
        self.tunnel = "XXX.XXX.com:15818"
        # 用户名和密码方式
        self.username = "username"
        self.password = "password"
```

测试成功，可以看到使用了client ip，并且查询成功。但失败率是比较高，重试了6遍才成功

```
root@323f2fa05c9a:/icpApi_20240221_yolo8# python3 ymicp-socks.py 
Loading weights into state dict...
model_data/best_epoch_weights.pth model loaded.
Configurations:
----------------------------------------------------------------------
|                     keys |                                   values|
----------------------------------------------------------------------
|               model_path |        model_data/best_epoch_weights.pth|
|              input_shape |                                 [32, 32]|
|          letterbox_image |                                    False|
|                     cuda |                                    False|
----------------------------------------------------------------------
sucess! client ip: 117.90.45.134 
Loading model_data/best.onnx for ONNX Runtime inference...

0: 320x320 5 texts, 32.1ms
Speed: 1.7ms preprocess, 32.1ms inference, 12.2ms postprocess per image at shape (1, 3, 320, 320)
查询结果：
{'code': 200, 'msg': '操作成功', 'params': {'endRow': 0, 'firstPage': 1, 'hasNextPage': False, 'hasPreviousPage': False, 'isFirstPage': True, 'isLastPage': True, 'lastPage': 1, 'list': [{'contentTypeName': '出版、文化、出版、新闻、宗教、出版、宗教、文化、新闻、新闻', 'domain': 'qq.com', 'domainId': 190000203203, 'leaderName': '', 'limitAccess': '否', 'mainId': 547280, 'mainLicence': '粤B2-20090059', 'natureName': '企业', 'serviceId': 4134047, 'serviceLicence': '粤B2-20090059-5', 'unitName': '深圳市腾讯计算机系统有限公司', 'updateRecordTime': '2022-09-06 15:51:52'}], 'navigatePages': 8, 'navigatepageNums': [1], 'nextPage': 1, 'pageNum': 1, 'pageSize': 10, 'pages': 1, 'prePage': 1, 'size': 1, 'startRow': 0, 'total': 1}, 'success': True}
```

以上只是使用示例，可以根据自己的情况做出响应的调试。

---

关于使用代理的问题

- 添加代理需要再原项目上做修改，测试了几次后，由于之前的问题，遂放弃了使用。

- 后测试代理节点使用浏览器正常访问到`beian.miit.gov.cn`，仅python无法使用，所以是自身的代码问题，但已经折腾完负载了，就不想再折腾了

- 我这里提供一份代码文件`icpApi\ymicp-socks.py`及使用的代理池项目

  ```
  爱加速代理池: https://github.com/s1g0day/Aijiasu_Agent_Pool
  节点转换成爬虫代理池: https://github.com/Rain-kl/glider_guid41asd4asd
  免费代理IP池: https://github.com/pingc0y/go_proxy_pool
  ```

  如果有解决的师傅，还请给小弟一个`fork`的机会

---



再次感谢`HG-ha`师傅， [ICP_Query 项目](https://github.com/HG-ha/ICP_Query) 好用！！！

如果本项目对你有用，还请star一下。哈哈

