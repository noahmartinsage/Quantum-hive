#!/usr/bin/env python3
"""
虞姬OKX模拟盘交易修复系统
在请求头中添加 x-simulated-trading: 1 解决认证问题
"""

import time
import hmac
import hashlib
import requests
import json
from datetime import datetime

class OKXSimulatedTradingFix:
    def __init__(self):
        # OKX模拟账号API配置
        self.api_key = "9173aacb-75b5-4377-b682-2835afb8be6f"
        self.secret = "F7C576C3759C919A266CF8735B5AF9BC"
        self.passphrase = "Qian1314."
        self.base_url = "https://www.okx.com"
        
        # 稳健连接
        self.session = requests.Session()
        self.session.trust_env = False
    
    def test_simulated_trading_header(self):
        """测试模拟交易头信息"""
        print("🔍 测试OKX模拟盘交易头信息 x-simulated-trading: 1 ...")
        print("=" * 60)
        
        # 测试1: 标准请求（无模拟头）
        print("\n1. 测试标准请求（无模拟头）...")
        standard_result = self.test_standard_request()
        
        # 测试2: 模拟交易请求（带模拟头）
        print("\n2. 测试模拟交易请求（带模拟头）...")
        simulated_result = self.test_simulated_request()
        
        # 测试3: 全面端点测试
        print("\n3. 测试全面端点...")
        comprehensive_results = self.test_comprehensive_endpoints()
        
        return {
            'standard': standard_result,
            'simulated': simulated_result,
            'comprehensive': comprehensive_results
        }
    
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
                    return {'success': True, 'data': data}
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
                'x-simulated-trading': '1'  # 关键：添加模拟交易头
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
                    'x-simulated-trading': '1'  # 关键：添加模拟交易头
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
    
    def generate_simulated_trading_report(self, test_results):
        """生成模拟交易报告"""
        print("\n💰 【虞姬OKX模拟盘交易修复报告】")
        print(f"📅 报告时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)
        
        # 连接状态分析
        print("\n🔗 【连接状态分析】")
        standard_success = test_results['standard'].get('success', False)
        simulated_success = test_results['simulated'].get('success', False)
        
        if not standard_success and simulated_success:
            print("   ✅ 模拟交易头信息修复成功!")
            print("   🔧 问题根本原因: 缺少 x-simulated-trading: 1 头信息")
        elif standard_success and simulated_success:
            print("   ⚠️ 两种请求都成功")
            print("   💡 可能原因: API配置正确，无需模拟头")
        else:
            print("   ❌ 两种请求都失败")
            print("   🔧 可能原因: API配置问题")
        
        # 模拟请求结果
        if test_results['simulated'].get('success'):
            balance_info = test_results['simulated']['data']
            
            print(f"\n📊 【模拟账号资产总览】")
            print(f"   总权益: {balance_info['total_equity']:.2f} USDT")
            print(f"   独立权益: {balance_info['iso_equity']:.2f} USDT")
            print(f"   调整权益: {balance_info['adj_equity']:.2f} USDT")
            print(f"   订单冻结: {balance_info['ord_frozen']:.2f} USDT")
            
            # 货币余额详情
            print(f"\n💱 【货币余额分布】")
            for currency in balance_info['currency_details']:
                if currency['balance'] > 0:
                    print(f"   {currency['currency']}:")
                    print(f"      余额: {currency['balance']:.4f}")
                    print(f"      可用: {currency['available']:.4f}")
                    print(f"      冻结: {currency['frozen']:.4f}")
                    print(f"      权益: {currency['equity']:.4f}")
        
        # 全面端点测试结果
        print(f"\n🔧 【全面端点测试结果】")
        successful_endpoints = []
        failed_endpoints = []
        
        for endpoint, result in test_results['comprehensive'].items():
            if result.get('success'):
                successful_endpoints.append(endpoint)
            else:
                failed_endpoints.append(endpoint)
        
        print(f"   成功端点: {len(successful_endpoints)}/{len(test_results['comprehensive'])}")
        print(f"   失败端点: {len(failed_endpoints)}/{len(test_results['comprehensive'])}")
        
        if successful_endpoints:
            print(f"\n   ✅ 成功端点:")
            for endpoint in successful_endpoints:
                print(f"      • {endpoint}")
        
        if failed_endpoints:
            print(f"\n   ❌ 失败端点:")
            for endpoint in failed_endpoints:
                print(f"      • {endpoint}")
        
        # 修复建议
        print(f"\n💡 【修复建议】")
        if simulated_success:
            print("   ✅ 模拟交易头信息修复有效")
            print("   🚀 可以立即开始模拟交易")
            print("   📋 在所有模拟交易请求中添加:")
            print("        'x-simulated-trading': '1'")
        else:
            print("   🔧 需要进一步调试")
            print("   📋 检查步骤:")
            print("      1. 确认模拟账号状态")
            print("      2. 验证API权限设置")
            print("      3. 检查Passphrase准确性")
            print("      4. 联系OKX客服")
        
        print("\n" + "=" * 70)
    
    def run_simulated_trading_fix(self):
        """运行模拟交易修复"""
        print("🚀 虞姬OKX模拟盘交易修复系统")
        print(f"⏰ 修复时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)
        
        # 测试模拟交易头信息
        test_results = self.test_simulated_trading_header()
        
        # 生成模拟交易报告
        self.generate_simulated_trading_report(test_results)
        
        print("\n" + "=" * 70)
        
        # 总结
        if test_results['simulated'].get('success'):
            print("🎉 模拟交易头信息修复成功! 可以立即开始模拟交易!")
            return True
        else:
            print("⚠️ 模拟交易头信息修复失败，需要进一步调试")
            return False

# 立即运行模拟交易修复
def fix_okx_simulated_trading():
    """修复OKX模拟交易"""
    print("🔧 立即修复虞姬OKX模拟盘交易头信息...")
    
    fixer = OKXSimulatedTradingFix()
    
    try:
        success = fixer.run_simulated_trading_fix()
        return success
    except Exception as e:
        print(f"❌ 修复异常: {e}")
        return False

if __name__ == "__main__":
    fix_okx_simulated_trading()