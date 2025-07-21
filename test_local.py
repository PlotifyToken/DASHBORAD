#!/usr/bin/env python3
"""
本地测试脚本 - 在部署前测试API是否工作正常
"""

import os
import sys
import json
from api.data import handler
from http.server import BaseHTTPRequestHandler
from io import StringIO
import unittest

class MockRequest:
    """模拟HTTP请求"""
    def __init__(self):
        self.responses = []
        self.headers = {}
        
    def send_response(self, code):
        self.status_code = code
        
    def send_header(self, key, value):
        self.headers[key] = value
        
    def end_headers(self):
        pass
        
    def wfile_write(self, data):
        self.response_data = data

def test_api():
    """测试API端点"""
    print("🧪 开始测试 UnlockLand Dashboard API...")
    
    # 检查环境变量
    print("\n1️⃣ 检查环境变量...")
    
    customer_io_key = os.environ.get('CUSTOMER_IO_APP_API_KEY')
    revenuecat_key = os.environ.get('REVENUECAT_TOKEN')
    
    if not customer_io_key:
        print("❌ 缺少 CUSTOMER_IO_APP_API_KEY 环境变量")
        print("💡 请设置: export CUSTOMER_IO_APP_API_KEY='你的API密钥'")
        return False
    else:
        print(f"✅ Customer.io API Key: {customer_io_key[:10]}...")
    
    if not revenuecat_key:
        print("❌ 缺少 REVENUECAT_TOKEN 环境变量")
        print("💡 请设置: export REVENUECAT_TOKEN='你的API密钥'")
        return False
    else:
        print(f"✅ RevenueCat Token: {revenuecat_key[:10]}...")
    
    # 创建模拟请求
    print("\n2️⃣ 测试API端点...")
    
    try:
        # 创建处理器实例
        test_handler = handler()
        
        # 模拟wfile属性
        class MockWFile:
            def __init__(self):
                self.data = b''
            def write(self, data):
                self.data = data
        
        test_handler.wfile = MockWFile()
        
        # 模拟请求方法
        original_methods = {}
        
        def mock_send_response(code):
            test_handler.status_code = code
            
        def mock_send_header(key, value):
            if not hasattr(test_handler, 'response_headers'):
                test_handler.response_headers = {}
            test_handler.response_headers[key] = value
            
        def mock_end_headers():
            pass
        
        test_handler.send_response = mock_send_response
        test_handler.send_header = mock_send_header
        test_handler.end_headers = mock_end_headers
        
        # 执行GET请求
        test_handler.do_GET()
        
        # 检查响应
        if hasattr(test_handler, 'status_code'):
            print(f"📊 响应状态码: {test_handler.status_code}")
            
            if test_handler.status_code == 200:
                try:
                    response_data = json.loads(test_handler.wfile.data.decode())
                    print("✅ API响应成功!")
                    print(f"📈 数据预览:")
                    print(f"   总用户: {response_data.get('totalUsers', 'N/A')}")
                    print(f"   ARR: ${response_data.get('arr', 'N/A')}")
                    print(f"   活跃订阅: {response_data.get('activeSubscriptions', 'N/A')}")
                    print(f"   数据源: {response_data.get('sources', {})}")
                    return True
                except json.JSONDecodeError as e:
                    print(f"❌ 响应数据解析失败: {e}")
                    print(f"原始响应: {test_handler.wfile.data}")
                    return False
            else:
                print(f"❌ API返回错误状态码: {test_handler.status_code}")
                if hasattr(test_handler, 'wfile') and test_handler.wfile.data:
                    try:
                        error_data = json.loads(test_handler.wfile.data.decode())
                        print(f"错误信息: {error_data.get('error', '未知错误')}")
                    except:
                        print(f"原始错误响应: {test_handler.wfile.data}")
                return False
        else:
            print("❌ 未收到响应")
            return False
            
    except Exception as e:
        print(f"❌ API测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主函数"""
    print("🚀 UnlockLand Dashboard 本地测试工具")
    print("="*50)
    
    # 检查Python版本
    if sys.version_info < (3, 7):
        print("❌ 需要Python 3.7或更高版本")
        return
    
    print(f"✅ Python版本: {sys.version}")
    
    # 运行测试
    success = test_api()
    
    print("\n" + "="*50)
    if success:
        print("🎉 测试通过！你的API可以正常工作")
        print("💡 现在可以部署到Vercel了")
        print("\n📋 下一步:")
        print("1. 创建GitHub仓库并上传代码")
        print("2. 在Vercel中导入项目")
        print("3. 设置环境变量")
        print("4. 部署完成!")
    else:
        print("❌ 测试失败，请检查配置")
        print("\n🔧 常见解决方案:")
        print("1. 确认API密钥正确")
        print("2. 检查网络连接")
        print("3. 验证API权限")

if __name__ == "__main__":
    main() 