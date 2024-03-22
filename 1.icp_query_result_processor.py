'''
# 处理0.icq_query.py 的结果 output.log

output.log内容格式:

unitName:郑州誉品电子商务有限公司, domain:jinriyupin.com
unitName:郑州誉品电子商务有限公司, domain:yupin360.com
'''
import sys
with open(sys.argv[1], 'r', encoding='utf-8') as fileread:
    fileread = fileread.readlines()
    for i in fileread:
        task_parts = i.strip().split(', ')
        # 创建空字典
        task_dict = {}

        # 遍历任务信息部分
        for part in task_parts:
            # 分割键值对
            key, value = part.split(':')
            # 添加到字典
            task_dict[key] = value
        # 打印字典
        print(task_dict['domain'])