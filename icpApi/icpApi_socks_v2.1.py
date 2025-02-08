'''
author     : s1g0day
Creat time : 2024/2/21 14:52
modification time: 2025/2/8 14:30
Remark     : 指定socks文件，无认证，配置日志系统
'''

from functools import wraps
from aiohttp import web
import json
from ymicp_socks import beian
from logger import api_logger
from ip_analyzer import ip_analyzer

# 跨域参数
corscode = {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, OPTIONS', # 需要限制请求就在这里增删
                'Access-Control-Allow-Headers': '*',
                'Server':'Welcome to api.wer.plus',
            }

# 实例化路由
routes = web.RouteTableDef()

# 异步json序列化
def jsondump(func):
    @wraps(func)
    async def wrapper(*args,**kwargs):
        result = await func(*args,**kwargs)
        try:
            return json.dumps(result ,ensure_ascii=False)
        except:
            return result
    return wrapper

# 封装一下web.json_resp
wj = lambda *args,**kwargs: web.json_response(*args,**kwargs)

# 处理OPTIONS和跨域的中间件
@jsondump
async def options_middleware(app, handler):
    async def middleware(request):
        # 记录IP访问
        ip_analyzer.record_ip(request.remote)

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

# 添加新的路由处理IP统计
@routes.get('/ip_stats')
@jsondump
async def get_ip_stats(request):
    """获取IP访问统计信息"""
    try:
        # 获取查询参数
        top_n = request.query.get('top', None)
        if top_n:
            try:
                top_n = int(top_n)
            except ValueError:
                return wj({'code': 400, 'msg': 'Invalid top parameter'}, status=400, headers=corscode)
        
        # 获取统计信息
        stats = ip_analyzer.get_formatted_stats(top_n=top_n)
        return wj({
            'code': 200,
            'msg': 'success',
            'data': stats
        }, headers=corscode)
    except Exception as e:
        api_logger.error(f"获取IP统计失败: {str(e)}")
        return wj({'code': 500, 'msg': 'Internal server error'}, status=500, headers=corscode)

@routes.get('/ip_stats/clear')
@jsondump
async def clear_ip_stats(request):
    """清除IP统计数据"""
    try:
        if ip_analyzer.clear_stats():
            return wj({
                'code': 200,
                'msg': 'IP statistics cleared successfully'
            }, headers=corscode)
        else:
            return wj({
                'code': 500,
                'msg': 'Failed to clear IP statistics'
            }, status=500, headers=corscode)
    except Exception as e:
        api_logger.error(f"清除IP统计失败: {str(e)}")
        return wj({'code': 500, 'msg': 'Internal server error'}, status=500, headers=corscode)
    
@jsondump
@routes.view(r'/query/{path}')
async def geturl(request):
    path = request.match_info['path']

    if path not in appth and path not in bappth:
        return wj({"code":102,"msg":"不是支持的查询类型"})
    
    if request.method == "GET":
        appname = request.query.get("search")
        pageNum = request.query.get("pageNum")
        pageSize = request.query.get("pageSize")
    if request.method == "POST":
        data = await request.json()
        appname = data.get("search")
        pageNum = data.get("pageNum")
        pageSize = data.get("pageSize")

    if not appname:
        return wj({"code":101,"msg":"参数错误,请指定search参数"})
    
    if path in appth:
        return wj(await appth.get(path)(
            appname,
            pageNum if str(pageNum) else '',
            pageSize if str(pageSize) else ''
            ))
    else:
        return wj(await bappth.get(path)(appname))

if __name__ == '__main__':

    myicp = beian()
    appth = {
        "web": myicp.ymWeb,    # 网站
        "app": myicp.ymApp,    # APP
        "mapp": myicp.ymMiniApp,   # 小程序
        "kapp": myicp.ymKuaiApp,    # 快应用
    }
    
    # 违法违规应用不支持翻页
    bappth = {
        "bweb": myicp.bymWeb,    # 违法违规网站
        "bapp": myicp.bymApp,    # 违法违规APP
        "bmapp": myicp.bymMiniApp,   # 违法违规小程序
        "bkapp": myicp.bymKuaiApp    # 违法违规快应用
    }
    app = web.Application()
    app.add_routes(routes)

    app.middlewares.append(options_middleware)
    print('''

            Welcome to the Yiming API : https://api.wer.plus
            Github                    : https://github.com/HG-ha
            Document                  : https://github.com/HG-ha/ICP_Query

    ''')
    web.run_app(
        app,
        host = "0.0.0.0",
        port = 16183
    )