'''
author     : s1g0day
Creat time : 2024/2/21 14:52
modification time: 2025/2/8 9:30
Remark     : Powered by cursor AI
'''

import os
import json
from datetime import datetime
from collections import defaultdict




class IPAnalyzer:
    def __init__(self, log_dir='logs'):
        self.log_dir = log_dir
        self.current_date = datetime.now().strftime('%Y-%m-%d')
        self.stats_file = os.path.join(log_dir, f'ip_stats_{self.current_date}.json')
        self.ip_counts = defaultdict(int)
        self._ensure_stats_file()
        self.load_stats()
    
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
    
    def _ensure_stats_file(self):
        """确保统计文件存在且可写"""
        try:
            # 确保目录存在
            self._ensure_log_directory()
            
            # 检查文件是否存在
            if not os.path.exists(self.stats_file):
                # 创建新文件
                with open(self.stats_file, 'w', encoding='utf-8') as f:
                    json.dump({}, f)
                print(f"Created stats file: {self.stats_file}")
            return True
        except Exception as e:
            print(f"Error handling stats file: {str(e)}")
            return False
    
    def _check_date(self):
        """检查是否需要更新统计文件（新的一天）"""
        current_date = datetime.now().strftime('%Y-%m-%d')
        if current_date != self.current_date:
            # 保存当前统计数据
            self.save_stats()
            
            # 更新日期和文件路径
            self.current_date = current_date
            self.stats_file = os.path.join(self.log_dir, f'ip_stats_{self.current_date}.json')
            
            # 重置统计数据
            self.ip_counts.clear()
            
            # 确保新的统计文件存在
            self._ensure_stats_file()
            return True
        return False
    
    def load_stats(self):
        """加载统计数据"""
        try:
            if os.path.exists(self.stats_file):
                with open(self.stats_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.ip_counts = defaultdict(int, data)
        except Exception as e:
            print(f"Error loading IP stats: {str(e)}")
            self.ip_counts = defaultdict(int)
    
    def save_stats(self):
        """保存统计数据"""
        try:
            self._ensure_stats_file()
            with open(self.stats_file, 'w', encoding='utf-8') as f:
                json.dump(dict(self.ip_counts), f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving IP stats: {str(e)}")
    
    def record_ip(self, ip):
        """记录IP访问"""
        try:
            # 检查日期变更
            self._check_date()
            
            # 确保文件存在
            self._ensure_stats_file()
            
            # 更新计数
            self.ip_counts[ip] += 1
            
            # 保存统计
            self.save_stats()
            return True
        except Exception as e:
            print(f"Error recording IP {ip}: {str(e)}")
            return False
    
    def get_ip_stats(self, top_n=None):
        """获取IP统计信息"""
        try:
            # 检查文件和加载数据
            self._ensure_stats_file()
            self.load_stats()
            
            # 排序统计数据
            sorted_ips = sorted(self.ip_counts.items(), key=lambda x: x[1], reverse=True)
            if top_n:
                sorted_ips = sorted_ips[:top_n]
            return dict(sorted_ips)
        except Exception as e:
            print(f"Error getting IP stats: {str(e)}")
            return {}
    
    def get_formatted_stats(self, top_n=None):
        """获取格式化的统计信息，返回JSON格式"""
        try:
            stats = self.get_ip_stats(top_n)
            if not stats:
                return {
                    "date": self.current_date,
                    "total_ips": 0,
                    "statistics": []
                }
            
            # 计算总访问次数
            total_visits = sum(stats.values())
            
            # 构建JSON格式的统计数据
            result = {
                "date": self.current_date,
                "total_ips": len(stats),
                "total_visits": total_visits,
                "statistics": [
                    {
                        "ip": ip,
                        "count": count,
                        "percentage": f"{round((count / total_visits) * 100, 2)}%"
                    }
                    for ip, count in stats.items()
                ]
            }
            return result
            
        except Exception as e:
            print(f"Error formatting IP stats: {str(e)}")
            return {
                "date": self.current_date,
                "total_ips": 0,
                "statistics": [],
                "error": str(e)
            }
    
    def clear_stats(self):
        """清除统计数据"""
        try:
            self.ip_counts.clear()
            self.save_stats()
            return True
        except Exception as e:
            print(f"Error clearing IP stats: {str(e)}")
            return False

# 创建全局实例
ip_analyzer = IPAnalyzer()

# 使用示例
if __name__ == '__main__':
    # 测试代码
    test_ips = ['192.168.1.1', '192.168.1.2', '192.168.1.1', '192.168.1.3']
    
    print("记录测试IP...")
    for ip in test_ips:
        ip_analyzer.record_ip(ip)
    
    print("\n所有IP统计：")
    print(ip_analyzer.get_formatted_stats())
    
    print("\n访问最多的2个IP：")
    print(ip_analyzer.get_formatted_stats(top_n=2))