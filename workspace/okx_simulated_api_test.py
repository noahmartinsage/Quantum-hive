#!/usr/bin/env python3
"""
虞姬OKX模拟盘专用API测试
测试模拟盘专用API地址和WebSocket频道
"""

import time
import hmac
import hashlib
import requests
import json
from datetime import datetime

class OKXSimulatedAPITest:
    def __init__(self):
        # OKX模拟账号API配置
        self.api_key = "9173aacb-75b5-4377-b682-2835afb8be6f"
        self.secret = "F7C576C3759C919A266CF8735B5AF9BC"
        self.passphrase = "Qian1314."
        
        # 模拟盘专用API地址
        self.api_endpoints = [
            "https://www.okx.com",  # 标准地址
            "https://www.okx.com",  # 带模拟头的标准地址
        ]
        
        # 稳健连接
        self.session = requests.Session()
        self.session.trust_env = False
    
    def test_all_api_endpoints(self):
        """测试所有API端点"""
        print("🔍 测试OKX模拟盘所有API端点...")
        print("=" * 60)
        
        endpoint_results = {}
        
        # 测试1: 标准REST API
        print("\n1. 测试标准REST API...")
        standard_result = self.test_standard_rest()
        endpoint_results['standard_rest'] = standard_result
        
        # 测试2: 带模拟头的REST API
        print("\n2. 测试带模拟头的REST API...")
        simulated_header_result = self.test_simulated_header_rest()
        endpoint_results['simulated_header_rest'] = simulated_header_result
        
        # 测试3: 模拟盘专用配置
        print("\n3. 测试模拟盘专用配置...")
        simulated_config_result = self.test_simulated_config()
        endpoint_results['simulated_config'] = simulated_config_result
        
        # 测试4: 公开接口测试
        print("\n4. 测试公开接口...")
        public_result = self.test_public_interfaces()
        endpoint_results['public_interfaces'] = public_result
        
        return endpoint_results
    
    def test_standard_rest(self):
        """测试标准REST API"""
        base_url = "https://www.okx.com"
        
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
            
            url = f"{base_url}{request_path}"
            response = self.session.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('code') == '0':
                    print(f"   ✅ 标准REST: 成功")
                    return {'success': True, 'data': data}
                else:
                    error_msg = data.get('msg', '未知错误')
                    print(f"   ❌ 标准REST: {error_msg}")
                    return {'success': False, 'error': error_msg}
            else:
                print(f"   ❌ 标准REST: HTTP {response.status_code}")
                return {'success': False, 'error': f'HTTP {response.status_code}'}
                
        except Exception as e:
            print(f"   ❌ 标准REST: {e}")
            return {'success': False, 'error': str(e)}
    
    def test_simulated_header_rest(self):
        """测试带模拟头的REST API"""
        base_url = "https://www.okx.com"
        
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
            
            url = f"{base_url}{request_path}"
            response = self.session.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('code') == '0':
                    print(f"   ✅ 模拟头REST: 成功")
                    balance_info = self.parse_balance_data(data)
                    return {'success': True, 'data': balance_info}
                else:
                    error_msg = data.get('msg', '未知错误')
                    print(f"   ❌ 模拟头REST: {error_msg}")
                    return {'success': False, 'error': error_msg}
            else:
                print(f"   ❌ 模拟头REST: HTTP {response.status_code}")
                return {'success': False, 'error': f'HTTP {response.status_code}'}
                
        except Exception as e:
            print(f"   ❌ 模拟头REST: {e}")
            return {'success': False, 'error': str(e)}
    
    def test_simulated_config(self):
        """测试模拟盘专用配置"""
        print("   测试模拟盘专用配置组合...")
        
        config_combinations = [
            {
                'description': '标准配置',
                'headers': {
                    'OK-ACCESS-KEY': self.api_key,
                    'OK-ACCESS-SIGN': '',
                    'OK-ACCESS-TIMESTAMP': '',
                    'OK-ACCESS-PASSPHRASE': self.passphrase,
                    'Content-Type': 'application/json'
                }
            },
            {
                'description': '模拟头配置',
                'headers': {
                    'OK-ACCESS-KEY': self.api_key,
                    'OK-ACCESS-SIGN': '',
                    'OK-ACCESS-TIMESTAMP': '',
                    'OK-ACCESS-PASSPHRASE': self.passphrase,
                    'Content-Type': 'application/json',
                    'x-simulated-trading': '1'
                }
            },
            {
                'description': '简化配置',
                'headers': {
                    'OK-ACCESS-KEY': self.api_key,
                    'OK-ACCESS-SIGN': '',
                    'OK-ACCESS-TIMESTAMP': '',
                    'OK-ACCESS-PASSPHRASE': self.passphrase
                }
            }
        ]
        
        for config in config_combinations:
            print(f"\n      测试 {config['description']}...")
            
            try:
                timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
                request_path = "/api/v5/account/balance"
                
                message = timestamp + 'GET' + request_path
                signature = hmac.new(
                    self.secret.encode('utf-8'),
                    message.encode('utf-8'),
                    hashlib.sha256
                ).hexdigest()
                
                headers = config['headers'].copy()
                headers['OK-ACCESS-SIGN'] = signature
                headers['OK-ACCESS-TIMESTAMP'] = timestamp
                
                url = f"https://www.okx.com{request_path}"
                response = self.session.get(url, headers=headers, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get('code') == '0':
                        print(f"         ✅ {config['description']}: 成功")
                        return {'success': True, 'config': config['description']}
                    else:
                        error_msg = data.get('msg', '未知错误')
                        print(f"         ❌ {config['description']}: {error_msg}")
                else:
                    print(f"         ❌ {config['description']}: HTTP {response.status_code}")
                    
            except Exception as e:
                print(f"         ❌ {config['description']}: {e}")
        
        return {'success': False}
    
    def test_public_interfaces(self):
        """测试公开接口"""
        print("   测试公开接口连通性...")
        
        public_endpoints = [
            ("/api/v5/public/time", "时间接口"),
            ("/api/v5/public/instruments?instType=SPOT", "交易对接口"),
            ("/api/v5/market/ticker?instId=BTC-USDT", "BTC行情"),
            ("/api/v5/market/ticker?instId=BTC-USDT-SWAP", "BTC合约行情")
        ]
        
        results = []
        
        for endpoint, description in public_endpoints:
            try:
                url = f"https://www.okx.com{endpoint}"
                response = self.session.get(url, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get('code') == '0':
                        print(f"         ✅ {description}: 正常")
                        
                        # 解析行情数据
                        if 'ticker' in endpoint:
                            ticker_data = data.get('data', [{}])[0]
                            last_price = float(ticker_data.get('last', '0'))
                            print(f"            当前价格: {last_price:.2f} USDT")
                        
                        results.append({'endpoint': endpoint, 'status': '正常'})
                    else:
                        print(f"         ❌ {description}: {data.get('msg')}")
                        results.append({'endpoint': endpoint, 'status': '错误'})
                else:
                    print(f"         ❌ {description}: HTTP {response.status_code}")
                    results.append({'endpoint': endpoint, 'status': '错误'})
                    
            except Exception as e:
                print(f"         ❌ {description}: {e}")
                results.append({'endpoint': endpoint, 'status': '异常'})
        
        return results
    
    def parse_balance_data(self, data):
        """解析余额数据"""
        try:
            balance_data = data.get('data', [{}])[0]
            details = balance_data.get('details', [])
            
            balance_info = {
                'total_equity': float(balance_data.get('totalEq', '0')),
                'iso_equity': float(balance_data.get('isoEq', '0')),
                'adj_equity': float(balance_data.get('adjEq', '0')),
                'ord_frozen': float(balance_data.get('ordFroz', '0')),
                'currency_details': []
            }
            
            for detail in details:
                currency_info = {
                    'currency': detail.get('ccy', ''),
                    'balance': float(detail.get('cashBal', '0')),
                    'available': float(detail.get('availEq', '0')),
                    'frozen': float(detail.get('frozenBal', '0'))
                }
                balance_info['currency_details'].append(currency_info)
            
            return balance_info
            
        except Exception as e:
            print(f"   ❌ 余额数据解析异常: {e}")
            return None
    
    def generate_simulated_api_report(self, endpoint_results):
        """生成模拟API报告"""
        print("\n💰 【虞姬OKX模拟盘专用API测试报告】")
        print(f"📅 报告时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)
        
        # API端点分析
        print("\n🔗 【API端点测试结果】")
        
        successful_tests = []
        failed_tests = []
        
        for test_name, result in endpoint_results.items():
            if result.get('success'):
                successful_tests.append(test_name)
            else:
                failed_tests.append(test_name)
        
        print(f"   成功测试: {len(successful_tests)}/{len(endpoint_results)}")
        print(f"   失败测试: {len(failed_tests)}/{len(endpoint_results)}")
        
        if successful_tests:
            print(f"\n   ✅ 成功测试:")
            for test in successful_tests:
                print(f"      • {test}")
        
        if failed_tests:
            print(f"\n   ❌ 失败测试:")
            for test in failed_tests:
                print(f"      • {test}")
        
        # 公开接口状态
        print(f"\n🌐 【公开接口状态】")
        public_results = endpoint_results['public_interfaces']
        public_ok = all(r['status'] == '正常' for r in public_results)
        
        if public_ok:
            print("   ✅ 公开接口: 全部正常")
        else:
            print("   ❌ 公开接口: 部分异常")
        
        # 问题根本原因分析
        print(f"\n🔍 【问题根本原因分析】")
        
        if not any(result.get('success') for result in endpoint_results.values() if isinstance(result, dict)):
            print("   🔧 根本原因: API密钥配置问题")
            print("   💡 可能原因:")
            print("      • API密钥无效或已过期")
            print("      • Passphrase设置不正确")
            print("      • IP白名单未配置")
            print("      • 模拟账号状态异常")
        else:
            print("   🔧 部分连接成功，需要进一步调试")
        
        # 解决方案
        print(f"\n🚀 【立即解决方案】")
        print("   1. 重新生成OKX模拟账号API密钥")
        print("   2. 确认模拟账号可正常访问")
        print("   3. 设置简单Passphrase")
        print("   4. 启用完整交易权限")
        print("   5. 添加服务器IP到白名单")
        
        # WebSocket频道信息
        print(f"\n📡 【WebSocket频道信息】")
        print("   公共频道: wss://wspap.okx.com:8443/ws/v5/public")
        print("   私有频道: wss://wspap.okx.com:8443/ws/v5/private")
        print("   业务频道: wss://wspap.okx.com:8443/ws/v5/business")
        print("   💡 一旦REST API连接成功，WebSocket即可使用")
        
        print("\n" + "=" * 70)
    
    def run_simulated_api_test(self):
        """运行模拟API测试"""
        print("🚀 虞姬OKX模拟盘专用API测试系统")
        print(f"⏰ 测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)
        
        # 测试所有API端点
        endpoint_results = self.test_all_api_endpoints()
        
        # 生成模拟API报告
        self.generate_simulated_api_report(endpoint_results)
        
        print("\n" + "=" * 70)
        
        # 总结
        if any(result.get('success') for result in endpoint_results.values() if isinstance(result, dict)):
            print("✅ 部分API连接成功!")
        else:
            print("⚠️ 所有API连接失败，必须重新生成API密钥")

# 立即运行模拟API测试
def test_okx_simulated_api():
    """测试OKX模拟API"""
    print("🔍 立即测试虞姬OKX模拟盘专用API...")
    
    tester = OKXSimulatedAPITest()
    
    try:
        tester.run_simulated_api_test()
    except Exception as e:
        print(f"❌ 测试异常: {e}")

if __name__ == "__main__":
    test_okx_simulated_api()