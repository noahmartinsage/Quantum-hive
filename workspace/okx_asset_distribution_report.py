#!/usr/bin/env python3
"""
虞姬OKX模拟账号资产分布报告
检查并汇报模拟账号内的资产分布情况
"""

import time
import hmac
import hashlib
import requests
import json
from datetime import datetime

class OKXAssetDistributionReport:
    def __init__(self):
        # OKX模拟账号API配置
        self.api_key = "9173aacb-75b5-4377-b682-2835afb8be6f"
        self.secret = "F7C576C3759C919A266CF8735B5AF9BC"
        self.passphrase = "Qian1314."
        self.base_url = "https://www.okx.com"
        
        # 稳健连接
        self.session = requests.Session()
        self.session.trust_env = False
    
    def get_comprehensive_asset_data(self):
        """获取全面的资产数据"""
        print("🔍 获取OKX模拟账号全面资产数据...")
        print("=" * 60)
        
        asset_data = {}
        
        # 1. 获取账户余额
        print("\n1. 获取账户余额信息...")
        balance_data = self.get_account_balance()
        asset_data['balance'] = balance_data
        
        # 2. 获取持仓信息
        print("\n2. 获取持仓信息...")
        positions_data = self.get_positions()
        asset_data['positions'] = positions_data
        
        # 3. 获取资产余额
        print("\n3. 获取资产余额...")
        asset_balances = self.get_asset_balances()
        asset_data['asset_balances'] = asset_balances
        
        # 4. 获取挂单信息
        print("\n4. 获取挂单信息...")
        pending_orders = self.get_pending_orders()
        asset_data['pending_orders'] = pending_orders
        
        return asset_data
    
    def get_account_balance(self):
        """获取账户余额"""
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
                    balance_info = self.parse_balance_data(data)
                    print(f"   ✅ 余额查询成功")
                    return {'success': True, 'data': balance_info}
                else:
                    error_msg = data.get('msg', '未知错误')
                    print(f"   ❌ 余额查询失败: {error_msg}")
                    return {'success': False, 'error': error_msg}
            else:
                print(f"   ❌ 余额查询失败: HTTP {response.status_code}")
                return {'success': False, 'error': f'HTTP {response.status_code}'}
                
        except Exception as e:
            print(f"   ❌ 余额查询异常: {e}")
            return {'success': False, 'error': str(e)}
    
    def get_positions(self):
        """获取持仓信息"""
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
                'Content-Type': 'application/json'
            }
            
            url = f"{self.base_url}{request_path}"
            response = self.session.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('code') == '0':
                    positions = data.get('data', [])
                    print(f"   ✅ 持仓查询成功")
                    print(f"      持仓数量: {len(positions)}")
                    return {'success': True, 'data': positions}
                else:
                    error_msg = data.get('msg', '未知错误')
                    print(f"   ❌ 持仓查询失败: {error_msg}")
                    return {'success': False, 'error': error_msg}
            else:
                print(f"   ❌ 持仓查询失败: HTTP {response.status_code}")
                return {'success': False, 'error': f'HTTP {response.status_code}'}
                
        except Exception as e:
            print(f"   ❌ 持仓查询异常: {e}")
            return {'success': False, 'error': str(e)}
    
    def get_asset_balances(self):
        """获取资产余额"""
        try:
            timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
            request_path = "/api/v5/asset/balances"
            
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
                    balances = data.get('data', [])
                    print(f"   ✅ 资产余额查询成功")
                    return {'success': True, 'data': balances}
                else:
                    error_msg = data.get('msg', '未知错误')
                    print(f"   ❌ 资产余额查询失败: {error_msg}")
                    return {'success': False, 'error': error_msg}
            else:
                print(f"   ❌ 资产余额查询失败: HTTP {response.status_code}")
                return {'success': False, 'error': f'HTTP {response.status_code}'}
                
        except Exception as e:
            print(f"   ❌ 资产余额查询异常: {e}")
            return {'success': False, 'error': str(e)}
    
    def get_pending_orders(self):
        """获取挂单信息"""
        try:
            timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
            request_path = "/api/v5/trade/orders-pending"
            
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
                    orders = data.get('data', [])
                    print(f"   ✅ 挂单查询成功")
                    print(f"      挂单数量: {len(orders)}")
                    return {'success': True, 'data': orders}
                else:
                    error_msg = data.get('msg', '未知错误')
                    print(f"   ❌ 挂单查询失败: {error_msg}")
                    return {'success': False, 'error': error_msg}
            else:
                print(f"   ❌ 挂单查询失败: HTTP {response.status_code}")
                return {'success': False, 'error': f'HTTP {response.status_code}'}
                
        except Exception as e:
            print(f"   ❌ 挂单查询异常: {e}")
            return {'success': False, 'error': str(e)}
    
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
    
    def generate_asset_distribution_report(self, asset_data):
        """生成资产分布报告"""
        print("\n💰 【虞姬OKX模拟账号资产分布报告】")
        print(f"📅 报告时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)
        
        # 账户余额分析
        if asset_data['balance'].get('success'):
            balance_info = asset_data['balance']['data']
            
            print("\n📊 【账户余额总览】")
            print(f"   总权益: {balance_info['total_equity']:.2f} USDT")
            print(f"   独立权益: {balance_info['iso_equity']:.2f} USDT")
            print(f"   调整权益: {balance_info['adj_equity']:.2f} USDT")
            print(f"   订单冻结: {balance_info['ord_frozen']:.2f} USDT")
            print(f"   初始保证金: {balance_info['imr']:.2f} USDT")
            print(f"   维持保证金: {balance_info['mmr']:.2f} USDT")
            print(f"   保证金率: {balance_info['mgn_ratio']:.4f}")
            
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
            print("\n❌ 【账户余额】")
            print(f"   无法获取余额信息: {asset_data['balance'].get('error')}")
        
        # 持仓信息分析
        if asset_data['positions'].get('success'):
            positions = asset_data['positions']['data']
            
            print(f"\n📈 【持仓分布】")
            print(f"   持仓数量: {len(positions)}")
            
            if positions:
                total_position_value = 0
                for position in positions:
                    inst_id = position.get('instId', '')
                    pos = float(position.get('pos', '0'))
                    avg_px = float(position.get('avgPx', '0'))
                    upl = float(position.get('upl', '0'))
                    
                    if pos != 0:
                        position_value = abs(pos * avg_px)
                        total_position_value += position_value
                        
                        print(f"\n   {inst_id}:")
                        print(f"      持仓量: {pos}")
                        print(f"      均价: {avg_px:.2f}")
                        print(f"      未实现盈亏: {upl:.4f} USDT")
                        print(f"      持仓价值: {position_value:.2f} USDT")
                
                print(f"\n   📊 总持仓价值: {total_position_value:.2f} USDT")
            else:
                print("   📊 当前无持仓")
        else:
            print(f"\n❌ 【持仓信息】")
            print(f"   无法获取持仓信息: {asset_data['positions'].get('error')}")
        
        # 资产余额分析
        if asset_data['asset_balances'].get('success'):
            asset_balances = asset_data['asset_balances']['data']
            
            print(f"\n💼 【资产余额分布】")
            total_assets = 0
            for asset in asset_balances:
                ccy = asset.get('ccy', '')
                bal = float(asset.get('bal', '0'))
                
                if bal > 0:
                    total_assets += bal
                    print(f"   {ccy}: {bal:.4f}")
            
            print(f"\n   📊 总资产余额: {total_assets:.4f}")
        else:
            print(f"\n❌ 【资产余额】")
            print(f"   无法获取资产余额: {asset_data['asset_balances'].get('error')}")
        
        # 挂单信息分析
        if asset_data['pending_orders'].get('success'):
            pending_orders = asset_data['pending_orders']['data']
            
            print(f"\n📋 【挂单分布】")
            print(f"   挂单数量: {len(pending_orders)}")
            
            if pending_orders:
                total_order_value = 0
                for order in pending_orders:
                    inst_id = order.get('instId', '')
                    sz = float(order.get('sz', '0'))
                    px = float(order.get('px', '0'))
                    side = order.get('side', '')
                    
                    order_value = sz * px
                    total_order_value += order_value
                    
                    print(f"\n   {inst_id}:")
                    print(f"      方向: {side}")
                    print(f"      数量: {sz}")
                    print(f"      价格: {px:.2f}")
                    print(f"      挂单价值: {order_value:.2f} USDT")
                
                print(f"\n   📊 总挂单价值: {total_order_value:.2f} USDT")
            else:
                print("   📊 当前无挂单")
        else:
            print(f"\n❌ 【挂单信息】")
            print(f"   无法获取挂单信息: {asset_data['pending_orders'].get('error')}")
        
        # 总结分析
        print(f"\n🎯 【资产分布总结】")
        if asset_data['balance'].get('success'):
            balance_info = asset_data['balance']['data']
            
            # 计算各类资产占比
            total_equity = balance_info['total_equity']
            
            print(f"   总资产规模: {total_equity:.2f} USDT")
            
            if total_equity > 0:
                # 可用资金占比
                available_ratio = 0
                for currency in balance_info['currency_details']:
                    if currency['currency'] == 'USDT':
                        available_ratio = currency['available'] / total_equity
                        break
                
                print(f"   可用资金占比: {available_ratio*100:.2f}%")
                print(f"   冻结资金占比: {(1 - available_ratio)*100:.2f}%")
                
                # 交易建议
                print(f"\n💡 【交易建议】")
                if available_ratio > 0.5:
                    print("   ✅ 可用资金充足，可增加交易仓位")
                elif available_ratio > 0.2:
                    print("   ⚠️ 可用资金适中，保持当前仓位")
                else:
                    print("   🔴 可用资金不足，建议减少仓位")
        
        print("\n" + "=" * 70)
    
    def run_asset_distribution_report(self):
        """运行资产分布报告"""
        print("🚀 虞姬OKX模拟账号资产分布报告")
        print(f"⏰ 报告时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)
        
        # 获取全面资产数据
        asset_data = self.get_comprehensive_asset_data()
        
        # 生成资产分布报告
        self.generate_asset_distribution_report(asset_data)
        
        print("\n" + "=" * 70)

# 立即运行资产分布报告
def generate_okx_asset_report():
    """生成OKX资产报告"""
    print("🔍 立即生成虞姬OKX模拟账号资产分布报告...")
    
    reporter = OKXAssetDistributionReport()
    
    try:
        reporter.run_asset_distribution_report()
    except Exception as e:
        print(f"❌ 资产报告生成异常: {e}")

if __name__ == "__main__":
    generate_okx_asset_report()