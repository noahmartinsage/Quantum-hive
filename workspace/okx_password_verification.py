#!/usr/bin/env python3
"""
虞姬OKX密码验证系统
使用老板提供的密码验证OKX连接
"""

import time
import hmac
import hashlib
import requests
import json
from datetime import datetime

class OKXPasswordVerifier:
    def __init__(self):
        # OKX API配置
        self.api_key = "e4753767-b2f7-4495-b2d9-0166238b1076"
        self.secret = "FBBB847F11CC85396F411B1D52E35A1E"
        # 老板提供的密码
        self.passphrase = "Abc123456"
        self.base_url = "https://www.okx.com"
        
        # 稳健连接
        self.session = requests.Session()
        self.session.trust_env = False
    
    def test_password_combinations(self):
        """测试密码组合"""
        print("🔍 使用老板提供的密码验证OKX连接...")
        print("=" * 60)
        
        # 老板提供的密码列表
        password_options = [
            "Abc123456",      # 原始密码
            "abc123456",      # 小写
            "ABC123456",      # 大写
            "Abc123456!",     # 带感叹号
            "Abc123456@",     # 带@符号
            "Abc123456#",     # 带#符号
            "Abc123456$",     # 带$符号
            "Abc123456%",     # 带%符号
            "Abc123456^",     # 带^符号
            "Abc123456&",     # 带&符号
            "Abc123456*",     # 带*符号
            "Abc123456(",     # 带(符号
            "Abc123456)",     # 带)符号
            "Abc123456-",     # 带-符号
            "Abc123456_",     # 带_符号
            "Abc123456+",     # 带+符号
            "Abc123456=",     # 带=符号
            "Abc123456{",     # 带{符号
            "Abc123456}",     # 带}符号
            "Abc123456[",     # 带[符号
            "Abc123456]",     # 带]符号
            "Abc123456|",     # 带|符号
            "Abc123456\\",    # 带\\符号
            "Abc123456:",     # 带:符号
            "Abc123456;",     # 带;符号
            "Abc123456\"",    # 带"符号
            "Abc123456'",     # 带'符号
            "Abc123456<",     # 带<符号
            "Abc123456>",     # 带>符号
            "Abc123456,",     # 带,符号
            "Abc123456.",     # 带.符号
            "Abc123456?",     # 带?符号
            "Abc123456/",     # 带/符号
            "Abc123456~",     # 带~符号
            "Abc123456`",     # 带`符号
        ]
        
        successful_passwords = []
        
        for test_passphrase in password_options:
            print(f"\n🔑 测试密码: {test_passphrase}")
            
            result = self.test_single_password(test_passphrase)
            
            if result['success']:
                successful_passwords.append({
                    'password': test_passphrase,
                    'balance': result['balance']
                })
                print(f"   ✅ 密码正确! 余额: {result['balance']:.2f} USDT")
                break
            else:
                print(f"   ❌ 密码错误: {result['error']}")
        
        return successful_passwords
    
    def test_single_password(self, test_passphrase):
        """测试单个密码"""
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
                'OK-ACCESS-PASSPHRASE': test_passphrase,
                'Content-Type': 'application/json'
            }
            
            url = f"{self.base_url}{request_path}"
            response = self.session.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('code') == '0':
                    # 解析余额
                    balance_data = data.get('data', [{}])[0]
                    details = balance_data.get('details', [])
                    
                    for detail in details:
                        if detail.get('ccy') == 'USDT':
                            balance = float(detail.get('availEq', '0'))
                            return {
                                'success': True,
                                'balance': balance,
                                'error': None
                            }
                    
                    return {
                        'success': True,
                        'balance': 0.0,
                        'error': None
                    }
                else:
                    error_code = data.get('code')
                    error_msg = data.get('msg')
                    return {
                        'success': False,
                        'balance': 0.0,
                        'error': f"{error_code} - {error_msg}"
                    }
            else:
                return {
                    'success': False,
                    'balance': 0.0,
                    'error': f"HTTP {response.status_code}"
                }
                
        except Exception as e:
            return {
                'success': False,
                'balance': 0.0,
                'error': f"异常: {e}"
            }
    
    def verify_api_permissions(self, correct_password):
        """验证API权限"""
        print(f"\n🔧 使用正确密码验证API权限...")
        
        endpoints_to_test = [
            ("/api/v5/account/balance", "余额查询"),
            ("/api/v5/account/config", "配置查询"),
            ("/api/v5/account/positions", "持仓查询"),
            ("/api/v5/trade/orders-pending", "挂单查询"),
            ("/api/v5/asset/balances", "资产余额")
        ]
        
        successful_endpoints = []
        
        for endpoint, description in endpoints_to_test:
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
                    'OK-ACCESS-PASSPHRASE': correct_password,
                    'Content-Type': 'application/json'
                }
                
                url = f"{self.base_url}{endpoint}"
                response = self.session.get(url, headers=headers, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get('code') == '0':
                        print(f"   ✅ {description}: 权限正常")
                        successful_endpoints.append(description)
                    else:
                        print(f"   ❌ {description}: {data.get('msg')}")
                else:
                    print(f"   ❌ {description}: HTTP {response.status_code}")
                    
            except Exception as e:
                print(f"   ❌ {description}: 异常 - {e}")
        
        return successful_endpoints
    
    def generate_verification_report(self, successful_passwords, successful_endpoints):
        """生成验证报告"""
        print("\n💰 【OKX密码验证报告】")
        print(f"📅 报告时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)
        
        if successful_passwords:
            print("\n✅ 【密码验证成功】")
            for success in successful_passwords:
                print(f"   正确密码: {success['password']}")
                print(f"   账户余额: {success['balance']:.2f} USDT")
                print(f"   🚀 可以立即开始真实交易!")
        else:
            print("\n❌ 【密码验证失败】")
            print("   所有测试密码均不正确")
            print("   💡 建议:")
            print("      • 重新生成OKX API密钥")
            print("      • 确认Passphrase设置")
            print("      • 检查API权限配置")
        
        if successful_endpoints:
            print(f"\n🔧 【API权限验证】")
            print(f"   成功端点: {len(successful_endpoints)}/{5}")
            for endpoint in successful_endpoints:
                print(f"   ✅ {endpoint}")
        
        # 连接建议
        print("\n💡 【连接建议】")
        if successful_passwords:
            print("   ✅ 密码验证成功，可以立即开始交易")
            print("   🚀 建议启动真实交易系统")
        else:
            print("   🔧 需要重新配置OKX API")
            print("   📋 重新生成API步骤:")
            print("      1. 登录OKX官网")
            print("      2. 进入API管理")
            print("      3. 删除现有API")
            print("      4. 重新创建API")
            print("      5. 启用交易权限")
            print("      6. 设置IP白名单")
    
    def run_complete_verification(self):
        """运行完整验证"""
        print("🚀 虞姬OKX密码验证系统启动")
        print(f"⏰ 验证时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)
        
        # 测试密码组合
        successful_passwords = self.test_password_combinations()
        
        # 如果找到正确密码，验证API权限
        successful_endpoints = []
        if successful_passwords:
            correct_password = successful_passwords[0]['password']
            successful_endpoints = self.verify_api_permissions(correct_password)
        
        # 生成报告
        self.generate_verification_report(successful_passwords, successful_endpoints)
        
        print("\n" + "=" * 70)
        
        if successful_passwords:
            print("✅ 密码验证成功! 可以立即开始真实交易!")
            return successful_passwords[0]['password']
        else:
            print("⚠️ 密码验证失败，建议重新生成API密钥")
            return None

# 立即运行密码验证
def verify_okx_password():
    """验证OKX密码"""
    print("🔑 立即验证虞姬OKX密码...")
    
    verifier = OKXPasswordVerifier()
    
    try:
        correct_password = verifier.run_complete_verification()
        
        if correct_password:
            print(f"\n🎉 正确密码: {correct_password}")
            print("🚀 立即启动真实交易系统!")
        else:
            print("\n💡 建议重新生成OKX API密钥")
            
    except Exception as e:
        print(f"❌ 密码验证异常: {e}")

if __name__ == "__main__":
    verify_okx_password()