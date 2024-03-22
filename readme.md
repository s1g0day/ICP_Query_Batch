# 简介

从工业和信息化部政务服务平台进行的ICP备案查询，核心是`HG-ha`师傅的 [ICP_Query 项目](https://github.com/HG-ha/ICP_Query) ，虽然慢，但好用

# 搭建

不折腾了，直接docker部署 20240225版本

```
# 拉取镜像
docker pull yiminger/ymicp:yolo8_latest
# 运行并转发容器16181端口到本地所有地址
docker run -d -p 16181:16181 yiminger/ymicp:yolo8_latest
```

# 项目

## 目录

```
.
├── 0.icp_query.py
├── 1.icp_query_result_processor.py
├── 2.quchong.py
├── config
│   ├── config.yaml
│   └── domain.txt
├── lib
│   ├── Requests_func.py
│   ├── hander_random.py
│   ├── logo.py
├── log
│   ├── Processing_Domain.log
│   ├── error.log
│   ├── error_Max.log
│   ├── no_req_list.log
│   └── success.log
```

## 配置

 `config.yaml`  

```
version: "0.0.1"

# 测试平台地址
query_url:
  # - http://192.168.1.1:16181
  # - http://192.168.1.2:16181
  # - http://192.168.1.3:16181
  
# 目标文件
domains_file: "config/domain.txt"
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

# 5、断点继续，以上4点都可以使用。假设Processin日志为："4/10: 浙江淘宝网络有限公司"，想从第4个继续，命令如下
python3 0.icp_query.py -s 4
```

## 输出日志

```
.
├── Processing_Domain.log		# 进度日志，如果Ctrl+c中断的话，可以从这里看到定义起始位置
├── error.log					# 报错日志，代码初期调试用的
├── error_Max.log				# 关键日志, 代码中对domains中的每行数据最多遍历10次，如果10次都查询错误，会写入到这个日志，方便对其重新测试
├── no_req_list.log				# 关键日志，存储了查询正常但没有数据回显的情况，需要注意是否是domians信息填错，如公司名称为简写等
└── success.log					# 关键日志, 查询成功且获取到所有备案域名信息
```

## 数据处理

这里处理的是`success.log`日志

```
# 提取出域名
[root@localhost icp_query_s1g0day]# python3 1.icp_query_result_processor.py log/success.log 
yjs-cdn1.com
yjs-cdn3.com
yunjiasu-dns.com
yunjiasupreview.com
videomind.cloud
baidussl.cloud
jomoxc.com
apkprotect17.cn
hmpsvr.com
duapp.com
jiyoujia.com
xiami.net
taobao.cn
yitao.com
mpmw.com
tao123.com
kanbox.com
meipingmeiwu.com
etao.com
homearch.store

# 将域名保存到 1.txt, 创建output目录
[root@localhost icp_query_s1g0day]# mkdir output

# 运行代码，结果保存到outpu目录下。这个代码的妙用还请亲身体验
[root@localhost icp_query_s1g0day]# python3 2.quchong.py 1.txt
```

# 后续

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