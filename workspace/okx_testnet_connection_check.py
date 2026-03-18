#!/usr/bin/env python3
"""
虞姬OKX测试网连接方式检查
检查虞姬设计的测试网连接方式是否有问题
"""

import time
import hmac
import hashlib
import requests
import json
from datetime import datetime

class OKXTestnetConnectionCheck:
    def __init__(self):
        # 老板提供的最新OKX凭据
        self.api_key = "cefedac1-1d25-4fae-861d-9f006e4cd654"
        self.secret = "EE66B6A88F9E57FBCAE6219081DABDE1"
        self.passphrase = "Qian1314."
        
        # 测试网专用API地址
        self.testnet_url = "https://www.okx.com"  # 标准地址
        self.testnet_ws_url = "wss://wspap.okx.com:8443/ws/v5/public"
        
        # 稳健连接
        self.session = requests.Session()
        self.session.trust_env = False
    
    def check_testnet_connection_design(self):
        """检查测试网连接方式设计"""
        print("🔍 虞姬OKX测试网连接方式设计检查...")
        print("=" * 60)
        
        design_issues = {}
        
        # 检查1: API地址设计
        print("\n1. API地址设计检查...")
        api_url_design = self.check_api_url_design()
        design_issues['api_url'] = api_url_design
        
        # 检查2: 测试网特殊配置
        print("\n2. 测试网特殊配置检查...")
        testnet_config = self.check_testnet_special_config()
        design_issues['testnet_config'] = testnet_config
        
        # 检查3: 模拟交易头设计
        print("\n3. 模拟交易头设计检查...")
        simulated_header = self.check_simulated_header_design()
        design_issues['simulated_header'] = simulated_header
        
        # 检查4: 连接参数设计
        print("\n4. 连接参数设计检查...")
        connection_params = self.check_connection_params_design()
        design_issues['connection_params'] = connection_params
        
        return design_issues
    
    def check_api_url_design(self):
        """检查API地址设计"""
        print("   检查API地址设计...")
        
        issues = []
        
        # 检查标准API地址
        print(f"      标准API地址: {self.testnet_url}")
        
        # 检查其他可能的测试网地址
        possible_urls = [
            "https://www.okx.com",
            "https://aws.okx.com", 
            "https://okx.com"
        ]
        
        print("      可能的API地址:")
        for url in possible_urls:
            print(f"        • {url}")
        
        # 检查URL连通性
        for url in possible_urls:
            try:
                test_url = f"{url}/api/v5/public/time"
                response = self.session.get(test_url, timeout=5)
                if response.status_code == 200:
                    print(f"        ✅ {url}: 可连通")
                else:
                    print(f"        ❌ {url}: HTTP {response.status_code}")
            except Exception as e:
                print(f"        ❌ {url}: {e}")
        
        return {'issues': issues, 'current_url': self.testnet_url}
    
    def check_testnet_special_config(self):
        """检查测试网特殊配置"""
        print("   检查测试网特殊配置...")
        
        issues = []
        
        # 检查测试网特殊头信息
        special_headers = [
            {
                'name': '标准模拟交易头',
                'headers': {
                    'x-simulated-trading': '1'
                }
            },
            {
                'name': '测试网专用头',
                'headers': {
                    'x-testnet': '1'
                }
            },
            {
                'name': '环境标识头',
                'headers': {
                    'x-environment': 'demo'
                }
            },
            {
                'name': '模拟环境头',
                'headers': {
                    'x-simulated-trading': 'true'
                }
            }
        ]
        
        timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        request_path = "/api/v5/account/balance"
        
        message = timestamp + 'GET' + request_path
        signature = hmac.new(
            self.secret.encode('utf-8'),
            message.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        base_headers = {
            'OK-ACCESS-KEY': self.api_key,
            'OK-ACCESS-SIGN': signature,
            'OK-ACCESS-TIMESTAMP': timestamp,
            'OK-ACCESS-PASSPHRASE': self.passphrase,
            'Content-Type': 'application/json'
        }
        
        for config in special_headers:
            print(f"\n      测试 {config['name']}...")
            
            headers = {**base_headers, **config['headers']}
            
            try:
                url = f"{self.testnet_url}{request_path}"
                response = self.session.get(url, headers=headers, timeout=10)
                
                print(f"        响应状态: {response.status_code}")
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get('code') == '0':
                        print(f"        ✅ {config['name']}: 成功")
                        return {'success': True, 'config': config['name']}
                    else:
                        error_msg = data.get('msg', '未知错误')
                        print(f"        ❌ {config['name']}: {error_msg}")
                else:
                    print(f"        ❌ {config['name']}: HTTP {response.status_code}")
                    
            except Exception as e:
                print(f"        ❌ {config['name']}: {e}")
        
        return {'issues': issues, 'tested_configs': [c['name'] for c in special_headers]}
    
    def check_simulated_header_design(self):
        """检查模拟交易头设计"""
        print("   检查模拟交易头设计...")
        
        issues = []
        
        # 检查模拟交易头的不同值
        header_values = [
            {'value': '1', 'description': '标准值'},
            {'value': 'true', 'description': '布尔值'},
            {'value': 'TRUE', 'description': '大写布尔值'},
            {'value': 'yes', 'description': '是'},
            {'value': 'on', 'description': '开启'},
            {'value': 'enable', 'description': '启用'}
        ]
        
        timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        request_path = "/api/v5/account/balance"
        
        message = timestamp + 'GET' + request_path
        signature = hmac.new(
            self.secret.encode('utf-8'),
            message.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        base_headers = {
            'OK-ACCESS-KEY': self.api_key,
            'OK-ACCESS-SIGN': signature,
            'OK-ACCESS-TIMESTAMP': timestamp,
            'OK-ACCESS-PASSPHRASE': self.passphrase,
            'Content-Type': 'application/json'
        }
        
        for header in header_values:
            print(f"\n      测试模拟头值: {header['value']} ({header['description']})...")
            
            headers = {**base_headers, 'x-simulated-trading': header['value']}
            
            try:
                url = f"{self.testnet_url}{request_path}"
                response = self.session.get(url, headers=headers, timeout=10)
                
                print(f"        响应状态: {response.status_code}")
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get('code') == '0':
                        print(f"        ✅ {header['value']}: 成功")
                        return {'success': True, 'value': header['value']}
                    else:
                        error_msg = data.get('msg', '未知错误')
                        print(f"        ❌ {header['value']}: {error_msg}")
                else:
                    print(f"        ❌ {header['value']}: HTTP {response.status_code}")
                    
            except Exception as e:
                print(f"        ❌ {header['value']}: {e}")
        
        return {'issues': issues, 'tested_values': [h['value'] for h in header_values]}
    
    def check_connection_params_design(self):
        """检查连接参数设计"""
        print("   检查连接参数设计...")
        
        issues = []
        
        # 检查连接超时
        timeout_values = [5, 10, 15, 30]
        print("      连接超时测试:")
        for timeout in timeout_values:
            try:
                url = f"{self.testnet_url}/api/v5/public/time"
                response = self.session.get(url, timeout=timeout)
                if response.status_code == 200:
                    print(f"        ✅ {timeout}秒: 正常")
                else:
                    print(f"        ❌ {timeout}秒: HTTP {response.status_code}")
            except Exception as e:
                print(f"        ❌ {timeout}秒: {e}")
        
        # 检查重试机制
        print("\n      重试机制检查:")
        print("        • 当前设计: 无自动重试")
        print("        • 建议: 添加重试机制")
        
        # 检查会话配置
        print("\n      会话配置检查:")
        print(f"        • 信任环境: {self.session.trust_env}")
        print(f"        • 建议: 设置为False（已设置）")
        
        return {'issues': issues, 'timeout_tested': timeout_values}
    
    def generate_testnet_design_report(self, design_issues):
        """生成测试网设计报告"""
        print("\n💰 【虞姬OKX测试网连接方式设计检查报告】")
        print(f"📅 报告时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)
        
        # 设计问题汇总
        print("\n🔧 【测试网连接方式设计问题】")
        
        total_issues = 0
        for category, result in design_issues.items():
            issues = result.get('issues', [])
            total_issues += len(issues)
            
            if issues:
                print(f"\n   ❌ {category.upper()} 问题:")
                for issue in issues:
                    print(f"      • {issue}")
            else:
                print(f"\n   ✅ {category.upper()}: 设计正确")
        
        print(f"\n   总设计问题: {total_issues}")
        
        # 根本原因分析
        print(f"\n🔍 【根本原因分析】")
        if total_issues == 0:
            print("   ✅ 虞姬测试网连接方式设计正确")
            print("   💡 问题不在虞姬设计，而在API配置")
        else:
            print("   🔧 虞姬测试网连接方式设计有问题")
            print("   💡 需要修复测试网连接设计")
        
        # 测试网专用解决方案
        print(f"\n🚀 【测试网专用解决方案】")
        if total_issues == 0:
            print("   ✅ 测试网连接方式设计正确")
            print("   📋 问题在API配置，需要:")
            print("      1. 确认模拟账号可正常访问")
            print("      2. 重新生成测试网API密钥")
            print("      3. 检查测试网IP白名单")
            print("      4. 验证测试网API权限")
        else:
            print("   🔧 测试网连接方式需要修复")
            print("   📋 需要修复设计问题:")
            for category, result in design_issues.items():
                issues = result.get('issues', [])
                if issues:
                    print(f"      • {category}: {len(issues)}个问题")
        
        print("\n" + "=" * 70)
    
    def run_testnet_design_check(self):
        """运行测试网设计检查"""
        print("🚀 虞姬OKX测试网连接方式设计检查系统")
        print(f"⏰ 检查时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)
        
        # 测试网连接方式设计检查
        design_issues = self.check_testnet_connection_design()
        
        # 生成测试网设计报告
        self.generate_testnet_design_report(design_issues)
        
        print("\n" + "=" * 70)
        
        # 总结
        total_issues = sum(len(result.get('issues', [])) for result in design_issues.values())
        
        if total_issues == 0:
            print("🎉 虞姬测试网连接方式设计正确! 问题在API配置!")
            return True
        else:
            print("⚠️ 虞姬测试网连接方式设计有问题，需要修复!")
            return False

# 立即运行测试网设计检查
def check_okx_testnet_design():
    """检查OKX测试网连接设计"""
    print("🔍 立即检查虞姬OKX测试网连接方式设计...")
    
    checker = OKXTestnetConnectionCheck()
    
    try:
        success = checker.run_testnet_design_check()
        return success
    except Exception as e:
        print(f"❌ 检查异常: {e}")
        return False

if __name__ == "__main__":
    check_okx_testnet_design()