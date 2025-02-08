'''
author     : s1g0day
Creat time : 2024/2/21 14:52
modification time: 2025/2/7 17:30
Remark     : Powered by cursor AI
'''

import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler

class Logger:
    def __init__(self, log_dir='logs'):
        self.log_dir = log_dir
        self.current_date = datetime.now().strftime('%Y-%m-%d')
        self.log_file = os.path.join(log_dir, f'api_{self.current_date}.log')
        self.logger = None
        self.formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        self._setup_logger()
    
    def _ensure_log_directory(self):
        """确保日志目录存在"""
        try:
            if not os.path.exists(self.log_dir):
                os.makedirs(self.log_dir, exist_ok=True)
                print(f"Created log directory: {self.log_dir}")
            return True
        except Exception as e:
            print(f"Error creating log directory: {str(e)}")
            return False
    
    def _ensure_log_file(self):
        """确保日志文件存在且可写"""
        try:
            # 强制创建目录
            self._ensure_log_directory()
            
            # 尝试以追加模式打开文件，如果不存在则创建
            with open(self.log_file, 'a', encoding='utf-8') as f:
                if os.path.getsize(self.log_file) == 0:
                    f.write(f"Log file created at {datetime.now()}\n")
            return True
        except Exception as e:
            print(f"Error handling log file: {str(e)}")
            return False
    
    def _setup_logger(self):
        """初始化logger"""
        if self.logger is None:
            self.logger = logging.getLogger('APILogger')
            self.logger.setLevel(logging.INFO)
        
        # 清除所有现有的处理器
        self.logger.handlers = []
        
        # 添加控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(self.formatter)
        self.logger.addHandler(console_handler)
    
    def _get_file_handler(self):
        """获取文件处理器"""
        try:
            # 确保文件存在
            if not self._ensure_log_file():
                return None
            
            file_handler = RotatingFileHandler(
                self.log_file,
                maxBytes=10*1024*1024,  # 10MB
                backupCount=10,
                encoding='utf-8'
            )
            file_handler.setFormatter(self.formatter)
            return file_handler
        except Exception as e:
            print(f"Error creating file handler: {str(e)}")
            return None
    
    def _write_log(self, level, message):
        """写入日志的核心方法"""
        try:
            # 检查日期变更
            current_date = datetime.now().strftime('%Y-%m-%d')
            if current_date != self.current_date:
                self.current_date = current_date
                self.log_file = os.path.join(self.log_dir, f'api_{self.current_date}.log')
            
            # 重新设置logger
            self._setup_logger()
            
            # 尝试添加文件处理器
            file_handler = self._get_file_handler()
            if file_handler:
                self.logger.addHandler(file_handler)
            
            # 写入日志
            if level == 'INFO':
                self.logger.info(message)
            elif level == 'ERROR':
                self.logger.error(message)
            elif level == 'WARNING':
                self.logger.warning(message)
            elif level == 'DEBUG':
                self.logger.debug(message)
            
            # 如果有文件处理器，用完后移除
            if file_handler:
                self.logger.removeHandler(file_handler)
                file_handler.close()
                
        except Exception as e:
            print(f"Error writing log: {str(e)}")
            # 确保至少在控制台输出日志
            print(f"{datetime.now()} - {level} - {message}")
    
    def info(self, message):
        """记录信息级别的日志"""
        self._write_log('INFO', message)
    
    def error(self, message):
        """记录错误级别的日志"""
        self._write_log('ERROR', message)
    
    def warning(self, message):
        """记录警告级别的日志"""
        self._write_log('WARNING', message)
    
    def debug(self, message):
        """记录调试级别的日志"""
        self._write_log('DEBUG', message)
    
    def log_request(self, request, status_code, message=''):
        """记录API请求信息"""
        log_message = (
            f"{message}: {request.remote} | "
            f"Method: {request.method} | "
            f"Path: {request.path} | "
            f"Status: {status_code} | "
            f"User-Agent: {request.headers.get('User-Agent', 'Unknown')} | "
        )
        self._write_log('INFO', log_message)

# 创建全局logger实例
api_logger = Logger()

# 使用示例
if __name__ == '__main__':
    # 测试日志记录
    api_logger.info("测试信息日志")
    api_logger.error("测试错误日志")
    api_logger.warning("测试警告日志")
    api_logger.debug("测试调试日志")