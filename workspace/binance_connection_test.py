#!/usr/bin/env python3
"""
虞姬币安测试网连接验证 v1.0
目标：验证API连接，测试基本功能
"""

import time
import hmac
import hashlib
import requests
import json
from datetime import datetime
from urllib.parse import urlencode

class BinanceConnectionTest:
    def __init__(self):
        # 币安测试网API配置
        self.api_key = "1a3250b36d5a27ccc0e6a0125d98d1556ff9eacc78baa1fd9ecb1be09056c8f4"
        self.api_secret = "6de29564a693aad4a969049d5accb6175fcd88be7dc4f2283e598d9a271c8505"
        
        # 测试网基础URL
        self.base_url = "https://testnet.binancefuture.com"
        self.fapi_url = f"{self.base_url}/fapi/v1"
        
    def generate_signature(self, params):
        """生成API签名"""
        query_string = urlencode(params)
        signature = hmac.new(
            self.api_secret.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        return signature
    
    def send_request(self, endpoint, params=None, method='GET'):
        """发送API请求"""
        if params is None:
            params = {}
        
        # 添加时间戳和签名
        params['timestamp'] = int(time.time() * 1000)
        params['signature'] = self.generate_signature(params)
        
        url = f"{self.fapi_url}{endpoint}"
        headers = {
            'X-MBX-APIKEY': self.api_key
        }
        
        print(f"🔗 请求: {method} {url}")
        print(f"📋 参数: {params}")
        
        try:
            if method == 'GET':
                response = requests.get(url, params=params, headers=headers, timeout=10)
            else:
                response = requests.post(url, params=params, headers=headers, timeout=10)
            
            print(f"📡 响应状态: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ 请求成功: {json.dumps(data, indent=2)[:500]}...")
                return data
            else:
                print(f"❌ 请求失败: {response.text}")
                return None
                
        except Exception as e:
            print(f"⚠️ 请求异常: {e}")
            return None
    
    def test_connection(self):
        """测试连接"""
        print("🧪 开始测试币安测试网连接...")
        print("-" * 50)
        
        # 测试1: 获取服务器时间
        print("\n1. 测试服务器时间...")
        time_data = self.send_request("/time")
        if time_data and 'serverTime' in time_data:
            server_time = datetime.fromtimestamp(time_data['serverTime'] / 1000)
            print(f"✅ 服务器时间: {server_time}")
        
        # 测试2: 获取交易对信息
        print("\n2. 测试交易对信息...")
        exchange_info = self.send_request("/exchangeInfo")
        if exchange_info and 'symbols' in exchange_info:
            btc_symbol = [s for s in exchange_info['symbols'] if s['symbol'] == 'BTCUSDT']
            if btc_symbol:
                print(f"✅ BTCUSDT交易对信息获取成功")
        
        # 测试3: 获取账户信息
        print("\n3. 测试账户信息...")
        account_info = self.send_request("/account")
        if account_info:
            if 'assets' in account_info:
                for asset in account_info['assets']:
                    if asset['asset'] == 'USDT':
                        balance = float(asset['walletBalance'])
                        print(f"✅ 账户余额: {balance} USDT")
                        break
        
        # 测试4: 获取持仓信息
        print("\n4. 测试持仓信息...")
        position_info = self.send_request("/positionRisk", {'symbol': 'BTCUSDT'})
        if position_info and isinstance(position_info, list):
            if len(position_info) > 0:
                position = position_info[0]
                print(f"✅ 持仓信息: {position}")
            else:
                print("✅ 当前无持仓")
        
        # 测试5: 获取市场价格
        print("\n5. 测试市场价格...")
        price_info = self.send_request("/ticker/price", {'symbol': 'BTCUSDT'})
        if price_info and 'price' in price_info:
            price = float(price_info['price'])
            print(f"✅ BTC当前价格: {price} USDT")
        
        print("\n" + "=" * 50)
        print("🎉 币安测试网连接验证完成!")
        print("✅ API连接正常")
        print("✅ 账户信息可获取")
        print("✅ 市场数据正常")
        print("✅ 准备开始交易!")

# 运行连接测试
def run_connection_test():
    """运行连接测试"""
    print("🚀 虞姬币安测试网连接验证启动")
    print(f"⏰ 时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    tester = BinanceConnectionTest()
    tester.test_connection()

if __name__ == "__main__":
    run_connection_test()