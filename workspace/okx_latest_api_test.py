#!/usr/bin/env python3
"""
虞姬OKX最新API凭据测试
使用老板提供的最新API凭据测试OKX连接
"""

import time
import hmac
import hashlib
import requests
import json
from datetime import datetime

class OKXLatestAPITest:
    def __init__(self):
        # 老板提供的最新API凭据
        self.api_key = "cefedac1-1d25-4fae-861d-9f006e4cd654"
        self.secret = "EE66B6A88F9E57FBCAE6219081DABDE1"
        self.passphrase = "Qian1314."
        self.base_url = "https://www.okx.com"
        
        # 稳健连接
        self.session = requests.Session()
        self.session.trust_env = False
    
    def test_latest_api_comprehensive(self):
        """全面测试最新API凭据"""
        print("🔍 使用老板最新API凭据全面测试OKX连接...")
        print("=" * 60)
        
        test_results = {}
        
        # 测试1: 标准REST API
        print("\n1. 测试标准REST API...")
        standard_result = self.test_standard_request()
        test_results['standard'] = standard_result
        
        # 测试2: 模拟交易REST API
        print("\n2. 测试模拟交易REST API...")
        simulated_result = self.test_simulated_request()
        test_results['simulated'] = simulated_result
        
        # 测试3: 全面端点测试
        print("\n3. 测试全面端点...")
        endpoints_result = self.test_all_endpoints()
        test_results['endpoints'] = endpoints_result
        
        # 测试4: 余额和持仓查询
        print("\n4. 测试余额和持仓...")
        balance_positions = self.test_balance_and_positions()
        test_results['balance_positions'] = balance_positions
        
        return test_results
    
    def test_standard_request(self):
        """测试标准请求"""
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
            response = self.session.get(url, headers=headers, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('code') == '0':
                    print(f"   ✅ 标准请求: 成功")
                    balance_info = self.parse_balance_data(data)
                    return {'success': True, 'data': balance_info}
                else:
                    error_msg = data.get('msg', '未知错误')
                    error_code = data.get('code', '未知')
                    print(f"   ❌ 标准请求: {error_code} - {error_msg}")
                    return {'success': False, 'error': f'{error_code} - {error_msg}'}
            else:
                print(f"   ❌ 标准请求: HTTP {response.status_code}")
                
                # 详细分析响应
                try:
                    error_data = response.json()
                    print(f"      错误代码: {error_data.get('code')}")
                    print(f"      错误信息: {error_data.get('msg')}")
                except:
                    print(f"      原始响应: {response.text}")
                
                return {'success': False, 'error': f'HTTP {response.status_code}'}
                
        except Exception as e:
            print(f"   ❌ 标准请求: {e}")
            return {'success': False, 'error': str(e)}
    
    def test_simulated_request(self):
        """测试模拟交易请求"""
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
            response = self.session.get(url, headers=headers, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('code') == '0':
                    print(f"   ✅ 模拟请求: 成功")
                    balance_info = self.parse_balance_data(data)
                    return {'success': True, 'data': balance_info}
                else:
                    error_msg = data.get('msg', '未知错误')
                    error_code = data.get('code', '未知')
                    print(f"   ❌ 模拟请求: {error_code} - {error_msg}")
                    return {'success': False, 'error': f'{error_code} - {error_msg}'}
            else:
                print(f"   ❌ 模拟请求: HTTP {response.status_code}")
                
                # 详细分析响应
                try:
                    error_data = response.json()
                    print(f"      错误代码: {error_data.get('code')}")
                    print(f"      错误信息: {error_data.get('msg')}")
                except:
                    print(f"      原始响应: {response.text}")
                
                return {'success': False, 'error': f'HTTP {response.status_code}'}
                
        except Exception as e:
            print(f"   ❌ 模拟请求: {e}")
            return {'success': False, 'error': str(e)}
    
    def test_all_endpoints(self):
        """测试所有端点"""
        endpoints = [
            ("/api/v5/account/balance", "余额查询"),
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
                        error_code = data.get('code', '未知')
                        print(f"      ❌ {description}: {error_code} - {error_msg}")
                        results[description] = {'success': False, 'error': f'{error_code} - {error_msg}'}
                else:
                    print(f"      ❌ {description}: HTTP {response.status_code}")
                    results[description] = {'success': False, 'error': f'HTTP {response.status_code}'}
                    
            except Exception as e:
                print(f"      ❌ {description}: {e}")
                results[description] = {'success': False, 'error': str(e)}
        
        return results
    
    def test_balance_and_positions(self):
        """测试余额和持仓"""
        print("   测试余额和持仓信息...")
        
        results = {}
        
        # 测试余额
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
            response = self.session.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('code') == '0':
                    balance_info = self.parse_balance_data(data)
                    print(f"      ✅ 余额查询: 成功")
                    results['balance'] = {'success': True, 'data': balance_info}
                else:
                    error_msg = data.get('msg', '未知错误')
                    print(f"      ❌ 余额查询: {error_msg}")
                    results['balance'] = {'success': False, 'error': error_msg}
            else:
                print(f"      ❌ 余额查询: HTTP {response.status_code}")
                results['balance'] = {'success': False, 'error': f'HTTP {response.status_code}'}
                
        except Exception as e:
            print(f"      ❌ 余额查询: {e}")
            results['balance'] = {'success': False, 'error': str(e)}
        
        # 测试持仓
        try:
            timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
            request_path = "/api/v5/account/positions"
            
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
            response = self.session.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('code') == '0':
                    positions = data.get('data', [])
                    print(f"      ✅ 持仓查询: 成功")
                    print(f"         持仓数量: {len(positions)}")
                    results['positions'] = {'success': True, 'data': positions}
                else:
                    error_msg = data.get('msg', '未知错误')
                    print(f"      ❌ 持仓查询: {error_msg}")
                    results['positions'] = {'success': False, 'error': error_msg}
            else:
                print(f"      ❌ 持仓查询: HTTP {response.status_code}")
                results['positions'] = {'success': False, 'error': f'HTTP {response.status_code}'}
                
        except Exception as e:
            print(f"      ❌ 持仓查询: {e}")
            results['positions'] = {'success': False, 'error': str(e)}
        
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
                'imr': float(balance_data.get('imr', '0')),
                'mmr': float(balance_data.get('mmr', '0')),
                'mgn_ratio': float(balance_data.get('mgnRatio', '0')),
                'currency_details': []
            }
            
            for detail in details:
                currency_info = {
                    'currency': detail.get('ccy', ''),
                    'balance': float(detail.get('cashBal', '0')),
                    'available': float(detail.get('availEq', '0')),
                    'frozen': float(detail.get('frozenBal', '0')),
                    'equity': float(detail.get('eq', '0'))
                }
                balance_info['currency_details'].append(currency_info)
            
            return balance_info
            
        except Exception as e:
            print(f"   ❌ 余额数据解析异常: {e}")
            return None
    
    def generate_latest_api_report(self, test_results):
        """生成最新API报告"""
        print("\n💰 【虞姬OKX最新API凭据测试报告】")
        print(f"📅 报告时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)
        
        # API凭据状态
        print("\n🔑 【API凭据状态】")
        standard_success = test_results['standard'].get('success', False)
        simulated_success = test_results['simulated'].get('success', False)
        
        if standard_success or simulated_success:
            print("   ✅ 最新API凭据连接成功!")
            
            # 显示余额信息
            if simulated_success:
                balance_info = test_results['simulated']['data']
                print(f"\n📊 【模拟账号资产总览】")
                print(f"   总权益: {balance_info['total_equity']:.2f} USDT")
                print(f"   独立权益: {balance_info['iso_equity']:.2f} USDT")
                print(f"   调整权益: {balance_info['adj_equity']:.2f} USDT")
                
                # 货币余额详情
                print(f"\n💱 【货币余额分布】")
                for currency in balance_info['currency_details']:
                    if currency['balance'] > 0:
                        print(f"   {currency['currency']}:")
                        print(f"      余额: {currency['balance']:.4f}")
                        print(f"      可用: {currency['available']:.4f}")
                        print(f"      冻结: {currency['frozen']:.4f}")
                        print(f"      权益: {currency['equity']:.4f}")
            
        else:
            print("   ❌ 最新API凭据连接失败")
            print(f"   标准请求错误: {test_results['standard'].get('error')}")
            print(f"   模拟请求错误: {test_results['simulated'].get('error')}")
        
        # 端点测试结果
        print(f"\n🔧 【端点测试结果】")
        endpoints_results = test_results['endpoints']
        successful_endpoints = []
        failed_endpoints = []
        
        for endpoint, result in endpoints_results.items():
            if result.get('success'):
                successful_endpoints.append(endpoint)
            else:
                failed_endpoints.append(endpoint)
        
        print(f"   成功端点: {len(successful_endpoints)}/{len(endpoints_results)}")
        print(f"   失败端点: {len(failed_endpoints)}/{len(endpoints_results)}")
        
        if successful_endpoints:
            print(f"\n   ✅ 成功端点:")
            for endpoint in successful_endpoints:
                print(f"      • {endpoint}")
        
        if failed_endpoints:
            print(f"\n   ❌ 失败端点:")
            for endpoint in failed_endpoints:
                print(f"      • {endpoint}")
        
        # 余额和持仓信息
        print(f"\n📈 【余额和持仓信息】")
        balance_positions = test_results['balance_positions']
        
        if balance_positions['balance'].get('success'):
            balance_info = balance_positions['balance']['data']
            print(f"   总资产: {balance_info['total_equity']:.2f} USDT")
        else:
            print(f"   余额查询: 失败")
        
        if balance_positions['positions'].get('success'):
            positions = balance_positions['positions']['data']
            print(f"   持仓数量: {len(positions)}")
        else:
            print(f"   持仓查询: 失败")
        
        # 解决方案
        print(f"\n🚀 【立即行动】")
        if standard_success or simulated_success:
            print("   ✅ 最新API凭据有效")
            print("   🎯 可以立即开始真实模拟交易")
            print("   📈 启动10U高倍合约量化交易")
        else:
            print("   🔧 最新API凭据仍然无效")
            print("   📋 必须重新配置模拟账号:")
            print("      1. 手动登录OKX模拟交易页面验证")
            print("      2. 重新生成API密钥")
            print("      3. 设置极简Passphrase")
            print("      4. 启用所有交易权限")
            print("      5. 添加服务器IP到白名单")
        
        print("\n" + "=" * 70)
    
    def run_latest_api_test(self):
        """运行最新API测试"""
        print("🚀 虞姬OKX最新API凭据测试系统")
        print(f"⏰ 测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)
        
        # 全面测试最新API凭据
        test_results = self.test_latest_api_comprehensive()
        
        # 生成最新API报告
        self.generate_latest_api_report(test_results)
        
        print("\n" + "=" * 70)
        
        # 总结
        if test_results['standard'].get('success') or test_results['simulated'].get('success'):
            print("🎉 最新API凭据连接成功! 可以立即开始模拟交易!")
            return True
        else:
            print("⚠️ 最新API凭据连接失败，必须重新配置模拟账号")
            return False

# 立即运行最新API测试
def test_okx_latest_api():
    """测试OKX最新API"""
    print("🔑 立即测试虞姬OKX最新API凭据...")
    
    tester = OKXLatestAPITest()
    
    try:
        success = tester.run_latest_api_test()
        return success
    except Exception as e:
        print(f"❌ 测试异常: {e}")
        return False

if __name__ == "__main__":
    test_okx_latest_api()