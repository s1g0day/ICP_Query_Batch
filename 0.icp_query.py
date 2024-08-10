'''
Author     : S1g0day
Creat time : 2024/3/15 17:27
Modification time: 2024/8/10 14:48
Introduce  : 通过接口查询域名或公司备案
'''
import yaml
from datetime import datetime
from argparse import ArgumentParser
from lib.logo import logo
from lib.Requests_func import make_request
from lib.log_functions import is_output_in_log, write_log_success, write_log_error, write_log_warning

def Page_traversal_temporary(id, total, params, query_url, req_list):
    # 一页显示所有数据
    domainId_list = []
    params['pageSize'] = total
    req_page_unitName = make_request(query_url, params, req_list[0]['unitName'])

    if req_page_unitName:
        unitName_list = req_page_unitName['params']['list']
        for item in unitName_list:
            if item.get('domain') and item.get('unitName'):
                success_output = f"id:{id}\tdomainId:{item['domainId']}\tunitName:{item['unitName']}\tnatureName:{item['natureName']}\tdomain:{item['domain']}\tmainLicence:{item['mainLicence']}\tserviceLicence:{item['serviceLicence']}\tupdateRecordTime:{item['updateRecordTime']}"
                
                if item['domainId'] and item['domainId'] not in domainId_list:

                    domainId_list.append(item['domainId'])
                    success_log_file_path = 'log/success.log'
                    write_log_success(success_log_file_path, success_output)
            else:
                write_log_warning("unitName or domain is None...")
    else:
        write_log_warning(f"No unitName_list found for {req_list}. Skipping...")
    return domainId_list

def query_from(query_url, search_data, id):

    params = {
        'search': search_data,
        'pageNum': 1,
        'pageSize': 10,
    }

    req = make_request(query_url, params, search_data)
    
    # 检查req是否为字典类型或是否包含所需的键
    if req and isinstance(req, dict) and 'params' in req:
        try:
            req_list = req['params']['list']
            if req_list and isinstance(req_list, list) and len(req_list) > 0:
                params['search'] = req_list[0]['unitName']
                req_unitName = make_request(query_url, params, params['search'])
                if req_unitName and isinstance(req_unitName, dict) and 'params' in req_unitName:
                    total = req_unitName['params']['total']
                    domain_list = Page_traversal_temporary(id, total, params, query_url, req_list)

                    if domain_list and isinstance(domain_list, list) and total != len(domain_list):
                        error_icp_output = f"{search_data} 应提取出 {total} 条信息，实际为 {len(domain_list)} 条"
                        error_icp_log_file_path = 'log/error_icp.log'
                        write_log_error(error_icp_log_file_path, error_icp_output)
                    return total

        except Exception as e:
            error_occurred_output = f"{search_data} an error occurred: {str(e)}"
            error_occurred_log_file_path = 'log/error_occurred.log'
            write_log_error(error_occurred_log_file_path, error_occurred_output, search_data)
    
    no_req_list_output = f"Does not have req_list: {search_data}"
    no_req_list_log_file_path = 'log/no_req_list.log'
    write_log_error(no_req_list_log_file_path, no_req_list_output, search_data)

    # 根据您的需求，如果if条件不满足，最多重新运行10次
    return None

def query_from_file(query_url, filename, start_index):
    with open(filename, 'r', encoding='utf-8') as file:
        data_list = file.readlines()
        total_domains = len(data_list)
    if start_index < 1:
        start_index = 1
        write_log_warning("输入异常, start_index 重置为 1")
    elif start_index > total_domains:
        start_index = total_domains
        write_log_warning(f"输入异常, start_index 重置为 {total_domains}")
        
    for index in range(start_index-1, total_domains):
        data = data_list[index].strip()
        
        if data:
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
            Processing_Domain_output = f'Time: {current_time}, Schedule: {index+1}/{total_domains}, Domain: {data}'
            print("\n")
            write_log_warning(f"Processing {Processing_Domain_output}")
            print("\n")
            total = query_from(query_url, data, index+1)
            if total is not None:
                Processing_Domain_output += f', Total: {total}'
                Processing_Domain_log_file_path = 'log/processing_Domain.log'
                write_log_success(Processing_Domain_log_file_path, Processing_Domain_output)       

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
            query_from(args.query_url, args.domain, args.start_index)
        elif args.domains_file:
            write_log_warning(f"Query_urls: {args.query_url}")
            write_log_warning(f"Domains_file: {args.domains_file}")
            query_from_file(args.query_url, args.domains_file, args.start_index)
        else:
            write_log_warning(f"Query_urls: {args.query_url}")
            write_log_warning(f"Domains_file: {push_config['domains_file']}")
            query_from_file(args.query_url, push_config['domains_file'], args.start_index)
            
    else:
        if args.domain:
            # 执行查询
            query_from(push_config['query_url'], args.domain, args.start_index)
        elif args.domains_file:
            write_log_warning(f"Query_urls: {push_config['query_url']}")
            write_log_warning(f"Domains_file: {args.domains_file}")
            query_from_file(push_config['query_url'], args.domains_file, args.start_index)
        else:
            write_log_warning(f"Query_urls: {push_config['query_url']}")
            write_log_warning(f"Domains_file: {push_config['domains_file']}")
            query_from_file(push_config['query_url'], push_config['domains_file'], args.start_index)
