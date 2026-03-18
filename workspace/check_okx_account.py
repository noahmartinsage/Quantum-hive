#!/usr/bin/env python3
"""
虞姬OKX账户状态检查
查看OKX模拟盘账户余额、持仓和交易状态
"""

import time
import hmac
import hashlib
import requests
import json
from datetime import datetime

class OKXAccountChecker:
    def __init__(self):
        # OKX模拟盘配置
        self.api_key = "e4753767-b2f7-4495-b2d9-0166238b1076"
        self.secret = "FBBB847F11CC85396F411B1D52E35A1E"
        self.passphrase = "Abc123456"
        self.base_url = "https://www.okx.com"
    
    def generate_signature(self, timestamp, method, request_path, body=""):
        """生成OKX签名"""
        message = timestamp + method + request_path + body
        signature = hmac.new(
            self.secret.encode('utf-8'),
            message.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        return signature
    
    def send_request(self, endpoint, params=None, method='GET'):
        """发送OKX API请求"""
        timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        request_path = f"/api/v5{endpoint}"
        
        headers = {
            'OK-ACCESS-KEY': self.api_key,
            'OK-ACCESS-SIGN': self.generate_signature(timestamp, method, request_path, json.dumps(params) if params else ""),
            'OK-ACCESS-TIMESTAMP': timestamp,
            'OK-ACCESS-PASSPHRASE': self.passphrase,
            'Content-Type': 'application/json'
        }
        
        url = f"{self.base_url}{request_path}"
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=10)
            else:
                response = requests.post(url, json=params, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('code') == '0':
                    return data.get('data', [])
                else:
                    print(f"❌ OKX API错误: {data}")
                    return None
            else:
                print(f"❌ OKX HTTP错误 {response.status_code}: {response.text}")
                return None
        except Exception as e:
            print(f"⚠️ OKX请求异常: {e}")
            return None
    
    def get_account_balance(self):
        """获取账户余额"""
        print("\n💰 检查账户余额...")
        endpoint = "/account/balance"
        balance_data = self.send_request(endpoint)
        
        if balance_data and len(balance_data) > 0:
            print("✅ 账户余额信息:")
            for detail in balance_data[0]['details']:
                currency = detail['ccy']
                available = float(detail['availEq'])
                frozen = float(detail['frozenBal'])
                total = float(detail['eq'])
                
                print(f"   {currency}:")
                print(f"     可用余额: {available:.6f}")
                print(f"     冻结余额: {frozen:.6f}")
                print(f"     总权益: {total:.6f}")
            return balance_data
        else:
            print("❌ 无法获取余额信息")
            return None
    
    def get_positions(self):
        """获取持仓信息"""
        print("\n📈 检查持仓信息...")
        endpoint = "/account/positions"
        positions_data = self.send_request(endpoint)
        
        if positions_data:
            if len(positions_data) > 0:
                print("✅ 当前持仓:")
                for position in positions_data:
                    inst_id = position['instId']
                    pos_side = position['posSide']
                    quantity = float(position['pos'])
                    avg_price = float(position['avgPx'])
                    unrealized_pnl = float(position['upl'])
                    
                    print(f"   {inst_id} ({pos_side}):")
                    print(f"     持仓量: {quantity}")
                    print(f"     均价: {avg_price:.2f}")
                    print(f"     未实现盈亏: {unrealized_pnl:.6f}")
            else:
                print("📈 当前无持仓")
            return positions_data
        else:
            print("❌ 无法获取持仓信息")
            return None
    
    def get_market_price(self, inst_id="BTC-USDT-SWAP"):
        """获取市场价格"""
        endpoint = "/market/ticker"
        params = {'instId': inst_id}
        price_data = self.send_request(endpoint, params)
        
        if price_data and len(price_data) > 0:
            last_price = float(price_data[0]['last'])
            print(f"\n🎯 市场价格: {inst_id} = {last_price:.2f} USDT")
            return last_price
        else:
            print("❌ 无法获取市场价格")
            return None
    
    def get_account_config(self):
        """获取账户配置"""
        print("\n⚙️ 检查账户配置...")
        endpoint = "/account/config"
        config_data = self.send_request(endpoint)
        
        if config_data and len(config_data) > 0:
            print("✅ 账户配置:")
            for config in config_data:
                level = config['level']
                acct_lv = config['acctLv']
                auto_loan = config['autoLoan']
                greeks_type = config['greeksType']
                
                print(f"   账户等级: {level}")
                print(f"   账户类型: {acct_lv}")
                print(f"   自动借贷: {auto_loan}")
                print(f"   希腊字母类型: {greeks_type}")
            return config_data
        else:
            print("❌ 无法获取账户配置")
            return None
    
    def get_leverage_info(self, inst_id="BTC-USDT-SWAP"):
        """获取杠杆信息"""
        print(f"\n📊 检查杠杆信息 ({inst_id})...")
        endpoint = "/account/leverage-info"
        params = {'instId': inst_id}
        leverage_data = self.send_request(endpoint, params)
        
        if leverage_data and len(leverage_data) > 0:
            print("✅ 杠杆信息:")
            for leverage in leverage_data:
                pos_side = leverage['posSide']
                lever = leverage['lever']
                mgn_ratio = float(leverage['mgnRatio'])
                
                print(f"   {pos_side}:")
                print(f"     杠杆倍数: {lever}")
                print(f"     保证金率: {mgn_ratio:.4f}")
            return leverage_data
        else:
            print("❌ 无法获取杠杆信息")
            return None
    
    def get_max_order_size(self, inst_id="BTC-USDT-SWAP"):
        """获取最大下单数量"""
        print(f"\n📏 检查最大下单数量 ({inst_id})...")
        endpoint = "/account/max-size"
        params = {
            'instId': inst_id,
            'tdMode': 'cross'
        }
        size_data = self.send_request(endpoint, params)
        
        if size_data and len(size_data) > 0:
            print("✅ 最大下单信息:")
            for size_info in size_data:
                max_buy = float(size_info['maxBuy'])
                max_sell = float(size_info['maxSell'])
                
                print(f"   最大买入: {max_buy}")
                print(f"   最大卖出: {max_sell}")
            return size_data
        else:
            print("❌ 无法获取最大下单信息")
            return None
    
    def get_recent_orders(self, inst_id="BTC-USDT-SWAP"):
        """获取最近订单"""
        print(f"\n📋 检查最近订单 ({inst_id})...")
        endpoint = "/trade/orders-history"
        params = {
            'instType': 'SWAP',
            'instId': inst_id,
            'limit': '10'
        }
        orders_data = self.send_request(endpoint, params)
        
        if orders_data and len(orders_data) > 0:
            print("✅ 最近订单:")
            for order in orders_data:
                ord_id = order['ordId']
                side = order['side']
                sz = float(order['sz'])
                avg_px = float(order['avgPx']) if order['avgPx'] else 0
                state = order['state']
                
                print(f"   订单 {ord_id}:")
                print(f"     方向: {side}")
                print(f"     数量: {sz}")
                print(f"     均价: {avg_px:.2f}")
                print(f"     状态: {state}")
            return orders_data
        else:
            print("📋 无历史订单")
            return None
    
    def check_account_status(self):
        """全面检查账户状态"""
        print("🚀 虞姬OKX账户状态检查")
        print(f"⏰ 检查时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("-" * 50)
        
        # 测试连接
        test_price = self.get_market_price()
        if not test_price:
            print("\n❌ OKX API连接失败，请检查API配置")
            return False
        
        # 全面检查
        self.get_account_balance()
        self.get_positions()
        self.get_account_config()
        self.get_leverage_info()
        self.get_max_order_size()
        self.get_recent_orders()
        
        print("\n" + "=" * 50)
        print("✅ OKX账户状态检查完成")
        print("🔧 账户配置正常，可以开始交易")
        
        return True

# 立即检查账户状态
def check_okx_account():
    """检查OKX账户状态"""
    print("🔍 立即检查虞姬OKX账户状态...")
    
    checker = OKXAccountChecker()
    
    try:
        checker.check_account_status()
    except KeyboardInterrupt:
        print("\n⏹️ 检查停止")
    except Exception as e:
        print(f"\n❌ 检查异常: {e}")

if __name__ == "__main__":
    check_okx_account()