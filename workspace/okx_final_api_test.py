#!/usr/bin/env python3
"""
虞姬OKX最终API凭据测试
使用老板提供的最新API凭据测试OKX连接
"""

import time
import hmac
import hashlib
import requests
import json
from datetime import datetime

class OKXFinalAPITest:
    def __init__(self):
        # 老板提供的最新API凭据
        self.api_key = "f603791b-8ea9-4765-9935-b3fc2847a3ba"
        self.secret = "AED3085F0173FD23CD577DD5C8475B6D"
        self.passphrase = "Qian159."
        self.base_url = "https://www.okx.com"
        
        # 稳健连接
        self.session = requests.Session()
        self.session.trust_env = False
    
    def test_final_api_thoroughly(self):
        """彻底测试最终API凭据"""
        print("🔍 使用老板最新API凭据彻底测试OKX连接...")
        print("=" * 60)
        
        test_results = {}
        
        # 测试1: 基础连接测试
        print("\n1. 基础连接测试...")
        basic_result = self.test_basic_connection()
        test_results['basic'] = basic_result
        
        # 测试2: 模拟交易头测试
        print("\n2. 模拟交易头测试...")
        simulated_result = self.test_simulated_header()
        test_results['simulated'] = simulated_result
        
        # 测试3: 全面端点测试
        print("\n3. 全面端点测试...")
        endpoints_result = self.test_comprehensive_endpoints()
        test_results['endpoints'] = endpoints_result
        
        # 测试4: 错误分析
        print("\n4. 详细错误分析...")
        error_analysis = self.analyze_errors()
        test_results['error_analysis'] = error_analysis
        
        return test_results
    
    def test_basic_connection(self):
        """测试基础连接"""
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
                    print(f"   ✅ 基础连接: 成功")
                    balance_info = self.parse_balance_data(data)
                    return {'success': True, 'data': balance_info}
                else:
                    error_msg = data.get('msg', '未知错误')
                    error_code = data.get('code', '未知')
                    print(f"   ❌ 基础连接: {error_code} - {error_msg}")
                    return {'success': False, 'error': f'{error_code} - {error_msg}'}
            else:
                print(f"   ❌ 基础连接: HTTP {response.status_code}")
                
                # 详细分析响应
                try:
                    error_data = response.json()
                    print(f"      错误代码: {error_data.get('code')}")
                    print(f"      错误信息: {error_data.get('msg')}")
                except:
                    print(f"      原始响应: {response.text}")
                
                return {'success': False, 'error': f'HTTP {response.status_code}'}
                
        except Exception as e:
            print(f"   ❌ 基础连接: {e}")
            return {'success': False, 'error': str(e)}
    
    def test_simulated_header(self):
        """测试模拟交易头"""
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
                    print(f"   ✅ 模拟头连接: 成功")
                    balance_info = self.parse_balance_data(data)
                    return {'success': True, 'data': balance_info}
                else:
                    error_msg = data.get('msg', '未知错误')
                    error_code = data.get('code', '未知')
                    print(f"   ❌ 模拟头连接: {error_code} - {error_msg}")
                    return {'success': False, 'error': f'{error_code} - {error_msg}'}
            else:
                print(f"   ❌ 模拟头连接: HTTP {response.status_code}")
                
                # 详细分析响应
                try:
                    error_data = response.json()
                    print(f"      错误代码: {error_data.get('code')}")
                    print(f"      错误信息: {error_data.get('msg')}")
                except:
                    print(f"      原始响应: {response.text}")
                
                return {'success': False, 'error': f'HTTP {response.status_code}'}
                
        except Exception as e:
            print(f"   ❌ 模拟头连接: {e}")
            return {'success': False, 'error': str(e)}
    
    def test_comprehensive_endpoints(self):
        """测试全面端点"""
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
    
    def analyze_errors(self):
        """分析错误"""
        print("   详细分析认证错误...")
        
        # 测试不同的配置组合
        configs = [
            {
                'name': '标准配置',
                'headers': {
                    'OK-ACCESS-KEY': self.api_key,
                    'OK-ACCESS-SIGN': '',
                    'OK-ACCESS-TIMESTAMP': '',
                    'OK-ACCESS-PASSPHRASE': self.passphrase,
                    'Content-Type': 'application/json'
                }
            },
            {
                'name': '模拟头配置',
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
                'name': '小写头配置',
                'headers': {
                    'ok-access-key': self.api_key,
                    'ok-access-sign': '',
                    'ok-access-timestamp': '',
                    'ok-access-passphrase': self.passphrase,
                    'content-type': 'application/json',
                    'x-simulated-trading': '1'
                }
            }
        ]
        
        for config in configs:
            print(f"\n      测试 {config['name']}...")
            
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
                if 'OK-ACCESS-SIGN' in headers:
                    headers['OK-ACCESS-SIGN'] = signature
                if 'ok-access-sign' in headers:
                    headers['ok-access-sign'] = signature
                if 'OK-ACCESS-TIMESTAMP' in headers:
                    headers['OK-ACCESS-TIMESTAMP'] = timestamp
                if 'ok-access-timestamp' in headers:
                    headers['ok-access-timestamp'] = timestamp
                
                url = f"{self.base_url}{request_path}"
                response = self.session.get(url, headers=headers, timeout=10)
                
                print(f"         HTTP状态码: {response.status_code}")
                
                if response.status_code != 200:
                    try:
                        error_data = response.json()
                        print(f"         错误代码: {error_data.get('code')}")
                        print(f"         错误信息: {error_data.get('msg')}")
                    except:
                        print(f"         原始响应: {response.text}")
                
            except Exception as e:
                print(f"         异常: {e}")
        
        return {'analysis_complete': True}
    
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
    
    def generate_final_report(self, test_results):
        """生成最终报告"""
        print("\n💰 【虞姬OKX最终API凭据测试报告】")
        print(f"📅 报告时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)
        
        # API凭据状态
        print("\n🔑 【API凭据状态】")
        basic_success = test_results['basic'].get('success', False)
        simulated_success = test_results['simulated'].get('success', False)
        
        if basic_success or simulated_success:
            print("   ✅ API凭据连接成功!")
            
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
            print("   ❌ API凭据连接失败")
            print(f"   基础连接错误: {test_results['basic'].get('error')}")
            print(f"   模拟头连接错误: {test_results['simulated'].get('error')}")
        
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
        
        # 根本原因分析
        print(f"\n🔍 【根本原因分析】")
        if not (basic_success or simulated_success):
            print("   🔧 问题根本原因: 模拟账号API配置问题")
            print("   💡 可能原因:")
            print("      • 模拟账号状态异常")
            print("      • API权限设置不完整")
            print("      • IP白名单未配置")
            print("      • 模拟账号需要手动激活")
        
        # 最终解决方案
        print(f"\n🚀 【最终解决方案】")
        if basic_success or simulated_success:
            print("   ✅ API凭据有效")
            print("   🎯 可以立即开始真实模拟交易")
            print("   📈 启动10U高倍合约量化交易")
        else:
            print("   🔧 API凭据无效")
            print("   📋 必须重新配置模拟账号:")
            print("      1. 手动登录OKX模拟交易页面验证")
            print("      2. 确认模拟账号可正常访问")
            print("      3. 重新生成API密钥")
            print("      4. 设置极简Passphrase")
            print("      5. 启用所有交易权限")
            print("      6. 添加服务器IP到白名单")
        
        print("\n" + "=" * 70)
    
    def run_final_api_test(self):
        """运行最终API测试"""
        print("🚀 虞姬OKX最终API凭据测试系统")
        print(f"⏰ 测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)
        
        # 彻底测试最终API凭据
        test_results = self.test_final_api_thoroughly()
        
        # 生成最终报告
        self.generate_final_report(test_results)
        
        print("\n" + "=" * 70)
        
        # 总结
        if test_results['basic'].get('success') or test_results['simulated'].get('success'):
            print("🎉 最终API凭据连接成功! 可以立即开始模拟交易!")
            return True
        else:
            print("⚠️ 最终API凭据连接失败，必须重新配置模拟账号")
            return False

# 立即运行最终API测试
def test_okx_final_api():
    """测试OKX最终API"""
    print("🔑 立即测试虞姬OKX最终API凭据...")
    
    tester = OKXFinalAPITest()
    
    try:
        success = tester.run_final_api_test()
        return success
    except Exception as e:
        print(f"❌ 测试异常: {e}")
        return False

if __name__ == "__main__":
    test_okx_final_api()