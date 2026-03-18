#!/usr/bin/env python3
"""
虞姬币安测试网实时交易系统 v1.0
连接真实API，开始实战交易
"""

import time
import hmac
import hashlib
import requests
import json
from datetime import datetime
from urllib.parse import urlencode

class BinanceLiveTrader:
    def __init__(self):
        # 币安测试网API配置
        self.api_key = "1a3250b36d5a27ccc0e6a0125d98d1556ff9eacc78baa1fd9ecb1be09056c8f4"
        self.api_secret = "6de29564a693aad4a969049d5accb6175fcd88be7dc4f2283e598d9a271c8505"
        
        # 测试网基础URL
        self.base_url = "https://testnet.binancefuture.com"
        self.fapi_url = f"{self.base_url}/fapi/v1"
        
        # 交易配置
        self.symbol = "BTCUSDT"
        self.leverage = 20
        self.total_capital = 100.0  # 100 USDT
        
        # 账户状态
        self.balance = 0.0
        self.positions = {}
        self.profit = 0.0
        self.trades = 0
        self.start_time = datetime.now()
        
        # 激进网格策略
        self.strategy_config = {
            'grid_levels': 5,
            'grid_spacing': 0.005,  # 0.5%
            'position_size': 0.2,   # 20%
            'take_profit': 0.01,    # 1%
            'stop_loss': 0.005      # 0.5%
        }
        
    def generate_signature(self, params):
        """生成API签名"""
        query_string = urlencode(params)
        signature = hmac.new(
            self.api_secret.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        return signature
    
    def send_signed_request(self, endpoint, params=None, method='GET'):
        """发送签名请求"""
        if params is None:
            params = {}
        
        params['timestamp'] = int(time.time() * 1000)
        params['signature'] = self.generate_signature(params)
        
        url = f"{self.fapi_url}{endpoint}"
        headers = {'X-MBX-APIKEY': self.api_key}
        
        try:
            if method == 'GET':
                response = requests.get(url, params=params, headers=headers, timeout=10)
            else:
                response = requests.post(url, params=params, headers=headers, timeout=10)
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ API错误 {response.status_code}: {response.text}")
                return None
                
        except Exception as e:
            print(f"⚠️ 请求异常: {e}")
            return None
    
    def get_account_info(self):
        """获取账户信息"""
        endpoint = "/account"
        account_data = self.send_signed_request(endpoint)
        
        if account_data and 'assets' in account_data:
            for asset in account_data['assets']:
                if asset['asset'] == 'USDT':
                    self.balance = float(asset['walletBalance'])
                    print(f"💰 账户余额: {self.balance} USDT")
                    return True
        
        print("⚠️ 无法获取账户信息")
        return False
    
    def get_positions(self):
        """获取持仓信息"""
        endpoint = "/positionRisk"
        params = {'symbol': self.symbol}
        positions_data = self.send_signed_request(endpoint, params)
        
        if positions_data and isinstance(positions_data, list):
            self.positions = {}
            for position in positions_data:
                if position['symbol'] == self.symbol and float(position['positionAmt']) != 0:
                    self.positions[self.symbol] = {
                        'amount': float(position['positionAmt']),
                        'entryPrice': float(position['entryPrice']),
                        'unrealizedProfit': float(position['unRealizedProfit'])
                    }
            if self.positions:
                print(f"📈 持仓信息: {self.positions}")
            else:
                print("📈 当前无持仓")
        
        return self.positions
    
    def get_market_price(self):
        """获取市场价格"""
        endpoint = "/ticker/price"
        params = {'symbol': self.symbol}
        price_data = self.send_signed_request(endpoint, params)
        
        if price_data and 'price' in price_data:
            price = float(price_data['price'])
            return price
        
        print("⚠️ 无法获取市场价格")
        return None
    
    def set_leverage(self):
        """设置杠杆"""
        endpoint = "/leverage"
        params = {
            'symbol': self.symbol,
            'leverage': self.leverage
        }
        result = self.send_signed_request(endpoint, params, 'POST')
        
        if result and 'leverage' in result:
            print(f"✅ 杠杆设置成功: {result['leverage']}x")
            return True
        else:
            print("⚠️ 杠杆设置失败")
            return False
    
    def place_market_order(self, side, quantity):
        """下市价单"""
        endpoint = "/order"
        params = {
            'symbol': self.symbol,
            'side': side,
            'type': 'MARKET',
            'quantity': quantity
        }
        
        result = self.send_signed_request(endpoint, params, 'POST')
        
        if result and 'orderId' in result:
            self.trades += 1
            current_price = self.get_market_price()
            
            print(f"✅ 市价单成功 | {side} | 数量: {quantity} | 订单ID: {result['orderId']}")
            return True
        
        print(f"❌ 下单失败 | {side} | 数量: {quantity}")
        return False
    
    def aggressive_grid_strategy(self, current_price):
        """激进网格策略"""
        if not hasattr(self, 'base_price'):
            self.base_price = current_price
            print(f"🎯 设置基础价格: {self.base_price:.2f}")
        
        # 计算网格买入点 (0.5%下跌)
        buy_price = self.base_price * (1 - self.strategy_config['grid_spacing'])
        if current_price <= buy_price and self.balance > 0:
            # 开多仓
            trade_size = self.balance * self.strategy_config['position_size']
            quantity = trade_size / current_price
            
            if quantity >= 0.001:  # 最小交易量
                if self.place_market_order('BUY', round(quantity, 6)):
                    self.base_price = current_price
                    return "BUY"
        
        # 计算网格卖出点 (0.5%上涨)
        sell_price = self.base_price * (1 + self.strategy_config['grid_spacing'])
        if current_price >= sell_price and self.symbol in self.positions:
            # 平多仓
            position_amount = abs(self.positions[self.symbol]['amount'])
            if position_amount >= 0.001:
                if self.place_market_order('SELL', round(position_amount, 6)):
                    # 记录盈亏
                    entry_price = self.positions[self.symbol]['entryPrice']
                    pnl = (current_price - entry_price) * position_amount
                    self.profit += pnl
                    print(f"🎯 平仓盈亏: {pnl:.4f} USDT")
                    self.base_price = current_price
                    return "SELL"
        
        return "HOLD"
    
    def initialize_trading(self):
        """初始化交易"""
        print("🔧 初始化币安测试网交易系统...")
        
        # 设置杠杆
        if not self.set_leverage():
            return False
        
        # 获取初始余额
        if not self.get_account_info():
            return False
        
        # 获取初始价格
        initial_price = self.get_market_price()
        if not initial_price:
            return False
        
        self.base_price = initial_price
        print("✅ 交易系统初始化完成")
        return True
    
    def run_live_trading(self):
        """运行实时交易"""
        print("🚀 虞姬币安测试网实时交易启动")
        print(f"💰 初始资金: {self.total_capital} USDT")
        print(f"📈 杠杆: {self.leverage}x")
        print(f"🎯 交易对: {self.symbol}")
        print(f"⚡ 策略: 激进网格交易 (0.5%触发)")
        print(f"⏰ 开始时间: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print("-" * 60)
        
        # 初始化
        if not self.initialize_trading():
            print("❌ 系统初始化失败，停止交易")
            return
        
        last_report_time = time.time()
        cycle = 0
        
        while True:
            try:
                # 获取市场数据
                current_price = self.get_market_price()
                if not current_price:
                    print("⏳ 等待市场价格...")
                    time.sleep(30)
                    continue
                
                # 更新账户状态
                self.get_account_info()
                self.get_positions()
                
                # 每3个周期执行一次交易
                if cycle % 3 == 0:
                    action = self.aggressive_grid_strategy(current_price)
                    if action != "HOLD":
                        print(f"🎯 执行动作: {action}")
                
                cycle += 1
                
                # 每分钟报告状态
                current_time = time.time()
                if current_time - last_report_time >= 60:
                    self.report_status(current_price)
                    last_report_time = current_time
                
                time.sleep(20)  # 每20秒检查一次
                
            except KeyboardInterrupt:
                print("\n⏹️ 实时交易停止")
                final_price = self.get_market_price()
                if final_price:
                    self.report_status(final_price)
                break
            except Exception as e:
                print(f"⚠️ 交易异常: {e}")
                time.sleep(30)
    
    def report_status(self, current_price):
        """报告状态"""
        total_assets = self.balance
        position_value = 0
        
        if self.symbol in self.positions:
            position_value = abs(self.positions[self.symbol]['amount']) * current_price
            total_assets += position_value
        
        progress = (total_assets / 1000000) * 100
        running_time = (datetime.now() - self.start_time).total_seconds()
        
        print(f"\n📊 【实时交易报告】 {datetime.now().strftime('%H:%M:%S')}")
        print(f"💰 总资产: {total_assets:.4f} USDT")
        print(f"💵 可用余额: {self.balance:.4f} USDT")
        print(f"📈 持仓价值: {position_value:.4f} USDT")
        print(f"🎯 总利润: {self.profit:.4f} USDT")
        print(f"🔢 交易次数: {self.trades}")
        print(f"🚀 百万进度: {progress:.8f}%")
        print(f"⏱️ 运行时间: {running_time:.0f}秒")
        
        # 计算预计时间
        if progress > 0 and running_time > 0:
            growth_rate = (total_assets - self.total_capital) / self.total_capital / running_time
            if growth_rate > 0:
                seconds_to_target = (1000000 - total_assets) / (total_assets * growth_rate)
                days_to_target = seconds_to_target / 86400
                if days_to_target > 0:
                    print(f"📅 预计达成: {days_to_target:.1f} 天")
        
        print("-" * 60)

# 立即启动实时交易
def start_binance_live_trading():
    """启动币安实时交易"""
    print("🚀 立即启动虞姬币安测试网实时交易系统!")
    
    trader = BinanceLiveTrader()
    
    try:
        trader.run_live_trading()
    except KeyboardInterrupt:
        print("\n⏹️ 系统停止")

if __name__ == "__main__":
    start_binance_live_trading()