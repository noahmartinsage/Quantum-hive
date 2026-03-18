#!/usr/bin/env python3
"""
虞姬OKX账户状态全面检查
全面检查OKX账户连接状态、余额、配置等信息
"""

import time
import hmac
import hashlib
import requests
import json
from datetime import datetime

class OKXAccountStatusChecker:
    def __init__(self):
        # OKX API配置
        self.api_key = "e4753767-b2f7-4495-b2d9-0166238b1076"
        self.secret = "FBBB847F11CC85396F411B1D52E35A1E"
        self.passphrase = "Abc123456"
        self.base_url = "https://www.okx.com"
        
        # 稳健连接
        self.session = requests.Session()
        self.session.trust_env = False
    
    def check_connection_status(self):
        """检查连接状态"""
        print("🔍 检查OKX账户连接状态...")
        print("=" * 60)
        
        connection_status = {
            'public_api': False,
            'private_api': False,
            'network': False,
            'authentication': False
        }
        
        # 1. 测试公开API
        print("\n1. 测试公开API连接...")
        try:
            url = f"{self.base_url}/api/v5/public/time"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('code') == '0':
                    print("   ✅ 公开API连接正常")
                    connection_status['public_api'] = True
                    connection_status['network'] = True
                else:
                    print(f"   ❌ 公开API错误: {data.get('msg')}")
            else:
                print(f"   ❌ 公开API HTTP错误: {response.status_code}")
        except Exception as e:
            print(f"   ❌ 公开API异常: {e}")
        
        # 2. 测试私有API
        print("\n2. 测试私有API连接...")
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
                    print("   ✅ 私有API连接正常")
                    connection_status['private_api'] = True
                    connection_status['authentication'] = True
                else:
                    error_code = data.get('code')
                    error_msg = data.get('msg')
                    print(f"   ❌ 私有API错误: {error_code} - {error_msg}")
                    
                    if error_code == '50105':
                        print("   💡 问题: Passphrase不正确")
                    elif error_code == '50114':
                        print("   💡 问题: API密钥无效")
                    elif error_code == '50014':
                        print("   💡 问题: IP白名单限制")
            else:
                print(f"   ❌ 私有API HTTP错误: {response.status_code}")
        except Exception as e:
            print(f"   ❌ 私有API异常: {e}")
        
        return connection_status
    
    def get_account_balance(self):
        """获取账户余额"""
        print("\n3. 获取账户余额信息...")
        
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
                    return self.parse_balance_data(data)
                else:
                    print(f"   ❌ 余额查询失败: {data.get('msg')}")
                    return None
            else:
                print(f"   ❌ 余额查询HTTP错误: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"   ❌ 余额查询异常: {e}")
            return None
    
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
            
            print("   ✅ 余额数据解析成功")
            return balance_info
            
        except Exception as e:
            print(f"   ❌ 余额数据解析异常: {e}")
            return None
    
    def get_account_config(self):
        """获取账户配置"""
        print("\n4. 获取账户配置信息...")
        
        try:
            timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
            request_path = "/api/v5/account/config"
            
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
                    return self.parse_config_data(data)
                else:
                    print(f"   ❌ 配置查询失败: {data.get('msg')}")
                    return None
            else:
                print(f"   ❌ 配置查询HTTP错误: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"   ❌ 配置查询异常: {e}")
            return None
    
    def parse_config_data(self, data):
        """解析配置数据"""
        try:
            config_data = data.get('data', [{}])[0]
            
            config_info = {
                'acct_lv': config_data.get('acctLv', ''),
                'pos_mode': config_data.get('posMode', ''),
                'auto_loan': config_data.get('autoLoan', ''),
                'greeks_type': config_data.get('greeksType', ''),
                'level': config_data.get('level', ''),
                'level_temp': config_data.get('levelTmp', '')
            }
            
            print("   ✅ 配置数据解析成功")
            return config_info
            
        except Exception as e:
            print(f"   ❌ 配置数据解析异常: {e}")
            return None
    
    def generate_comprehensive_report(self, connection_status, balance_info, config_info):
        """生成全面报告"""
        print("\n💰 【OKX账户状态全面报告】")
        print(f"📅 报告时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)
        
        # 连接状态
        print("\n🔗 【连接状态】")
        for status, value in connection_status.items():
            icon = "✅" if value else "❌"
            status_text = "正常" if value else "异常"
            print(f"   {icon} {status}: {status_text}")
        
        # 账户余额
        if balance_info:
            print("\n💰 【账户余额】")
            print(f"   总权益: {balance_info['total_equity']:.2f} USDT")
            print(f"   独立权益: {balance_info['iso_equity']:.2f} USDT")
            print(f"   调整权益: {balance_info['adj_equity']:.2f} USDT")
            print(f"   订单冻结: {balance_info['ord_frozen']:.2f} USDT")
            print(f"   初始保证金: {balance_info['imr']:.2f} USDT")
            print(f"   维持保证金: {balance_info['mmr']:.2f} USDT")
            print(f"   保证金率: {balance_info['mgn_ratio']:.2f}%")
            
            # 货币余额详情
            print("\n💱 【货币余额详情】")
            for currency in balance_info['currency_details']:
                if currency['currency'] == 'USDT' or currency['balance'] > 0:
                    print(f"   {currency['currency']}:")
                    print(f"      余额: {currency['balance']:.2f}")
                    print(f"      可用: {currency['available']:.2f}")
                    print(f"      冻结: {currency['frozen']:.2f}")
                    print(f"      权益: {currency['equity']:.2f}")
        else:
            print("\n💰 【账户余额】")
            print("   ⚠️ 无法获取余额信息")
        
        # 账户配置
        if config_info:
            print("\n⚙️ 【账户配置】")
            print(f"   账户等级: {config_info['acct_lv']}")
            print(f"   持仓模式: {config_info['pos_mode']}")
            print(f"   自动借贷: {config_info['auto_loan']}")
            print(f"   Greeks类型: {config_info['greeks_type']}")
            print(f"   等级: {config_info['level']}")
            print(f"   临时等级: {config_info['level_temp']}")
        else:
            print("\n⚙️ 【账户配置】")
            print("   ⚠️ 无法获取配置信息")
        
        # 连接建议
        print("\n💡 【连接建议】")
        if not connection_status['private_api']:
            print("   🔧 私有API连接异常，需要修复:")
            print("      • 验证Passphrase是否正确")
            print("      • 检查API密钥权限")
            print("      • 确认IP白名单设置")
        else:
            print("   ✅ 所有连接正常，可以开始交易")
        
        # 交易建议
        if balance_info and balance_info['total_equity'] > 0:
            print("\n🎯 【交易建议】")
            usdt_balance = None
            for currency in balance_info['currency_details']:
                if currency['currency'] == 'USDT':
                    usdt_balance = currency['available']
                    break
            
            if usdt_balance:
                print(f"   💰 可用USDT余额: {usdt_balance:.2f}")
                print("   🚀 可以立即开始交易!")
            else:
                print("   ⚠️ 未找到可用USDT余额")
    
    def run_complete_status_check(self):
        """运行完整状态检查"""
        print("🚀 虞姬OKX账户状态全面检查")
        print(f"⏰ 检查时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)
        
        # 检查连接状态
        connection_status = self.check_connection_status()
        
        # 获取账户余额
        balance_info = self.get_account_balance()
        
        # 获取账户配置
        config_info = self.get_account_config()
        
        # 生成全面报告
        self.generate_comprehensive_report(connection_status, balance_info, config_info)
        
        print("\n" + "=" * 70)
        
        # 总结
        if connection_status['private_api'] and balance_info:
            print("✅ 账户状态检查完成! 可以立即开始交易!")
        else:
            print("⚠️ 账户连接存在问题，建议修复后再进行交易")

# 立即运行状态检查
def check_okx_account_status():
    """检查OKX账户状态"""
    print("🔍 立即检查虞姬OKX账户状态...")
    
    checker = OKXAccountStatusChecker()
    
    try:
        checker.run_complete_status_check()
    except Exception as e:
        print(f"❌ 状态检查异常: {e}")

if __name__ == "__main__":
    check_okx_account_status()