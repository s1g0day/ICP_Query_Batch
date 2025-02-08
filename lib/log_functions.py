import os
import logging
from datetime import datetime

class APILogger:
    def __init__(self, log_dir='log'):
        # 确保日志目录存在
        self.log_dir = log_dir
        os.makedirs(log_dir, exist_ok=True)
        
        # 配置主日志文件
        log_file = os.path.join(log_dir, 'application.log')
        self.file_handler = logging.FileHandler(log_file, encoding='utf-8')
        self.file_handler.setFormatter(
            logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        )
        
        # 配置日志记录器
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(self.file_handler)
    
    def _write_to_specific_log(self, log_path, content):
        """写入特定的日志文件"""
        if not self._is_content_in_log(log_path, content):
            with open(log_path, 'a', encoding='utf-8') as f:
                f.write(content + '\n')
    
    def _is_content_in_log(self, log_path, content):
        """检查内容是否已存在于日志文件中"""
        if not os.path.exists(log_path):
            return False
        
        try:
            with open(log_path, 'r', encoding='utf-8') as f:
                return content in f.read()
        except Exception:
            return False
    
    def info(self, message):
        """记录信息日志"""
        print(message)
        self.logger.info(message)
    
    def error(self, message):
        """记录错误日志"""
        print(message)
        self.logger.error(message)
    
    def warning(self, message):
        """记录警告日志"""
        print(message)
        self.logger.warning(message)
    
    def success(self, message, log_file='success.log'):
        """记录成功日志"""
        if 'Schedule' not in message:
            print(message)
        log_path = os.path.join(self.log_dir, log_file)
        self._write_to_specific_log(log_path, message)
        self.logger.info(message)
    
    # 为了保持向后兼容，保留原有的函数接口
    def write_log_success(self, log_file_path, success_output):
        api_logger.success(success_output, os.path.basename(log_file_path))

    def write_log_error(self, log_file_path, error_output, search_data=''):
        output = search_data if search_data else error_output
        api_logger.error(error_output)
        if log_file_path:
            api_logger._write_to_specific_log(log_file_path, output)

    def write_log_warning(self, warning_output):
        api_logger.warning(warning_output)

# 创建全局logger实例
api_logger = APILogger()

