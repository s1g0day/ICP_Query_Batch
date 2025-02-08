'''
author     : s1g0day
Creat time : 2024/2/21 14:52
modification time: 2024/8/12 14:58
Remark     : 设置本地代理池，保存验证码图片
'''

import asyncio
import aiohttp
import cv2
import time
import hashlib
import re
import base64
import numpy as np
import ujson
import random
import datetime
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import string
import os
from detnate import detnate
from aiohttp_socks import SocksConnector

class beian():
    def __init__(self):
        self.typj = {
            0:ujson.dumps(
                {'pageNum': '', 'pageSize': '', 'unitName': '',"serviceType":1}
                ), # 网站
            1:ujson.dumps(
                {"pageNum":"","pageSize":"","unitName":'',"serviceType":6}
                ), # APP
            2:ujson.dumps(
                {'pageNum': '', 'pageSize': '', 'unitName': '',"serviceType":7}
                ), # 小程序
            3:ujson.dumps(
                {'pageNum': '', 'pageSize': '', 'unitName': '',"serviceType":8}
                ) # 快应用
        }
        self.btypj = {
            0: ujson.dumps({"domainName":""}),
            1: ujson.dumps({"serviceName":"","serviceType":6}),
            2: ujson.dumps({"serviceName":"","serviceType":7}),
            3: ujson.dumps({"serviceName":"","serviceType":8})
        }
        self.cookie_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36 Edg/101.0.1210.32'}
        self.home = 'https://beian.miit.gov.cn/'
        self.url = 'https://hlwicpfwc.miit.gov.cn/icpproject_query/api/auth'
        # self.getCheckImage = 'https://hlwicpfwc.miit.gov.cn/icpproject_query/api/image/getCheckImage'
        self.getCheckImage = 'https://hlwicpfwc.miit.gov.cn/icpproject_query/api/image/getCheckImagePoint'
        self.checkImage = 'https://hlwicpfwc.miit.gov.cn/icpproject_query/api/image/checkImage'
        # 正常查询
        self.queryByCondition = 'https://hlwicpfwc.miit.gov.cn/icpproject_query/api/icpAbbreviateInfo/queryByCondition'
        # 违法违规域名查询
        self.blackqueryByCondition = 'https://hlwicpfwc.miit.gov.cn/icpproject_query/api/blackListDomain/queryByCondition'
        # 违法违规APP,小程序,快应用
        self.blackappAndMiniByCondition = 'https://hlwicpfwc.miit.gov.cn/icpproject_query/api/blackListDomain/queryByCondition_appAndMini'
        self.det = detnate()
        self.p_uuid = ''

    def generate_random_filename(self, length=8, extension=None):
        if not os.path.exists('temp'):
            os.makedirs('temp')
        letters = string.ascii_lowercase
        random_filename = "temp/" +''.join(random.choice(letters) for _ in range(length))
        if extension != None:
            random_filename += '.' + extension
        return random_filename
    
    async def _init_session(self):
        self.session = aiohttp.ClientSession(connector=SocksConnector.from_url('socks5://127.0.0.1:8443'))
    
    async def _close_session(self):
        if self.session is not None:
            await self.session.close()
    
    async def get_token(self):
        timeStamp = round(time.time()*1000)
        authSecret = 'testtest' + str(timeStamp)
        authKey = hashlib.md5(authSecret.encode(encoding='UTF-8')).hexdigest()
        self.auth_data = {'authKey': authKey, 'timeStamp': timeStamp}
        self.cookie = await self.get_cookie()
        self.base_header = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36 Edg/101.0.1210.32',
                'Origin': 'https://beian.miit.gov.cn',
                'Referer': 'https://beian.miit.gov.cn/',
                'Cookie': f'__jsluid_s={self.cookie}',
                'Accept': 'application/json, text/plain, */*'
            }
        try:
            async with self.session.post(self.url,data=self.auth_data,headers=self.base_header) as req:
                req = await req.text()
                t = ujson.loads(req)
                return t['params']['bussiness']
        except Exception as e:
            return e

    async def get_cookie(self):
        async with self.session.get(self.home,headers=self.cookie_headers) as req:
            jsluid_s = re.compile('[0-9a-z]{32}').search(str(req.cookies))[0]
            return jsluid_s

    # 进行aes加密
    def get_pointJson(self,value,key):
        cipher = AES.new(key.encode(), AES.MODE_ECB)
        ciphertext = cipher.encrypt(pad(ujson.dumps(value).encode(), AES.block_size))
        ciphertext_base64 = base64.b64encode(ciphertext)
        return ciphertext_base64.decode('utf-8')


    # 新增的UID加密生成算法
    def get_clientUid(self):
        characters = "0123456789abcdef"
        unique_id = ['0'] * 36

        for i in range(36):
            unique_id[i] = random.choice(characters)

        unique_id[14] = '4'
        unique_id[19] = characters[(3 & int(unique_id[19], 16)) | 8]
        unique_id[8] = unique_id[13] = unique_id[18] = unique_id[23] = "-"

        point_id = "point-" + ''.join(unique_id)

        return ujson.dumps({"clientUid":point_id})

    async def check_img(self):
        self.token = await self.get_token()
        try:
            data = self.get_clientUid()
            clientUid = ujson.loads(data)["clientUid"]
            length = str(len(str(data).encode('utf-8')))
            self.base_header.update({'Content-Length': length, 'Token': self.token})
            self.base_header['Content-Type'] = 'application/json'
 
            async with self.session.post(self.getCheckImage,data=data,headers=self.base_header) as req:
                res = await req.json()
                self.p_uuid = res['params']['uuid']
                big_image = res['params']['bigImage']
                small_image = res['params']['smallImage']
                self.secretKey = res['params']['secretKey']
                self.wordCount = res['params']['wordCount']
                selice_small = await self.small_selice(small_image,big_image)
            
            pointJson = self.get_pointJson(selice_small,self.secretKey)
            data = ujson.loads(ujson.dumps({"token":self.p_uuid,
                    "secretKey":self.secretKey,
                    "clientUid":clientUid,
                    "pointJson":pointJson}))
            length = str(len(str(data).encode('utf-8')))
            self.base_header.update({'Content-Length': length})
            async with self.session.post(self.checkImage,
                    json=data,headers=self.base_header) as req:
                res = await req.text()
                data = ujson.loads(res)
                if data["success"] == False:
                    return 'verf error'
                else:
                    return data["params"]["sign"]
        except Exception as e:
            return False

    async def small_selice(self,small_image,big_image):
        isma = cv2.imdecode(np.frombuffer(base64.b64decode(small_image),np.uint8), cv2.COLOR_GRAY2RGB)
        isma = cv2.cvtColor(isma, cv2.COLOR_BGRA2BGR)
        ibig = cv2.imdecode(np.frombuffer(base64.b64decode(big_image),np.uint8), cv2.COLOR_GRAY2RGB)
        data = self.det.check_target(ibig,isma)

        # 生成时间戳
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        
        # 创建保存图像的目录
        output_dir = "output"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        isma_dir = os.path.join(output_dir, "isma")
        if not os.path.exists(isma_dir):
            os.makedirs(isma_dir)
        ibig_dir = os.path.join(output_dir, "ibig")
        if not os.path.exists(ibig_dir):
            os.makedirs(ibig_dir)
        
        # 保存图像
        isma_filename = f"{timestamp}_small.jpg"
        isma_filepath = os.path.join(isma_dir, isma_filename)
        cv2.imwrite(isma_filepath, isma)  # 保存带时间戳的小图像
        ibig_filename = f"{timestamp}_big.jpg"
        ibig_filepath = os.path.join(ibig_dir, ibig_filename)
        cv2.imwrite(ibig_filepath, ibig)  # 保存带时间戳的大图像
        return data
        

    async def getbeian(self,name,sp,pageNum,pageSize,):
        info = ujson.loads(self.typj.get(sp))
        info['pageNum'] = pageNum
        info['pageSize'] = pageSize
        info['unitName'] = name
        sign = await self.check_img()
        if sign == 'verf error':
            return {'code':201,'error':'验证码识别失败'}
        length = str(len(str(ujson.dumps(info,ensure_ascii=False)).encode('utf-8')))
        self.base_header.update({'Content-Length': length, 'Uuid': self.p_uuid, 'Token': self.token, 'Sign': sign})
        async with self.session.post(self.queryByCondition, data=ujson.dumps(info,ensure_ascii=False), headers=self.base_header) as req:
            res = await req.text()
            return ujson.loads(res)
        
    async def getblackbeian(self,name,sp):
        info = ujson.loads(self.btypj.get(sp))
        if sp == 0:
            info['domainName'] = name
        else:
            info['serviceName'] = name
        sign = await self.check_img()
        if sign == 'verf error':
            return {'code':201,'error':'验证码识别失败'}
        length = str(len(str(ujson.dumps(info,ensure_ascii=False)).encode('utf-8')))
        self.base_header.update({'Content-Length': length, 'Uuid': self.p_uuid, 'Token': self.token, 'Sign': sign})
        async with self.session.post(
            self.blackqueryByCondition if sp == 0 else self.blackappAndMiniByCondition, 
                                     data=ujson.dumps(info,ensure_ascii=False), 
                                     headers=self.base_header) as req:
            res = await req.text()
            return ujson.loads(res)

    async def autoget(self,name,sp,pageNum='',pageSize='',b=1):
        await self._init_session()
        try:
            data = await self.getbeian(name,sp,pageNum,pageSize) if b == 1 else await self.getblackbeian(name,sp)
        except Exception as e:
            return {"code":122,"msg":"查询失败"}
        finally:
            await self._close_session()

        if data['code'] == 500:
            return {"code":122,"msg":"工信部服务器异常"}
        return data

    # APP备案查询
    async def ymApp(self,name,pageNum='',pageSize=''):
        return await self.autoget(name,1,pageNum,pageSize)

    # 网站备案查询
    async def ymWeb(self,name,pageNum='',pageSize=''):
        return await self.autoget(name,0,pageNum,pageSize)

    # 小程序备案查询
    async def ymMiniApp(self,name,pageNum='',pageSize=''):
        return await self.autoget(name,2,pageNum,pageSize)

    # 快应用备案查询
    async def ymKuaiApp(self,name,pageNum='',pageSize=''):
        return await self.autoget(name,3,pageNum,pageSize)
    
    # 违法违规APP查询
    async def bymApp(self,name):
        return await self.autoget(name,1,b=0)

    # 违法违规网站查询
    async def bymWeb(self,name):
        return await self.autoget(name,0,b=0)

    # 违法违规小程序查询
    async def bymMiniApp(self,name):
        return await self.autoget(name,2,b=0)

    # 违法违规快应用查询
    async def bymKuaiApp(self,name):
        return await self.autoget(name,3,b=0)

if __name__ == '__main__':
    async def main():
        a = beian()
        # 官方单页查询pageSize最大支持26
        # 页面索引pageNum从1开始,第一页可以不写
        data = await a.ymWeb("qq.com")
        print(f"查询结果：\n{data}")
        return data
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

    '''
    在其他代码模块中调用（异步）

        from ymicp import beian

        icp = beian()
        data = await icp.ymApp("微信")
    
    '''