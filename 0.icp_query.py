'''
Author     : S1g0day
Creat time : 2024/3/15 17:27
Modification time: 2024/8/8 18:00
Introduce  : 通过接口查询域名或公司备案
'''
import os
import yaml
from lib.logo import logo
from datetime import datetime
from lib.Requests_func import make_request
from argparse import ArgumentParser

# def Page_traversal(pages, req_unitName, params, query_url, req_list):
#     # 原函数，通过分页处理。但分页查询存在数据重复问题
#     domainId_list = []
#     for page in range(1, pages + 1):
#         if page == 1:
#             unitName_list = req_unitName['params']['list']
#             print(f"Planned speed: {page}/{pages}")
#         else:
#             params['pageNum'] = page
#             req_page_unitName = make_request(query_url, params, req_list[0]['unitName'])
#             unitName_list = req_page_unitName['params']['list']
#             print(f"{page}/{pages}")
#         if unitName_list:
#             for item in unitName_list:
#                 if item.get('domain') and item.get('unitName'):
#                     output = f"unitName:{item['unitName']}\tdomainId:{item['domainId']}\tmainLicence:{item['mainLicence']}\tserviceLicence:{item['serviceLicence']}\tdomain:{item['domain']}\tnatureName:{item['natureName']}\tupdateRecordTime:{item['updateRecordTime']}"
#                     print(output)
#                     if item['domainId'] and item['domainId'] not in domainId_list:
#                         domainId_list.append(item['domainId'])
#                         open('log/success.log', 'a+', encoding='utf-8').write(f"\n{output}")
#                 else:
#                     print("unitName or domain is None...")
#         else:
#             print(f"No unitName_list found for {req_list}. Skipping...")
#     return domainId_list

# 检查要写入的内容是否已存在于文件中
def is_output_in_log(log_file_path, output):

    if not os.path.exists(log_file_path):
        with open(log_file_path, 'a+', encoding='utf-8'):
            pass

    with open(log_file_path, 'r', encoding='utf-8') as log_file:
        log_contents = log_file.read()
        return output in log_contents
    
def Page_traversal_temporary(total, params, query_url, req_list):
    # 一页显示所有数据
    domainId_list = []
    params['pageSize'] = total
    req_page_unitName = make_request(query_url, params, req_list[0]['unitName'])
    unitName_list = req_page_unitName['params']['list']

    if unitName_list:
        for item in unitName_list:
            if item.get('domain') and item.get('unitName'):
                success_output = f"domainId:{item['domainId']}\tunitName:{item['unitName']}\tnatureName:{item['natureName']}\tdomain:{item['domain']}\tmainLicence:{item['mainLicence']}\tserviceLicence:{item['serviceLicence']}\tupdateRecordTime:{item['updateRecordTime']}"
                print(success_output)
                
                if item['domainId'] and item['domainId'] not in domainId_list:

                    domainId_list.append(item['domainId'])
                    success_log_file_path = 'log/success.log'

                    if not is_output_in_log(success_log_file_path, success_output):
                        open(success_log_file_path, 'a+', encoding='utf-8').write(f"\n{success_output}")
            else:
                print("unitName or domain is None...")
    else:
        print(f"No unitName_list found for {req_list}. Skipping...")
    return domainId_list

def query_from(query_url, search_data, page_Num=1):
    params = {
        'search': search_data,
        'pageNum': page_Num,
        'pageSize': '10',
    }
    req = make_request(query_url, params, search_data)
    req_list = req['params']['list']
    if req_list:
        params['search'] = req_list[0]['unitName']
        req_unitName = make_request(query_url, params, params['search'])
        # pages = req_unitName['params']['pages']
        # domain_list = Page_traversal(pages, req_unitName, params, query_url, req_list)

        total = req_unitName['params']['total']
        domain_list = Page_traversal_temporary(total, params, query_url, req_list)

        if total != len(domain_list):
            print(f"\nsearch_data:{search_data}, messages:备案提取异常,已输出 error_icp.log , 需手工确认")

            error_icp_output = f"{search_data} 应提取出 {total} 条信息，实际为 {len(domain_list)} 条"
            error_icp_log_file_path = 'log/error_icp.log'

            if not is_output_in_log(error_icp_log_file_path, error_icp_output):
                open(error_icp_log_file_path, 'a+', encoding='utf-8').write(f'{error_icp_output}\n')

        return total
    else:
        print(f"No req_list found for {search_data}. Skipping...")
        no_req_list_file_path = 'log/no_req_list.log'

        if not is_output_in_log(no_req_list_file_path, search_data):
            open(no_req_list_file_path, 'a+', encoding='utf-8').write(f"{search_data}\n")

        return None

def query_from_file(query_url, filename, start_index):
    with open(filename, 'r', encoding='utf-8') as file:
        data_list = file.readlines()
        total_domains = len(data_list)
    if start_index < 1:
        start_index = 1
        print("输入异常, start_index 重置为 1")
    elif start_index > total_domains:
        start_index = total_domains
        print(f"输入异常, start_index 重置为 {total_domains}")
        
    for index in range(start_index-1, total_domains):
        data = data_list[index].strip()
        
        if data:
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
            processing_Domain_output = f'Time: {current_time}, Schedule: {index+1}/{total_domains}, Domain: {data}'
            print(f"\nProcessing {processing_Domain_output}\n")
            
            total = query_from(query_url, data)
            if total is not None:
                processing_Domain_output += f', Total: {total}'
                processing_Domain_file_path = 'log/processing_Domain.log'

                if not is_output_in_log(processing_Domain_file_path, processing_Domain_output):
                    open(processing_Domain_file_path, 'a+', encoding='utf-8').write(f"{processing_Domain_output}\n")            

if __name__ == '__main__':
    logo()
    parser = ArgumentParser()
    parser.add_argument("-d", dest="query_url", help="请输入测试平台地址")
    parser.add_argument("-u", dest="domain", help="请输入目标")
    parser.add_argument("-uf", dest="domains_file", help="请输入目标文件")
    parser.add_argument("-s", dest="start_index", type=int, default="1", help="请输入起始位置，第一个数据的下标为0")
    args = parser.parse_args()

    # Load YAML configuration
    push_config = yaml.safe_load(open("config/config.yaml", "r", encoding="utf-8").read())

    if args.query_url:
        if args.domain:
            # 执行查询
            query_from(args.query_url, args.domain)
        elif args.domains_file:
            print(f"Query_urls: {args.query_url}\nDomains_file: {args.domains_file}")
            query_from_file(args.query_url, args.domains_file, args.start_index)
        else:
            print(f"Query_urls: {args.query_url}\nDomains_file: {push_config['domains_file']}")
            query_from_file(args.query_url, push_config['domains_file'], args.start_index)
            
    else:
        if args.domain:
            # 执行查询
            query_from(push_config['query_url'], args.domain)
        elif args.domains_file:
            print(f"Query_urls: {push_config['query_url']}\nDomains_file: {args.domains_file}")
            query_from_file(push_config['query_url'], args.domains_file, args.start_index)
        else:
            print(f"Query_urls: {push_config['query_url']}\nDomains_file: {push_config['domains_file']}")
            query_from_file(push_config['query_url'], push_config['domains_file'], args.start_index)
