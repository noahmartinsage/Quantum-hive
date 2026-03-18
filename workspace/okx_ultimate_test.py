#!/usr/bin/env python3
"""
虞姬OKX终极测试
使用老板提供的最新OKX凭据进行终极测试
"""

import time
import hmac
import hashlib
import requests
import json
from datetime import datetime

class OKXUltimateTest:
    def __init__(self):
        # 老板提供的最新OKX凭据
        self.api_key = "cefedac1-1d25-4fae-861d-9f006e4cd654"
        self.secret = "EE66B6A88F9E57FBCAE6219081DABDE1"
        self.passphrase = "Qian1314."
        self.base_url = "https://www.okx.com"
        
        # 稳健连接
        self.session = requests.Session()
        self.session.trust_env = False
    
    def test_ultimate_connection(self):
        """终极连接测试"""
        print("🔍 虞姬OKX终极连接测试...")
        print("=" * 60)
        
        test_results = {}
        
        # 测试1: 签名验证测试
        print("\n1. 签名验证测试...")
        signature_test = self.test_signature_verification()
        test_results['signature'] = signature_test
        
        # 测试2: 模拟交易全面测试
        print("\n2. 模拟交易全面测试...")
        simulated_test = self.test_simulated_trading()
        test_results['simulated'] = simulated_test
        
        # 测试3: 公开接口验证
        print("\n3. 公开接口验证...")
        public_test = self.test_public_interfaces()
        test_results['public'] = public_test
        
        return test_results
    
    def test_signature_verification(self):
        """测试签名验证"""
        print("   测试签名算法...")
        
        try:
            timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
            request_path = "/api/v5/account/balance"
            
            # 生成签名
            message = timestamp + 'GET' + request_path
            print(f"      签名消息: {message}")
            print(f"      Secret: {self.secret}")
            
            signature = hmac.new(
                self.secret.encode('utf-8'),
                message.encode('utf-8'),
                hashlib.sha256
            ).hexdigest()
            
            print(f"      生成签名: {signature}")
            
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
            
            print(f"      请求URL: {url}")
            print(f"      请求头: {headers}")
            
            if response.status_code == 200:
                data = response.json()
                if data.get('code') == '0':
                    print(f"      ✅ 签名验证: 成功")
                    return {'success': True, 'data': data}
                else:
                    error_msg = data.get('msg', '未知错误')
                    error_code = data.get('code', '未知')
                    print(f"      ❌ 签名验证: {error_code} - {error_msg}")
                    return {'success': False, 'error': f'{error_code} - {error_msg}'}
            else:
                print(f"      ❌ 签名验证: HTTP {response.status_code}")
                
                # 详细分析响应
                try:
                    error_data = response.json()
                    print(f"         错误代码: {error_data.get('code')}")
                    print(f"         错误信息: {error_data.get('msg')}")
                except:
                    print(f"         原始响应: {response.text}")
                
                return {'success': False, 'error': f'HTTP {response.status_code}'}
                
        except Exception as e:
            print(f"      ❌ 签名验证: {e}")
            return {'success': False, 'error': str(e)}
    
    def test_simulated_trading(self):
        """测试模拟交易"""
        print("   测试模拟交易功能...")
        
        endpoints = [
            ("/api/v5/account/balance", "余额查询"),
            ("/api/v5/account/config", "配置查询"),
            ("/api/v5/account/positions", "持仓查询"),
            ("/api/v5/trade/orders-pending", "挂单查询"),
            ("/api/v5/asset/balances", "资产余额")
        ]
        
        results = {}
        
        for endpoint, description in endpoints:
            print(f"\n      测试 {description}...")
            
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
                        print(f"         ✅ {description}: 成功")
                        
                        # 解析余额数据
                        if 'balance' in endpoint:
                            balance_info = self.parse_balance_data(data)
                            if balance_info:
                                print(f"            总资产: {balance_info['total_equity']:.2f} USDT")
                        
                        results[description] = {'success': True, 'data': data}
                    else:
                        error_msg = data.get('msg', '未知错误')
                        error_code = data.get('code', '未知')
                        print(f"         ❌ {description}: {error_code} - {error_msg}")
                        results[description] = {'success': False, 'error': f'{error_code} - {error_msg}'}
                else:
                    print(f"         ❌ {description}: HTTP {response.status_code}")
                    results[description] = {'success': False, 'error': f'HTTP {response.status_code}'}
                    
            except Exception as e:
                print(f"         ❌ {description}: {e}")
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
    
    def generate_ultimate_report(self, test_results):
        """生成终极报告"""
        print("\n💰 【虞姬OKX终极连接测试报告】")
        print(f"📅 报告时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)
        
        # 签名验证结果
        print("\n🔑 【签名验证结果】")
        signature_success = test_results['signature'].get('success', False)
        
        if signature_success:
            print("   ✅ 签名验证成功!")
            
            # 显示余额信息
            balance_info = test_results['signature']['data']
            if balance_info:
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
            print("   ❌ 签名验证失败")
            print(f"   错误信息: {test_results['signature'].get('error')}")
        
        # 模拟交易结果
        print(f"\n🔧 【模拟交易测试结果】")
        simulated_results = test_results['simulated']
        successful_endpoints = []
        failed_endpoints = []
        
        for endpoint, result in simulated_results.items():
            if result.get('success'):
                successful_endpoints.append(endpoint)
            else:
                failed_endpoints.append(endpoint)
        
        print(f"   成功端点: {len(successful_endpoints)}/{len(simulated_results)}")
        print(f"   失败端点: {len(failed_endpoints)}/{len(simulated_results)}")
        
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
        
        # 根本原因分析
        print(f"\n🔍 【根本原因分析】")
        if not signature_success:
            print("   🔧 问题根本原因: 签名验证失败")
            print("   💡 可能原因:")
            print("      • Secret密钥格式不正确")
            print("      • 签名算法有误")
            print("      • 时间戳格式问题")
            print("      • API权限设置不完整")
        
        # 最终解决方案
        print(f"\n🚀 【终极解决方案】")
        if signature_success:
            print("   ✅ OKX凭据有效")
            print("   🎯 可以立即开始真实模拟交易")
            print("   📈 启动10U高倍合约量化交易")
        else:
            print("   🔧 OKX凭据无效")
            print("   📋 必须彻底重新配置:")
            print("      1. 手动登录OKX模拟交易页面")
            print("      2. 重新生成API密钥")
            print("      3. 设置极简Passphrase")
            print("      4. 启用所有交易权限")
            print("      5. 添加服务器IP到白名单")
            print("      6. 确认Secret密钥正确复制")
        
        print("\n" + "=" * 70)
    
    def run_ultimate_test(self):
        """运行终极测试"""
        print("🚀 虞姬OKX终极连接测试系统")
        print(f"⏰ 测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)
        
        # 终极连接测试
        test_results = self.test_ultimate_connection()
        
        # 生成终极报告
        self.generate_ultimate_report(test_results)
        
        print("\n" + "=" * 70)
        
        # 总结
        if test_results['signature'].get('success'):
            print("🎉 OKX凭据连接成功! 可以立即开始模拟交易!")
            return True
        else:
            print("⚠️ OKX凭据连接失败，必须重新配置模拟账号")
            return False

# 立即运行终极测试
def test_okx_ultimate():
    """测试OKX终极连接"""
    print("🔑 立即测试虞姬OKX终极连接...")
    
    tester = OKXUltimateTest()
    
    try:
        success = tester.run_ultimate_test()
        return success
    except Exception as e:
        print(f"❌ 测试异常: {e}")
        return False

if __name__ == "__main__":
    test_okx_ultimate()