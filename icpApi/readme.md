## 1、添加socks代理

**安装`aiohttp_socks`**： 首先，确保你已经安装了`aiohttp_socks`库。如果没有安装，可以通过以下命令安装：   

```
pip install aiohttp_socks
```

**修改`_init_session`方法**： 在`beian`类的`_init_session`方法中，你需要设置代理。这里假设你使用的是Socks5代理，并且代理的地址是`127.0.0.1`，端口是`7890`。   修改后的`_init_session`方法如下：

````
cp ymicp.py ymicp_socks_v2.py
vi ymicp_socks_v2.py
````

`ymicp_socks_v2.py`

```
from aiohttp_socks import SocksConnector

async def _init_session(self):
    self.session = aiohttp.ClientSession(connector=SocksConnector.from_url('socks5://127.0.0.1:8443'))
```

**测试代码**： 确保你的代理设置正确，并且代理服务器正在运行。你可以通过运行你的代码来测试代理是否生效。

```
root@b5158010562d:/icpApi_20240221_yolo8# python3 ymicp_socks_v2.py 
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
ymicp_socks_v2.py:75: DeprecationWarning: SocksConnector is deprecated. Use ProxyConnector instead.
  self.session = aiohttp.ClientSession(connector=SocksConnector.from_url('socks5://127.0.0.1:8443'))
Loading model_data/best.onnx for ONNX Runtime inference...

0: 320x320 5 texts, 23.9ms
Speed: 4.2ms preprocess, 23.9ms inference, 2.6ms postprocess per image at shape (1, 3, 320, 320)
[W NNPACK.cpp:64] Could not initialize NNPACK! Reason: Unsupported hardware.
查询结果：
{'code': 200, 'msg': '操作成功', 'params': {'endRow': 0, 'firstPage': 1, 'hasNextPage': False, 'hasPreviousPage': False, 'isFirstPage': True, 'isLastPage': True, 'lastPage': 1, 'list': [{'contentTypeName': '出版、出版、文化、文化、宗教、宗教、出版、文化、宗教、出版', 'domain': 'qq.com', 'domainId': 190000203203, 'leaderName': '', 'limitAccess': '否', 'mainId': 547280, 'mainLicence': '粤B2-20090059', 'natureName': '企业', 'serviceId': 4134047, 'serviceLicence': '粤B2-20090059-5', 'unitName': '深圳市腾讯计算机系统有限公司', 'updateRecordTime': '2022-09-06 15:51:52'}], 'navigatePages': 8, 'navigatepageNums': [1], 'nextPage': 1, 'pageNum': 1, 'pageSize': 10, 'pages': 1, 'prePage': 1, 'size': 1, 'startRow': 0, 'total': 1}, 'success': True}
```

**配置API代码**

```
cp icpApi.py icpApi-socks.py
vi icpApi-socks.py
```

修改导入包

```
from ymicp_socks_proxy import beian
```

修改端口

```
    web.run_app(
        app,
        host = "0.0.0.0",
        port = 16182
    )
```

我的程序运行在ymicp docker环境内，所有无所谓端口是多少，也不需要映射到宿主机

## 2、添加header认证

```
async def options_middleware(app, handler):
    async def middleware(request):
        # 验证header
        auth_header = request.headers.get('Authorization')
        if not auth_header or auth_header != 'Bearer your-secret-token':
            api_logger.warning(f"未授权访问: {request.remote} - {request.path}")
            return wj({'code': 404, "msg": "Unauthorized"}, status=404, headers=corscode)

        # 处理 OPTIONS 请求
        if request.method == 'OPTIONS':
            api_logger.info(f"OPTIONS请求: {request.remote} - {request.path}")
            return wj(headers=corscode)
        
        try:
            response = await handler(request)
            response.headers.update(corscode)
            if response.status == 200:
                api_logger.log_request(request, 200, "请求成功")
                return response
        except web.HTTPException as ex:
            api_logger.error(f"请求异常: {request.remote} - {request.path} - {ex.status} - {ex.reason}")
            if ex.status == 404:
                return wj({'code': ex.status,"msg":"查询请访问http://0.0.0.0:16181/query/{name}"},headers=corscode)
            return wj({'code': ex.status,"msg":ex.reason},headers=corscode)
        
        return response
    return middleware
```

## 3、添加日志系统

`logger.py`

`ip_analyzer.py`
