#!/usr/bin/env python3
"""
虞姬OKX新凭据连接测试
使用老板提供的最新OKX凭据进行连接测试
"""

import time
import hmac
import hashlib
import requests
import json
from datetime import datetime

class OKXNewCredentialsTest:
    def __init__(self):
        # 老板提供的最新OKX凭据
        self.api_key = "e4753767-b2f7-4495-b2d9-0166238b1076"
        self.secret = "FBBB847F11CC85396F411B1D52E35A1E"
        self.passphrase = "Qlzwqc2012."
        self.base_url = "https://www.okx.com"
        
        # 稳健连接
        self.session = requests.Session()
        self.session.trust_env = False
    
    def test_new_credentials(self):
        """测试新凭据"""
        print("🔍 虞姬OKX新凭据连接测试...")
        print("=" * 60)
        
        test_results = {}
        
        # 测试1: 标准余额查询
        print("\n1. 标准余额查询测试...")
        balance_test = self.test_standard_balance()
        test_results['balance'] = balance_test
        
        # 测试2: 模拟交易余额查询
        print("\n2. 模拟交易余额查询测试...")
        simulated_test = self.test_simulated_balance()
        test_results['simulated'] = simulated_test
        
        # 测试3: 公开API测试
        print("\n3. 公开API测试...")
        public_test = self.test_public_api()
        test_results['public'] = public_test
        
        # 测试4: 全面端点测试
        print("\n4. 全面端点测试...")
        endpoints_test = self.test_comprehensive_endpoints()
        test_results['endpoints'] = endpoints_test
        
        return test_results
    
    def test_standard_balance(self):
        """测试标准余额查询"""
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
                'Content-Type': 'application/json'
            }
            
            url = f"{self.base_url}{request_path}"
            print(f"   请求URL: {url}")
            print(f"   时间戳: {timestamp}")
            print(f"   签名: {signature[:20]}...")
            
            response = self.session.get(url, headers=headers, timeout=15)
            
            print(f"   响应状态: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                if data.get('code') == '0':
                    print(f"   ✅ 标准余额查询成功!")
                    
                    balance_data = data.get('data', [{}])[0]
                    total_eq = float(balance_data.get('totalEq', '0'))
                    
                    return {'success': True, 'balance': total_eq, 'data': balance_data}
                else:
                    error_code = data.get('code', '未知')
                    error_msg = data.get('msg', '未知错误')
                    print(f"   ❌ 标准余额查询失败: {error_code} - {error_msg}")
                    return {'success': False, 'error': f'{error_code} - {error_msg}'}
            else:
                print(f"   ❌ 标准余额查询失败: HTTP {response.status_code}")
                
                try:
                    error_data = response.json()
                    error_code = error_data.get('code', '未知')
                    error_msg = error_data.get('msg', '未知错误')
                    print(f"   错误代码: {error_code}")
                    print(f"   错误信息: {error_msg}")
                    return {'success': False, 'error': f'{error_code} - {error_msg}'}
                except:
                    print(f"   原始响应: {response.text}")
                    return {'success': False, 'error': f'HTTP {response.status_code}'}
                    
        except Exception as e:
            print(f"   ❌ 标准余额查询异常: {e}")
            return {'success': False, 'error': str(e)}
    
    def test_simulated_balance(self):
        """测试模拟交易余额查询"""
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
            
            url = f"{self.base_url}{request_path}"
            print(f"   请求URL: {url}")
            print(f"   时间戳: {timestamp}")
            print(f"   签名: {signature[:20]}...")
            
            response = self.session.get(url, headers=headers, timeout=15)
            
            print(f"   响应状态: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                if data.get('code') == '0':
                    print(f"   ✅ 模拟交易余额查询成功!")
                    
                    balance_data = data.get('data', [{}])[0]
                    total_eq = float(balance_data.get('totalEq', '0'))
                    
                    return {'success': True, 'balance': total_eq, 'data': balance_data}
                else:
                    error_code = data.get('code', '未知')
                    error_msg = data.get('msg', '未知错误')
                    print(f"   ❌ 模拟交易余额查询失败: {error_code} - {error_msg}")
                    return {'success': False, 'error': f'{error_code} - {error_msg}'}
            else:
                print(f"   ❌ 模拟交易余额查询失败: HTTP {response.status_code}")
                
                try:
                    error_data = response.json()
                    error_code = error_data.get('code', '未知')
                    error_msg = error_data.get('msg', '未知错误')
                    print(f"   错误代码: {error_code}")
                    print(f"   错误信息: {error_msg}")
                    return {'success': False, 'error': f'{error_code} - {error_msg}'}
                except:
                    print(f"   原始响应: {response.text}")
                    return {'success': False, 'error': f'HTTP {response.status_code}'}
                    
        except Exception as e:
            print(f"   ❌ 模拟交易余额查询异常: {e}")
            return {'success': False, 'error': str(e)}
    
    def test_public_api(self):
        """测试公开API"""
        try:
            # 测试BTC行情
            url = f"{self.base_url}/api/v5/market/ticker?instId=BTC-USDT"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('code') == '0':
                    ticker_data = data.get('data', [{}])[0]
                    last_price = float(ticker_data.get('last', '0'))
                    print(f"   ✅ 公开API正常")
                    print(f"   BTC当前价格: {last_price:.2f} USDT")
                    return {'success': True, 'btc_price': last_price}
                else:
                    print(f"   ❌ 公开API错误: {data.get('msg')}")
                    return {'success': False}
            else:
                print(f"   ❌ 公开API失败: HTTP {response.status_code}")
                return {'success': False}
                
        except Exception as e:
            print(f"   ❌ 公开API异常: {e}")
            return {'success': False}
    
    def test_comprehensive_endpoints(self):
        """测试全面端点"""
        endpoints = [
            ("/api/v5/account/config", "配置查询"),
            ("/api/v5/account/positions", "持仓查询"),
            ("/api/v5/trade/orders-pending", "挂单查询"),
            ("/api/v5/asset/balances", "资产余额")
        ]
        
        results = {}
        
        for endpoint, description in endpoints:
            print(f"\n   测试 {description}...")
            
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
                    'Content-Type': 'application/json',
                    'x-simulated-trading': '1'
                }
                
                url = f"{self.base_url}{endpoint}"
                response = self.session.get(url, headers=headers, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get('code') == '0':
                        print(f"      ✅ {description}: 成功")
                        results[description] = {'success': True, 'data': data}
                    else:
                        error_msg = data.get('msg', '未知错误')
                        print(f"      ❌ {description}: {error_msg}")
                        results[description] = {'success': False, 'error': error_msg}
                else:
                    print(f"      ❌ {description}: HTTP {response.status_code}")
                    results[description] = {'success': False, 'error': f'HTTP {response.status_code}'}
                    
            except Exception as e:
                print(f"      ❌ {description}: {e}")
                results[description] = {'success': False, 'error': str(e)}
        
        return results
    
    def generate_new_credentials_report(self, test_results):
        """生成新凭据报告"""
        print("\n💰 【虞姬OKX新凭据连接测试报告】")
        print(f"📅 报告时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)
        
        balance_test = test_results['balance']
        simulated_test = test_results['simulated']
        public_test = test_results['public']
        endpoints_test = test_results['endpoints']
        
        if balance_test['success'] or simulated_test['success']:
            print("\n🎉 【新凭据连接成功】")
            
            if balance_test['success']:
                print(f"   ✅ 标准余额查询成功!")
                print(f"   💰 总资产: {balance_test['balance']:.2f} USDT")
            
            if simulated_test['success']:
                print(f"   ✅ 模拟交易余额查询成功!")
                print(f"   💰 模拟资产: {simulated_test['balance']:.2f} USDT")
            
            if public_test['success']:
                print(f"   📈 BTC价格: {public_test['btc_price']:.2f} USDT")
            
            # 端点测试结果
            successful_endpoints = [k for k, v in endpoints_test.items() if v.get('success')]
            print(f"   🔧 成功端点: {len(successful_endpoints)}/{len(endpoints_test)}")
            
            print(f"\n🚀 【立即行动】")
            print("   可以立即开始真实模拟交易!")
            print("   启动10U高倍合约量化交易!")
        else:
            print("\n❌ 【新凭据连接失败】")
            
            if balance_test['success'] == False:
                print(f"   🔧 标准余额失败: {balance_test['error']}")
            
            if simulated_test['success'] == False:
                print(f"   🔧 模拟交易失败: {simulated_test['error']}")
            
            if public_test['success']:
                print(f"   📈 BTC价格: {public_test['btc_price']:.2f} USDT")
            
            print(f"\n🔍 【问题分析】")
            print("   💡 可能原因:")
            print("      • API密钥状态异常")
            print("      • 模拟账号配置问题")
            print("      • IP白名单未配置")
            print("      • 模拟账号权限设置问题")
            
            print(f"\n🚀 【解决方案】")
            print("   📋 必须重新配置模拟账号:")
            print("      1. 手动登录OKX模拟交易页面")
            print("      2. 确认模拟账号可正常访问")
            print("      3. 重新生成API密钥")
            print("      4. 启用所有交易权限")
            print("      5. 添加服务器IP到白名单")
        
        print("\n" + "=" * 70)
    
    def run_new_credentials_test(self):
        """运行新凭据测试"""
        print("🚀 虞姬OKX新凭据连接测试系统")
        print(f"⏰ 测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)
        
        test_results = {}
        
        # 测试新凭据
        test_results = self.test_new_credentials()
        
        # 生成报告
        self.generate_new_credentials_report(test_results)
        
        print("\n" + "=" * 70)
        
        # 总结
        if test_results['balance']['success'] or test_results['simulated']['success']:
            print("🎉 新凭据连接成功! 可以立即开始模拟交易!")
            return True
        else:
            print("⚠️ 新凭据连接失败，必须重新配置模拟账号")
            return False

# 立即运行新凭据测试
def test_okx_new_credentials():
    """测试OKX新凭据"""
    print("🔍 立即测试虞姬OKX新凭据...")
    
    tester = OKXNewCredentialsTest()
    
    try:
        success = tester.run_new_credentials_test()
        return success
    except Exception as e:
        print(f"❌ 测试异常: {e}")
        return False

if __name__ == "__main__":
    test_okx_new_credentials()