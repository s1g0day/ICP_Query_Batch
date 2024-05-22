## 输出日志

```
.
├── Processing_Domain.log		# 进度日志，如果Ctrl+c中断的话，可以从这里看到定义起始位置
├── error.log					# 报错日志，代码初期调试用的(可忽略)
├── error_Max.log				# 关键日志, 代码中对domains中的每行数据最多遍历10次，如果10次都查询错误，会写入到这个日志，方便对其重新测试
├── error_status_code.log		# 报错日志, 测试平台地址请求失败日志(可忽略)，通过error_Max.log查询失败的记录
├── no_req_list.log				# 关键日志，存储了查询正常但没有数据回显的情况，需要注意是否是domians信息填错，如公司名称为简写等
└── success.log					# 关键日志, 查询成功且获取到所有备案域名信息
```

`quchong.py`日志

```
.
├── _output_ips.txt				# 筛选出所有IP并将其排序后的结果
├── _output_ascii_domain.txt	# 筛选出所有中文域名并将其转为ascii的结果
└── _output_all.txt				# 所有域名及IP结果，其中中文域名及转换结果已打印在输出行，并未写入当前日志
```

