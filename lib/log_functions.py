import os
import logging

# 打开日志文件并指定编码方式
log_file = open('log/application.log', mode='a', encoding='utf-8')

# 配置日志记录器
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', stream=log_file)

# 创建日志记录器
logger = logging.getLogger(__name__)

# 检查要写入的内容是否已存在于文件中
def is_output_in_log(log_file_path, output):

    if not os.path.exists(log_file_path):
        with open(log_file_path, 'a+', encoding='utf-8'):
            pass

    with open(log_file_path, 'r', encoding='utf-8') as log_file:
        log_contents = log_file.read()
        return output in log_contents

# 写入成功日志
def write_log_success(log_file_path, success_output):
    if "Schedule" not in log_file_path:
        print(success_output)
    if not is_output_in_log(log_file_path, success_output):
        with open(log_file_path, 'ab') as log_file:
            log_file.write(success_output.encode('utf-8') + b'\n')
        logger.info(success_output)

# 写入错误日志
def write_log_error(log_file_path, error_output, search_data=''):
    print(error_output)
    if search_data:
        output = search_data
    else:
        output = error_output
        # print(search_data)
    if not is_output_in_log(log_file_path, output):
        with open(log_file_path, 'ab') as log_file:
            log_file.write(output.encode('utf-8') + b'\n')
        logger.error(error_output)

# 写入警告日志
def write_log_warning(warning_output):
    print(warning_output)
    logger.warning(warning_output)
