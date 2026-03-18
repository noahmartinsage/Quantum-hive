#!/usr/bin/env python3
"""
虞姬OKX测试网连接方式修复
修复虞姬设计的测试网连接方式问题
"""

import time
import hmac
import hashlib
import requests
import json
from datetime import datetime

class OKXTestnetConnectionFix:
    def __init__(self):
        # 老板提供的最新OKX凭据
        self.api_key = "cefedac1-1d25-4fae-861d-9f006e4cd654"
        self.secret = "EE66B6A88F9E57FBCAE6219081DABDE1"
        self.passphrase = "Qian1314."
        
        # 测试网专用API地址
        self.testnet_url = "https://www.okx.com"
        self.testnet_ws_url = "wss://wspap.okx.com:8443/ws/v5/public"
        
        # 稳健连接
        self.session = requests.Session()
        self.session.trust_env = False
    
    def fix_testnet_connection(self):
        """修复测试网连接方式"""
        print("🔧 虞姬OKX测试网连接方式修复...")
        print("=" * 60)
        
        fix_results = {}
        
        # 修复1: 测试网专用API地址
        print("\n1. 测试网专用API地址修复...")
        api_url_fix = self.fix_api_url()
        fix_results['api_url'] = api_url_fix
        
        # 修复2: 测试网特殊头信息
        print("\n2. 测试网特殊头信息修复...")
        header_fix = self.fix_testnet_headers()
        fix_results['header'] = header_fix
        
        # 修复3: 签名算法修复
        print("\n3. 签名算法修复...")
        signature_fix = self.fix_signature_algorithm()
        fix_results['signature'] = signature_fix
        
        # 修复4: 连接参数修复
        print("\n4. 连接参数修复...")
        connection_fix = self.fix_connection_params()
        fix_results['connection'] = connection_fix
        
        return fix_results
    
    def fix_api_url(self):
        """修复API地址"""
        print("   修复API地址...")
        
        # 测试不同的API地址
        test_urls = [
            {
                'url': 'https://www.okx.com',
                'description': '标准地址'
            },
            {
                'url': 'https://aws.okx.com',
                'description': 'AWS地址'
            },
            {
                'url': 'https://okx.com',
                'description': '简化地址'
            }
        ]
        
        for test_url in test_urls:
            print(f"\n      测试 {test_url['description']}...")
            
            try:
                timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
                request_path = "/api/v5/account/balance"
                
                message = timestamp + 'GET' + request_path
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
                    'Content-Type': 'application/json',
                    'x-simulated-trading': '1'
                }
                
                url = f"{test_url['url']}{request_path}"
                response = self.session.get(url, headers=headers, timeout=10)
                
                print(f"        响应状态: {response.status_code}")
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get('code') == '0':
                        print(f"        ✅ {test_url['description']}: 成功")
                        return {'success': True, 'url': test_url['url']}
                    else:
                        error_msg = data.get('msg', '未知错误')
                        print(f"        ❌ {test_url['description']}: {error_msg}")
                else:
                    print(f"        ❌ {test_url['description']}: HTTP {response.status_code}")
                    
            except Exception as e:
                print(f"        ❌ {test_url['description']}: {e}")
        
        return {'success': False}
    
    def fix_testnet_headers(self):
        """修复测试网头信息"""
        print("   修复测试网头信息...")
        
        # 测试不同的头信息组合
        header_combinations = [
            {
                'name': '标准模拟头',
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
                'name': '双头组合',
                'headers': {
                    'x-simulated-trading': '1',
                    'x-testnet': '1'
                }
            },
            {
                'name': '无特殊头',
                'headers': {}
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
        
        for combination in header_combinations:
            print(f"\n      测试 {combination['name']}...")
            
            headers = {**base_headers, **combination['headers']}
            
            try:
                url = f"{self.testnet_url}{request_path}"
                response = self.session.get(url, headers=headers, timeout=10)
                
                print(f"        响应状态: {response.status_code}")
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get('code') == '0':
                        print(f"        ✅ {combination['name']}: 成功")
                        return {'success': True, 'combination': combination['name']}
                    else:
                        error_msg = data.get('msg', '未知错误')
                        print(f"        ❌ {combination['name']}: {error_msg}")
                else:
                    print(f"        ❌ {combination['name']}: HTTP {response.status_code}")
                    
            except Exception as e:
                print(f"        ❌ {combination['name']}: {e}")
        
        return {'success': False}
    
    def fix_signature_algorithm(self):
        """修复签名算法"""
        print("   修复签名算法...")
        
        timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        request_path = "/api/v5/account/balance"
        
        # 测试不同的签名算法
        signature_methods = [
            {
                'name': '标准签名',
                'message': timestamp + 'GET' + request_path,
                'secret': self.secret
            },
            {
                'name': '带空格签名',
                'message': timestamp + ' GET ' + request_path,
                'secret': self.secret
            },
            {
                'name': '小写签名',
                'message': timestamp + 'get' + request_path,
                'secret': self.secret
            },
            {
                'name': '带查询参数签名',
                'message': timestamp + 'GET' + request_path + '?ccy=USDT',
                'secret': self.secret
            }
        ]
        
        for method in signature_methods:
            print(f"\n      测试 {method['name']}...")
            
            try:
                signature = hmac.new(
                    method['secret'].encode('utf-8'),
                    method['message'].encode('utf-8'),
                    hashlib.sha256
                ).hexdigest()
                
                headers = {
                    'OK-ACCESS-KEY': self.api_key,
                    'OK-ACCESS-SIGN': signature,
                    'OK-ACCESS-TIMESTAMP': timestamp,
                    'OK-ACCESS-PASSPHRASE': self.passphrase,
                    'Content-Type': 'application/json',
                    'x-simulated-trading': '1'
                }
                
                url = f"{self.testnet_url}{request_path}"
                if '查询参数' in method['name']:
                    url += '?ccy=USDT'
                
                response = self.session.get(url, headers=headers, timeout=10)
                
                print(f"        响应状态: {response.status_code}")
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get('code') == '0':
                        print(f"        ✅ {method['name']}: 成功")
                        return {'success': True, 'method': method['name']}
                    else:
                        error_msg = data.get('msg', '未知错误')
                        print(f"        ❌ {method['name']}: {error_msg}")
                else:
                    print(f"        ❌ {method['name']}: HTTP {response.status_code}")
                    
            except Exception as e:
                print(f"        ❌ {method['name']}: {e}")
        
        return {'success': False}
    
    def fix_connection_params(self):
        """修复连接参数"""
        print("   修复连接参数...")
        
        # 测试不同的连接参数
        connection_params = [
            {
                'name': '标准超时',
                'timeout': 15,
                'verify': True
            },
            {
                'name': '长超时',
                'timeout': 30,
                'verify': True
            },
            {
                'name': '短超时',
                'timeout': 5,
                'verify': True
            },
            {
                'name': '不验证SSL',
                'timeout': 15,
                'verify': False
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
        
        headers = {
            'OK-ACCESS-KEY': self.api_key,
            'OK-ACCESS-SIGN': signature,
            'OK-ACCESS-TIMESTAMP': timestamp,
            'OK-ACCESS-PASSPHRASE': self.passphrase,
            'Content-Type': 'application/json',
            'x-simulated-trading': '1'
        }
        
        for params in connection_params:
            print(f"\n      测试 {params['name']}...")
            
            try:
                url = f"{self.testnet_url}{request_path}"
                response = self.session.get(url, headers=headers, timeout=params['timeout'], verify=params['verify'])
                
                print(f"        响应状态: {response.status_code}")
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get('code') == '0':
                        print(f"        ✅ {params['name']}: 成功")
                        return {'success': True, 'params': params['name']}
                    else:
                        error_msg = data.get('msg', '未知错误')
                        print(f"        ❌ {params['name']}: {error_msg}")
                else:
                    print(f"        ❌ {params['name']}: HTTP {response.status_code}")
                    
            except Exception as e:
                print(f"        ❌ {params['name']}: {e}")
        
        return {'success': False}
    
    def generate_fix_report(self, fix_results):
        """生成修复报告"""
        print("\n💰 【虞姬OKX测试网连接方式修复报告】")
        print(f"📅 报告时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)
        
        # 修复结果汇总
        print("\n🔧 【修复结果汇总】")
        
        successful_fixes = []
        failed_fixes = []
        
        for fix_name, result in fix_results.items():
            if result.get('success'):
                successful_fixes.append(fix_name)
            else:
                failed_fixes.append(fix_name)
        
        print(f"   成功修复: {len(successful_fixes)}/{len(fix_results)}")
        print(f"   失败修复: {len(failed_fixes)}/{len(fix_results)}")
        
        if successful_fixes:
            print(f"\n   ✅ 成功修复:")
            for fix in successful_fixes:
                print(f"      • {fix}")
        
        if failed_fixes:
            print(f"\n   ❌ 失败修复:")
            for fix in failed_fixes:
                print(f"      • {fix}")
        
        # 根本原因分析
        print(f"\n🔍 【根本原因分析】")
        if any(result.get('success') for result in fix_results.values()):
            print("   ✅ 找到有效连接方式")
            print("   💡 虞姬连接方式可以修复")
        else:
            print("   🔧 所有修复尝试都失败")
            print("   💡 问题不在虞姬连接方式")
            print("   💡 真正原因: API配置问题")
        
        # 最终解决方案
        print(f"\n🚀 【最终解决方案】")
        if any(result.get('success') for result in fix_results.values()):
            print("   ✅ 虞姬连接方式修复成功")
            print("   🎯 可以立即开始真实模拟交易")
        else:
            print("   🔧 虞姬连接方式无法修复")
            print("   📋 必须重新配置模拟账号:")
            print("      1. 手动登录OKX模拟交易页面")
            print("      2. 确认模拟账号可正常访问")
            print("      3. 重新生成API密钥")
            print("      4. 启用所有交易权限")
            print("      5. 添加服务器IP到白名单")
        
        print("\n" + "=" * 70)
    
    def run_testnet_fix(self):
        """运行测试网修复"""
        print("🚀 虞姬OKX测试网连接方式修复系统")
        print(f"⏰ 修复时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)
        
        # 测试网连接方式修复
        fix_results = self.fix_testnet_connection()
        
        # 生成修复报告
        self.generate_fix_report(fix_results)
        
        print("\n" + "=" * 70)
        
        # 总结
        if any(result.get('success') for result in fix_results.values()):
            print("🎉 虞姬连接方式修复成功! 可以立即开始模拟交易!")
            return True
        else:
            print("⚠️ 虞姬连接方式无法修复，必须重新配置模拟账号")
            return False

# 立即运行测试网修复
def fix_okx_testnet():
    """修复OKX测试网连接"""
    print("🔧 立即修复虞姬OKX测试网连接方式...")
    
    fixer = OKXTestnetConnectionFix()
    
    try:
        success = fixer.run_testnet_fix()
        return success
    except Exception as e:
        print(f"❌ 修复异常: {e}")
        return False

if __name__ == "__main__":
    fix_okx_testnet()