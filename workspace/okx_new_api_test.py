#!/usr/bin/env python3
"""
虞姬OKX新API凭据测试
使用老板提供的新API凭据测试OKX连接
"""

import time
import hmac
import hashlib
import requests
import json
from datetime import datetime

class OKXNewAPITest:
    def __init__(self):
        # 老板提供的新API凭据
        self.api_key = "8fb83dcd-dc09-4b1f-b39a-85185475cbe1"
        self.secret = "48D4E87E65E19FA992B385DB49EA68DB"
        self.passphrase = "Qian159."
        self.base_url = "https://www.okx.com"
        
        # 稳健连接
        self.session = requests.Session()
        self.session.trust_env = False
    
    def test_new_api_comprehensive(self):
        """全面测试新API凭据"""
        print("🔍 使用老板新API凭据全面测试OKX连接...")
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
        
        # 测试4: 公开接口测试
        print("\n4. 测试公开接口...")
        public_result = self.test_public_interfaces()
        test_results['public'] = public_result
        
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
            response = self.session.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('code') == '0':
                    print(f"   ✅ 标准请求: 成功")
                    balance_info = self.parse_balance_data(data)
                    return {'success': True, 'data': balance_info}
                else:
                    error_msg = data.get('msg', '未知错误')
                    print(f"   ❌ 标准请求: {error_msg}")
                    return {'success': False, 'error': error_msg}
            else:
                print(f"   ❌ 标准请求: HTTP {response.status_code}")
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
            response = self.session.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('code') == '0':
                    print(f"   ✅ 模拟请求: 成功")
                    balance_info = self.parse_balance_data(data)
                    return {'success': True, 'data': balance_info}
                else:
                    error_msg = data.get('msg', '未知错误')
                    print(f"   ❌ 模拟请求: {error_msg}")
                    return {'success': False, 'error': error_msg}
            else:
                print(f"   ❌ 模拟请求: HTTP {response.status_code}")
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
                        print(f"      ❌ {description}: {error_msg}")
                        results[description] = {'success': False, 'error': error_msg}
                else:
                    print(f"      ❌ {description}: HTTP {response.status_code}")
                    results[description] = {'success': False, 'error': f'HTTP {response.status_code}'}
                    
            except Exception as e:
                print(f"      ❌ {description}: {e}")
                results[description] = {'success': False, 'error': str(e)}
        
        return results
    
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
                url = f"{self.base_url}{endpoint}"
                response = self.session.get(url, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get('code') == '0':
                        print(f"      ✅ {description}: 正常")
                        
                        # 解析行情数据
                        if 'ticker' in endpoint:
                            ticker_data = data.get('data', [{}])[0]
                            last_price = float(ticker_data.get('last', '0'))
                            print(f"            当前价格: {last_price:.2f} USDT")
                        
                        results.append({'endpoint': endpoint, 'status': '正常'})
                    else:
                        print(f"      ❌ {description}: {data.get('msg')}")
                        results.append({'endpoint': endpoint, 'status': '错误'})
                else:
                    print(f"      ❌ {description}: HTTP {response.status_code}")
                    results.append({'endpoint': endpoint, 'status': '错误'})
                    
            except Exception as e:
                print(f"      ❌ {description}: {e}")
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
    
    def generate_new_api_report(self, test_results):
        """生成新API报告"""
        print("\n💰 【虞姬OKX新API凭据测试报告】")
        print(f"📅 报告时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)
        
        # 新API凭据状态
        print("\n🔑 【新API凭据状态】")
        standard_success = test_results['standard'].get('success', False)
        simulated_success = test_results['simulated'].get('success', False)
        
        if standard_success or simulated_success:
            print("   ✅ 新API凭据连接成功!")
            
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
            print("   ❌ 新API凭据连接失败")
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
        
        # 公开接口状态
        print(f"\n🌐 【公开接口状态】")
        public_results = test_results['public']
        public_ok = all(r['status'] == '正常' for r in public_results)
        
        if public_ok:
            print("   ✅ 公开接口: 全部正常")
        else:
            print("   ❌ 公开接口: 部分异常")
        
        # 解决方案
        print(f"\n🚀 【立即行动】")
        if standard_success or simulated_success:
            print("   ✅ 新API凭据有效")
            print("   🎯 可以立即开始真实模拟交易")
            print("   📈 启动10U高倍合约量化交易")
        else:
            print("   🔧 新API凭据仍然无效")
            print("   📋 需要重新生成API密钥")
            print("      1. 确认模拟账号可正常访问")
            print("      2. 重新生成API密钥")
            print("      3. 设置简单Passphrase")
            print("      4. 启用完整交易权限")
        
        print("\n" + "=" * 70)
    
    def run_new_api_test(self):
        """运行新API测试"""
        print("🚀 虞姬OKX新API凭据测试系统")
        print(f"⏰ 测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)
        
        # 全面测试新API凭据
        test_results = self.test_new_api_comprehensive()
        
        # 生成新API报告
        self.generate_new_api_report(test_results)
        
        print("\n" + "=" * 70)
        
        # 总结
        if test_results['standard'].get('success') or test_results['simulated'].get('success'):
            print("🎉 新API凭据连接成功! 可以立即开始模拟交易!")
            return True
        else:
            print("⚠️ 新API凭据连接失败，需要重新生成API密钥")
            return False

# 立即运行新API测试
def test_okx_new_api():
    """测试OKX新API"""
    print("🔑 立即测试虞姬OKX新API凭据...")
    
    tester = OKXNewAPITest()
    
    try:
        success = tester.run_new_api_test()
        return success
    except Exception as e:
        print(f"❌ 测试异常: {e}")
        return False

if __name__ == "__main__":
    test_okx_new_api()