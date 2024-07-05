import sys
import openpyxl

# 创建一个新的Excel工作簿
workbook = openpyxl.Workbook()
# 获取默认的活动工作表
worksheet = workbook.active

with open(sys.argv[1], 'r', encoding='utf-8') as fileread:
    fileread = fileread.readlines()
    for i in fileread:
        if i != "\n":
            task_parts = i.strip().split('\t')
            # 创建空字典
            task_dict = {}

            # 遍历任务信息部分
            for part in task_parts:
                # 分割键值对
                key, value = part.split(':')
                # 添加到字典
                task_dict[key] = value

            # 输出到Excel行
            worksheet.append([task_dict['domainId'], task_dict['unitName'], task_dict['domain'], task_dict['serviceLicence']])

# 保存Excel文件
workbook.save('output.xlsx')
