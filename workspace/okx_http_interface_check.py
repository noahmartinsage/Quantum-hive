#!/usr/bin/env python3
"""
虞姬OKX HTTP接口正确性检查
验证刚创建的API密钥和HTTP接口配置
"""

import time
import hmac
import hashlib
import requests
import json
from datetime import datetime

class OKXHTTPInterfaceChecker:
    def __init__(self):
        # 新创建的API配置
        self.api_key = "e4753767-b2f7-4495-b2d9-0166238b1076"
        self.secret = "FBBB847F11CC85396F411B1D52E35A1E"
        self.passphrase = "Abc123456"
        
        # OKX API端点
        self.base_urls = [
            "https://www.okx.com",      # 主域名
            "https://aws.okx.com",      # AWS域名
            "https://okx.com"           # 无www域名
        ]
        
        # 稳健连接
        self.session = requests.Session()
        self.session.trust_env = False
    
    def check_all_http_interfaces(self):
        """检查所有HTTP接口"""
        print("🔍 检查OKX所有HTTP接口正确性...")
        print("=" * 60)
        
        interface_results = {}
        
        for base_url in self.base_urls:
            print(f"\n🌐 测试基础URL: {base_url}")
            
            # 测试公开接口
            public_result = self.test_public_interface(base_url)
            
            # 测试私有接口
            private_result = self.test_private_interface(base_url)
            
            interface_results[base_url] = {
                'public': public_result,
                'private': private_result
            }
        
        return interface_results
    
    def test_public_interface(self, base_url):
        """测试公开接口"""
        print("   测试公开接口...")
        
        endpoints = [
            ("/api/v5/public/time", "时间接口"),
            ("/api/v5/public/instruments?instType=SPOT", "交易对接口"),
            ("/api/v5/market/ticker?instId=BTC-USDT", "行情接口")
        ]
        
        results = []
        
        for endpoint, description in endpoints:
            try:
                url = f"{base_url}{endpoint}"
                response = self.session.get(url, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get('code') == '0':
                        print(f"      ✅ {description}: 正常")
                        results.append({'endpoint': endpoint, 'status': '正常', 'error': None})
                    else:
                        error_msg = data.get('msg', '未知错误')
                        print(f"      ❌ {description}: {error_msg}")
                        results.append({'endpoint': endpoint, 'status': '错误', 'error': error_msg})
                else:
                    print(f"      ❌ {description}: HTTP {response.status_code}")
                    results.append({'endpoint': endpoint, 'status': '错误', 'error': f'HTTP {response.status_code}'})
                    
            except Exception as e:
                print(f"      ❌ {description}: {e}")
                results.append({'endpoint': endpoint, 'status': '异常', 'error': str(e)})
        
        return results
    
    def test_private_interface(self, base_url):
        """测试私有接口"""
        print("   测试私有接口...")
        
        endpoints = [
            ("/api/v5/account/balance", "余额查询"),
            ("/api/v5/account/config", "配置查询"),
            ("/api/v5/trade/orders-pending", "挂单查询")
        ]
        
        results = []
        
        for endpoint, description in endpoints:
            try:
                timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
                
                message = timestamp + 'GET' + endpoint
                signature = hmac.new(
                    self.secret.encode('utf-8'),
                    message.encode('utf-8'),
                    hashlib.sha256
                ).hexdigest()
                
                headers = {
                    'OK-ACCESS-KEY': self.api_key,
                    'OK-ACCESS-SIGN': signature,
                    'OK-ACCESS-TIMESTAMP': timestamp,
                    'OK-ACCESS-PASSPHRASE': self.passphrase,
                    'Content-Type': 'application/json'
                }
                
                url = f"{base_url}{endpoint}"
                response = self.session.get(url, headers=headers, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get('code') == '0':
                        print(f"      ✅ {description}: 正常")
                        results.append({'endpoint': endpoint, 'status': '正常', 'error': None})
                    else:
                        error_code = data.get('code')
                        error_msg = data.get('msg')
                        print(f"      ❌ {description}: {error_code} - {error_msg}")
                        results.append({'endpoint': endpoint, 'status': '错误', 'error': f'{error_code} - {error_msg}'})
                else:
                    print(f"      ❌ {description}: HTTP {response.status_code}")
                    if response.status_code == 401:
                        # 详细分析401错误
                        print(f"         🔍 401错误分析:")
                        print(f"            • 检查API密钥是否正确")
                        print(f"            • 检查Secret是否正确")
                        print(f"            • 检查Passphrase是否正确")
                        print(f"            • 检查IP白名单设置")
                    results.append({'endpoint': endpoint, 'status': '错误', 'error': f'HTTP {response.status_code}'})
                    
            except Exception as e:
                print(f"      ❌ {description}: {e}")
                results.append({'endpoint': endpoint, 'status': '异常', 'error': str(e)})
        
        return results
    
    def verify_api_configuration(self):
        """验证API配置"""
        print("\n🔧 验证API配置正确性...")
        
        config_checks = [
            ("API密钥格式", len(self.api_key) == 36, "应为36位UUID格式"),
            ("Secret密钥格式", len(self.secret) == 32, "应为32位十六进制"),
            ("Passphrase长度", len(self.passphrase) >= 6, "至少6位字符"),
            ("API密钥前缀", self.api_key.startswith("e475"), "检查密钥前缀"),
            ("Secret字符集", all(c in '0123456789ABCDEF' for c in self.secret.upper()), "应为十六进制字符")
        ]
        
        for check_name, check_result, expected in config_checks:
            if check_result:
                print(f"   ✅ {check_name}: 正确 {expected}")
            else:
                print(f"   ❌ {check_name}: 错误 {expected}")
    
    def check_common_issues(self):
        """检查常见问题"""
        print("\n🔍 检查常见连接问题...")
        
        common_issues = [
            ("时间戳同步", "确保服务器时间与OKX服务器同步"),
            ("IP白名单", "确认当前服务器IP已添加到白名单"),
            ("API权限", "确认启用交易、查询等权限"),
            ("网络防火墙", "检查防火墙是否阻止API连接"),
            ("DNS解析", "验证OKX域名解析是否正确")
        ]
        
        for issue, solution in common_issues:
            print(f"   ⚠️ {issue}: {solution}")
    
    def generate_interface_report(self, interface_results):
        """生成接口报告"""
        print("\n🌐 【OKX HTTP接口正确性报告】")
        print(f"📅 报告时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)
        
        # 分析接口结果
        working_urls = []
        working_private_urls = []
        
        for base_url, results in interface_results.items():
            public_ok = all(r['status'] == '正常' for r in results['public'])
            private_ok = any(r['status'] == '正常' for r in results['private'])
            
            if public_ok:
                working_urls.append(base_url)
                if private_ok:
                    working_private_urls.append(base_url)
        
        # 接口状态
        print("\n🔗 【HTTP接口状态】")
        if working_urls:
            print("   ✅ 公开接口正常的基础URL:")
            for url in working_urls:
                print(f"      • {url}")
        else:
            print("   ❌ 所有公开接口均失败")
        
        if working_private_urls:
            print("\n   ✅ 私有接口正常的基础URL:")
            for url in working_private_urls:
                print(f"      • {url}")
        else:
            print("\n   ❌ 所有私有接口均认证失败")
        
        # 详细错误分析
        print("\n🔧 【详细错误分析】")
        for base_url, results in interface_results.items():
            private_errors = [r for r in results['private'] if r['status'] != '正常']
            if private_errors:
                print(f"\n   📍 {base_url} 私有接口错误:")
                for error in private_errors[:3]:  # 显示前3个错误
                    print(f"      • {error['endpoint']}: {error['error']}")
        
        # API配置验证
        self.verify_api_configuration()
        
        # 常见问题检查
        self.check_common_issues()
        
        # 解决方案
        print("\n💡 【解决方案】")
        if working_private_urls:
            print("   ✅ HTTP接口正确，可以开始交易")
        else:
            print("   🔧 HTTP接口存在问题，需要修复:")
            print("      1. 确认API密钥刚创建时设置的Passphrase")
            print("      2. 检查OKX后台API权限设置")
            print("      3. 验证IP白名单配置")
            print("      4. 检查服务器时间同步")
    
    def run_complete_interface_check(self):
        """运行完整接口检查"""
        print("🚀 虞姬OKX HTTP接口正确性检查")
        print(f"⏰ 检查时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)
        
        # 检查所有HTTP接口
        interface_results = self.check_all_http_interfaces()
        
        # 生成接口报告
        self.generate_interface_report(interface_results)
        
        print("\n" + "=" * 70)
        
        # 总结
        working_private_urls = []
        for base_url, results in interface_results.items():
            if any(r['status'] == '正常' for r in results['private']):
                working_private_urls.append(base_url)
        
        if working_private_urls:
            print("✅ HTTP接口检查完成! 可以立即开始交易!")
        else:
            print("⚠️ HTTP接口检查失败，需要重新配置API")

# 立即运行接口检查
def check_okx_http_interfaces():
    """检查OKX HTTP接口"""
    print("🔍 立即检查虞姬OKX HTTP接口正确性...")
    
    checker = OKXHTTPInterfaceChecker()
    
    try:
        checker.run_complete_interface_check()
    except Exception as e:
        print(f"❌ 接口检查异常: {e}")

if __name__ == "__main__":
    check_okx_http_interfaces()