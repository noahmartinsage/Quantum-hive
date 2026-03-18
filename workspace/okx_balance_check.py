#!/usr/bin/env python3
"""
虞姬OKX账户余额状态检查
使用稳健连接架构检查OKX账户余额
"""

import time
import hmac
import hashlib
import requests
import json
from datetime import datetime

class OKXBalanceChecker:
    def __init__(self):
        # OKX配置
        self.api_key = "e4753767-b2f7-4495-b2d9-0166238b1076"
        self.secret = "FBBB847F11CC85396F411B1D52E35A1E"
        self.passphrase = "Abc123456"
        self.base_url = "https://www.okx.com"
        
        # 稳健连接配置
        self.session = requests.Session()
        self.session.trust_env = False  # 不信任环境代理
        self.timeout = 15
    
    def check_balance_with_robust_connection(self):
        """使用稳健连接检查余额"""
        print("🔍 使用虞姬稳健连接架构检查OKX账户余额...")
        print("=" * 60)
        
        try:
            # 生成认证信息
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
            
            # 使用稳健连接发送请求
            print("\n1. 发送余额查询请求...")
            response = self.session.get(url, headers=headers, timeout=self.timeout)
            
            print(f"   HTTP状态码: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('code') == '0':
                    print("   ✅ API请求成功")
                    return self.parse_balance_data(data)
                else:
                    error_code = data.get('code')
                    error_msg = data.get('msg')
                    print(f"   ❌ API错误: {error_code} - {error_msg}")
                    
                    # 具体错误处理
                    if error_code == '50111':
                        print("   💡 建议: 检查Passphrase是否正确")
                    elif error_code == '50114':
                        print("   💡 建议: 验证API密钥有效性")
                    elif error_code == '50014':
                        print("   💡 建议: 检查IP白名单设置")
                    elif error_code == '50113':
                        print("   💡 建议: 确认交易权限已启用")
                    
                    return None
            else:
                print(f"   ❌ HTTP错误: {response.status_code}")
                print(f"   响应内容: {response.text}")
                return None
                
        except requests.exceptions.Timeout:
            print("   ❌ 请求超时")
            print("   💡 建议: 增加超时时间或检查网络连接")
            return None
        except requests.exceptions.ConnectionError:
            print("   ❌ 连接错误")
            print("   💡 建议: 检查网络连接和防火墙设置")
            return None
        except Exception as e:
            print(f"   ❌ 请求异常: {e}")
            return None
    
    def parse_balance_data(self, data):
        """解析余额数据"""
        print("\n2. 解析账户余额数据...")
        
        try:
            balance_data = data.get('data', [{}])[0]
            
            if not balance_data:
                print("   ⚠️ 账户数据为空")
                return None
            
            # 提取详细信息
            details = balance_data.get('details', [])
            
            if not details:
                print("   ⚠️ 余额详情为空")
                return None
            
            print("   ✅ 余额数据解析成功")
            
            # 格式化余额信息
            balance_info = {
                'total_equity': balance_data.get('totalEq', '0'),
                'iso_equity': balance_data.get('isoEq', '0'),
                'adj_equity': balance_data.get('adjEq', '0'),
                'ord_frozen': balance_data.get('ordFroz', '0'),
                'imr': balance_data.get('imr', '0'),
                'mmr': balance_data.get('mmr', '0'),
                'mgn_ratio': balance_data.get('mgnRatio', '0'),
                'currency_details': []
            }
            
            for detail in details:
                currency_info = {
                    'currency': detail.get('ccy', ''),
                    'balance': detail.get('cashBal', '0'),
                    'available': detail.get('availEq', '0'),
                    'frozen': detail.get('frozenBal', '0'),
                    'equity': detail.get('eq', '0')
                }
                balance_info['currency_details'].append(currency_info)
            
            return balance_info
            
        except Exception as e:
            print(f"   ❌ 数据解析异常: {e}")
            return None
    
    def generate_balance_report(self, balance_info):
        """生成余额报告"""
        if not balance_info:
            print("\n❌ 无法获取余额信息")
            return
        
        print("\n💰 【OKX账户余额状态报告】")
        print(f"📅 报告时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)
        
        # 总体账户信息
        print("\n📊 【总体账户信息】")
        print(f"   总权益: {balance_info['total_equity']} USDT")
        print(f"   独立权益: {balance_info['iso_equity']} USDT")
        print(f"   调整权益: {balance_info['adj_equity']} USDT")
        print(f"   订单冻结: {balance_info['ord_frozen']} USDT")
        print(f"   初始保证金: {balance_info['imr']} USDT")
        print(f"   维持保证金: {balance_info['mmr']} USDT")
        print(f"   保证金率: {balance_info['mgn_ratio']}%")
        
        # 货币余额详情
        print("\n💱 【货币余额详情】")
        
        if not balance_info['currency_details']:
            print("   ⚠️ 无货币余额信息")
            return
        
        for currency in balance_info['currency_details']:
            if currency['currency'] == 'USDT':
                print(f"\n   💰 {currency['currency']}:")
                print(f"      余额: {currency['balance']} USDT")
                print(f"      可用: {currency['available']} USDT")
                print(f"      冻结: {currency['frozen']} USDT")
                print(f"      权益: {currency['equity']} USDT")
            elif float(currency['balance']) > 0 or float(currency['available']) > 0:
                print(f"\n   💰 {currency['currency']}:")
                print(f"      余额: {currency['balance']}")
                print(f"      可用: {currency['available']}")
                print(f"      冻结: {currency['frozen']}")
                print(f"      权益: {currency['equity']}")
    
    def check_account_config(self):
        """检查账户配置"""
        print("\n🔧 【账户配置检查】")
        
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
            response = self.session.get(url, headers=headers, timeout=self.timeout)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('code') == '0':
                    config_data = data.get('data', [{}])[0]
                    acct_lv = config_data.get('acctLv', '')
                    pos_mode = config_data.get('posMode', '')
                    
                    print(f"   账户等级: {acct_lv}")
                    print(f"   持仓模式: {pos_mode}")
                    
                    if acct_lv in ['1', '2', '3', '4']:
                        print("   ✅ 账户等级支持交易")
                    else:
                        print("   ⚠️ 账户等级可能不支持交易")
                else:
                    print(f"   ❌ 配置查询失败: {data.get('msg')}")
            else:
                print(f"   ❌ 配置查询HTTP错误: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ 配置查询异常: {e}")
    
    def run_complete_balance_check(self):
        """运行完整余额检查"""
        print("🚀 虞姬OKX账户余额状态检查")
        print(f"⏰ 检查时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)
        
        # 检查余额
        balance_info = self.check_balance_with_robust_connection()
        
        # 生成报告
        self.generate_balance_report(balance_info)
        
        # 检查账户配置
        self.check_account_config()
        
        print("\n" + "=" * 70)
        
        if balance_info:
            print("✅ 余额检查完成!")
            
            # 提取USDT余额用于交易
            usdt_balance = None
            for currency in balance_info['currency_details']:
                if currency['currency'] == 'USDT':
                    usdt_balance = currency['available']
                    break
            
            if usdt_balance:
                print(f"💰 可用USDT余额: {usdt_balance} USDT")
                print("🚀 可以立即开始真实交易!")
        else:
            print("⚠️ 余额检查失败，但模拟交易系统继续运行")
            print("💡 建议: 检查API配置或使用模拟交易")

# 立即运行余额检查
def check_okx_balance():
    """检查OKX余额"""
    print("🔍 立即检查虞姬OKX账户余额状态...")
    
    checker = OKXBalanceChecker()
    
    try:
        checker.run_complete_balance_check()
    except Exception as e:
        print(f"❌ 余额检查异常: {e}")

if __name__ == "__main__":
    check_okx_balance()