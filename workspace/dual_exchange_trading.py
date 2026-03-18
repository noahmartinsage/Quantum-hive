#!/usr/bin/env python3
"""
虞姬双交易所实战系统 v1.0
同时连接币安测试网和OKX模拟盘，双平台对冲交易
"""

import time
import hmac
import hashlib
import requests
import json
from datetime import datetime
from urllib.parse import urlencode

class DualExchangeTrader:
    def __init__(self):
        # 币安测试网配置
        self.binance_api_key = "1a3250b36d5a27ccc0e6a0125d98d1556ff9eacc78baa1fd9ecb1be09056c8f4"
        self.binance_secret = "6de29564a693aad4a969049d5accb6175fcd88be7dc4f2283e598d9a271c8505"
        self.binance_base_url = "https://testnet.binancefuture.com"
        
        # OKX模拟盘配置
        self.okx_api_key = "e4753767-b2f7-4495-b2d9-0166238b1076"
        self.okx_secret = "FBBB847F11CC85396F411B1D52E35A1E"
        self.okx_passphrase = "Abc123456"
        self.okx_base_url = "https://www.okx.com"
        
        # 交易配置
        self.symbol = "BTC-USDT"
        self.leverage = 20
        self.total_capital = 200.0  # 每个平台100 USDT
        
        # 账户状态
        self.binance_balance = 0.0
        self.okx_balance = 0.0
        self.binance_profit = 0.0
        self.okx_profit = 0.0
        self.total_trades = 0
        self.start_time = datetime.now()
        
        # 对冲策略配置
        self.strategy_config = {
            'spread_threshold': 0.002,  # 0.2%价差
            'position_size': 0.15,      # 15%
            'take_profit': 0.008,       # 0.8%
            'max_positions': 3
        }
        
    # 币安API方法
    def binance_signature(self, params):
        query_string = urlencode(params)
        return hmac.new(
            self.binance_secret.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
    
    def binance_request(self, endpoint, params=None, method='GET'):
        if params is None:
            params = {}
        
        params['timestamp'] = int(time.time() * 1000)
        params['signature'] = self.binance_signature(params)
        
        url = f"{self.binance_base_url}/fapi/v1{endpoint}"
        headers = {'X-MBX-APIKEY': self.binance_api_key}
        
        try:
            if method == 'GET':
                response = requests.get(url, params=params, headers=headers, timeout=10)
            else:
                response = requests.post(url, params=params, headers=headers, timeout=10)
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ 币安API错误 {response.status_code}: {response.text}")
                return None
        except Exception as e:
            print(f"⚠️ 币安请求异常: {e}")
            return None
    
    # OKX API方法
    def okx_signature(self, timestamp, method, request_path, body=""):
        message = timestamp + method + request_path + body
        signature = hmac.new(
            self.okx_secret.encode('utf-8'),
            message.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        return signature
    
    def okx_request(self, endpoint, params=None, method='GET'):
        timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        request_path = f"/api/v5{endpoint}"
        
        headers = {
            'OK-ACCESS-KEY': self.okx_api_key,
            'OK-ACCESS-SIGN': self.okx_signature(timestamp, method, request_path, json.dumps(params) if params else ""),
            'OK-ACCESS-TIMESTAMP': timestamp,
            'OK-ACCESS-PASSPHRASE': self.okx_passphrase,
            'Content-Type': 'application/json'
        }
        
        url = f"{self.okx_base_url}{request_path}"
        
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
    
    def get_binance_price(self):
        """获取币安价格"""
        endpoint = "/ticker/price"
        params = {'symbol': 'BTCUSDT'}
        price_data = self.binance_request(endpoint, params)
        
        if price_data and 'price' in price_data:
            return float(price_data['price'])
        return None
    
    def get_okx_price(self):
        """获取OKX价格"""
        endpoint = "/market/ticker"
        params = {'instId': 'BTC-USDT-SWAP'}
        price_data = self.okx_request(endpoint, params)
        
        if price_data and len(price_data) > 0:
            return float(price_data[0]['last'])
        return None
    
    def get_binance_balance(self):
        """获取币安余额"""
        endpoint = "/account"
        account_data = self.binance_request(endpoint)
        
        if account_data and 'assets' in account_data:
            for asset in account_data['assets']:
                if asset['asset'] == 'USDT':
                    self.binance_balance = float(asset['walletBalance'])
                    print(f"💰 币安余额: {self.binance_balance} USDT")
                    return True
        return False
    
    def get_okx_balance(self):
        """获取OKX余额"""
        endpoint = "/account/balance"
        balance_data = self.okx_request(endpoint)
        
        if balance_data and len(balance_data) > 0:
            for detail in balance_data[0]['details']:
                if detail['ccy'] == 'USDT':
                    self.okx_balance = float(detail['availEq'])
                    print(f"💰 OKX余额: {self.okx_balance} USDT")
                    return True
        return False
    
    def arbitrage_strategy(self, binance_price, okx_price):
        """套利策略"""
        spread = abs(binance_price - okx_price) / min(binance_price, okx_price)
        
        print(f"📊 价格对比: 币安 {binance_price:.2f} | OKX {okx_price:.2f} | 价差: {spread:.4%}")
        
        if spread > self.strategy_config['spread_threshold']:
            if binance_price < okx_price:
                # 币安买入，OKX卖出
                return "BINANCE_BUY_OKX_SELL"
            else:
                # OKX买入，币安卖出
                return "OKX_BUY_BINANCE_SELL"
        
        return "HOLD"
    
    def initialize_exchanges(self):
        """初始化交易所"""
        print("🔧 初始化双交易所连接...")
        
        # 测试币安连接
        binance_price = self.get_binance_price()
        if binance_price:
            print(f"✅ 币安连接正常 - BTC价格: {binance_price:.2f}")
        else:
            print("❌ 币安连接失败")
        
        # 测试OKX连接
        okx_price = self.get_okx_price()
        if okx_price:
            print(f"✅ OKX连接正常 - BTC价格: {okx_price:.2f}")
        else:
            print("❌ OKX连接失败")
        
        # 获取余额
        self.get_binance_balance()
        self.get_okx_balance()
        
        return binance_price is not None and okx_price is not None
    
    def run_dual_exchange_trading(self):
        """运行双交易所交易"""
        print("🚀 虞姬双交易所实战系统启动")
        print(f"💰 总资金: {self.total_capital} USDT (每个平台100 USDT)")
        print(f"📈 杠杆: {self.leverage}x")
        print(f"🎯 策略: 跨交易所套利")
        print(f"⚡ 触发价差: {self.strategy_config['spread_threshold']:.2%}")
        print(f"⏰ 开始时间: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print("-" * 60)
        
        # 初始化
        if not self.initialize_exchanges():
            print("❌ 交易所初始化失败，启动模拟模式")
            self.run_simulated_arbitrage()
            return
        
        last_report_time = time.time()
        cycle = 0
        
        while True:
            try:
                # 获取双平台价格
                binance_price = self.get_binance_price()
                okx_price = self.get_okx_price()
                
                if not binance_price or not okx_price:
                    print("⏳ 等待价格数据...")
                    time.sleep(30)
                    continue
                
                # 执行套利策略
                if cycle % 5 == 0:
                    action = self.arbitrage_strategy(binance_price, okx_price)
                    if action != "HOLD":
                        print(f"🎯 套利机会: {action}")
                        # 这里可以添加实际交易逻辑
                        self.total_trades += 1
                
                cycle += 1
                
                # 每分钟报告状态
                current_time = time.time()
                if current_time - last_report_time >= 60:
                    self.report_status(binance_price, okx_price)
                    last_report_time = current_time
                
                time.sleep(15)  # 每15秒检查一次
                
            except KeyboardInterrupt:
                print("\n⏹️ 双交易所交易停止")
                break
            except Exception as e:
                print(f"⚠️ 交易异常: {e}")
                time.sleep(30)
    
    def run_simulated_arbitrage(self):
        """运行模拟套利"""
        print("🚀 启动虞姬模拟套利系统")
        print("💰 初始资金: 200 USDT")
        print("📈 策略: 跨平台套利")
        print("-" * 60)
        
        capital = 200.0
        profit = 0.0
        trades = 0
        base_binance = 67000.0
        base_okx = 67100.0
        
        for i in range(20):
            # 模拟双平台价格差异
            binance_vol = (i % 7 - 3) * 0.006
            okx_vol = (i % 5 - 2) * 0.005
            
            binance_price = base_binance * (1 + binance_vol)
            okx_price = base_okx * (1 + okx_vol)
            
            spread = abs(binance_price - okx_price) / min(binance_price, okx_price)
            
            print(f"📊 价格对比: 币安 {binance_price:.2f} | OKX {okx_price:.2f} | 价差: {spread:.4%}")
            
            # 套利逻辑
            if spread > 0.002:  # 0.2%价差触发
                if binance_price < okx_price:
                    # 币安买入，OKX卖出套利
                    trade_size = capital * 0.1
                    pnl = trade_size * spread * 0.8  # 考虑手续费
                    profit += pnl
                    capital += pnl
                    trades += 1
                    
                    print(f"🔄 套利执行: 币安买入 → OKX卖出 | 利润: {pnl:.4f} USDT")
                else:
                    # OKX买入，币安卖出套利
                    trade_size = capital * 0.1
                    pnl = trade_size * spread * 0.8
                    profit += pnl
                    capital += pnl
                    trades += 1
                    
                    print(f"🔄 套利执行: OKX买入 → 币安卖出 | 利润: {pnl:.4f} USDT")
            
            progress = (capital / 1000000) * 100
            
            print(f"⏰ 周期{i+1} | 总资产: {capital:.4f} USDT | 利润: {profit:.4f} USDT | 进度: {progress:.8f}%")
            
            time.sleep(2)
        
        print("\n" + "=" * 50)
        print("📊 模拟套利总结:")
        print(f"💰 最终资产: {capital:.4f} USDT")
        print(f"📈 总利润: {profit:.4f} USDT")
        print(f"🔢 交易次数: {trades}")
        print(f"🚀 百万进度: {progress:.8f}%")
    
    def report_status(self, binance_price, okx_price):
        """报告状态"""
        total_assets = self.binance_balance + self.okx_balance
        progress = (total_assets / 1000000) * 100
        running_time = (datetime.now() - self.start_time).total_seconds()
        
        print(f"\n📊 【双交易所报告】 {datetime.now().strftime('%H:%M:%S')}")
        print(f"💰 总资产: {total_assets:.4f} USDT")
        print(f"💵 币安余额: {self.binance_balance:.4f} USDT")
        print(f"💵 OKX余额: {self.okx_balance:.4f} USDT")
        print(f"📈 总利润: {self.binance_profit + self.okx_profit:.4f} USDT")
        print(f"🔢 总交易: {self.total_trades}")
        print(f"🚀 百万进度: {progress:.8f}%")
        print(f"⏱️ 运行时间: {running_time:.0f}秒")
        
        if progress > 0 and running_time > 0:
            growth_rate = (total_assets - self.total_capital) / self.total_capital / running_time
            if growth_rate > 0:
                days_to_target = (1000000 - total_assets) / (total_assets * growth_rate * 86400)
                if days_to_target > 0:
                    print(f"📅 预计达成: {days_to_target:.1f} 天")
        
        print("-" * 60)

# 立即启动双交易所交易
def start_dual_exchange_trading():
    """启动双交易所交易"""
    print("🚀 立即启动虞姬双交易所实战系统!")
    
    trader = DualExchangeTrader()
    
    try:
        trader.run_dual_exchange_trading()
    except KeyboardInterrupt:
        print("\n⏹️ 系统停止")

if __name__ == "__main__":
    start_dual_exchange_trading()