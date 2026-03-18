#!/usr/bin/env python3
"""
虞姬币安测试网实战交易机器人 v1.0
修复API端点，立即启动交易
"""

import time
import hmac
import hashlib
import requests
import json
from datetime import datetime
from urllib.parse import urlencode

class BinanceFixedBot:
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
        self.initial_capital = 10.0
        
        # 账户状态
        self.balance = 10.0
        self.position = 0.0
        self.profit = 0.0
        self.trades = 0
        self.winning_trades = 0
        self.start_time = datetime.now()
        
        # 风险控制
        self.risk_config = {
            'max_position': 0.3,
            'stop_loss': 0.03,
            'take_profit': 0.06,
            'grid_levels': 5,
            'grid_spacing': 0.02
        }
        
        # 交易记录
        self.trade_history = []
        
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
                print(f"❌ API错误: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"⚠️ 请求异常: {e}")
            return None
    
    def get_market_price(self):
        """获取市场价格"""
        endpoint = "/ticker/price"
        params = {'symbol': self.symbol}
        price_data = self.send_request(endpoint, params)
        
        if price_data and 'price' in price_data:
            return float(price_data['price'])
        return None
    
    def place_market_order(self, side, quantity):
        """下市价单"""
        endpoint = "/order"
        params = {
            'symbol': self.symbol,
            'side': side,
            'type': 'MARKET',
            'quantity': quantity
        }
        
        result = self.send_request(endpoint, params, 'POST')
        
        if result and 'orderId' in result:
            self.trades += 1
            current_price = self.get_market_price()
            
            trade_record = {
                'order_id': result['orderId'],
                'side': side,
                'quantity': quantity,
                'price': current_price,
                'timestamp': datetime.now()
            }
            
            self.trade_history.append(trade_record)
            
            print(f"✅ 市价单成功 | {side} | 数量: {quantity} | 价格: {current_price:.2f}")
            return True
        
        return False
    
    def simulate_grid_trading(self, current_price):
        """模拟网格交易策略"""
        if not hasattr(self, 'base_price'):
            self.base_price = current_price
            print(f"🎯 设置基础价格: {self.base_price:.2f}")
        
        # 网格买入条件
        buy_condition = current_price <= self.base_price * 0.98
        # 网格卖出条件
        sell_condition = current_price >= self.base_price * 1.02
        
        if buy_condition and self.position < self.balance * 0.3:
            # 开多仓
            trade_size = self.balance * 0.1
            quantity = trade_size / current_price
            
            if self.place_market_order('BUY', round(quantity, 6)):
                self.position += quantity
                self.balance -= trade_size
                self.base_price = current_price  # 更新基础价格
                return "BUY"
        
        elif sell_condition and self.position > 0:
            # 平多仓
            close_quantity = self.position * 0.3
            trade_value = close_quantity * current_price
            
            if self.place_market_order('SELL', round(close_quantity, 6)):
                # 计算盈亏
                entry_price = self.trade_history[-2]['price'] if len(self.trade_history) >= 2 else current_price
                pnl = (current_price - entry_price) * close_quantity
                
                self.profit += pnl
                self.balance += trade_value + pnl
                self.position -= close_quantity
                
                if pnl > 0:
                    self.winning_trades += 1
                    status = "✅ 盈利"
                else:
                    status = "❌ 亏损"
                
                print(f"{status} | PnL: {pnl:.4f} USDT")
                self.base_price = current_price  # 更新基础价格
                return "SELL"
        
        return "HOLD"
    
    def run_live_trading(self):
        """运行实时交易"""
        print("🚀 虞姬币安测试网实战交易启动")
        print(f"💰 初始资金: {self.balance} USDT")
        print(f"📈 杠杆: {self.leverage}x")
        print(f"🎯 目标: 100万美金")
        print(f"⏰ 开始时间: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print("-" * 60)
        
        last_report_time = time.time()
        cycle_count = 0
        
        while True:
            try:
                # 获取市场价格
                current_price = self.get_market_price()
                if not current_price:
                    time.sleep(30)
                    continue
                
                # 每5个周期执行一次交易
                if cycle_count % 5 == 0:
                    action = self.simulate_grid_trading(current_price)
                    if action != "HOLD":
                        print(f"🎯 执行动作: {action}")
                
                cycle_count += 1
                
                # 每分钟报告状态
                current_time = time.time()
                if current_time - last_report_time >= 60:
                    self.report_status(current_price)
                    last_report_time = current_time
                
                time.sleep(10)
                
            except Exception as e:
                print(f"⚠️ 交易异常: {e}")
                time.sleep(30)
    
    def report_status(self, current_price):
        """报告状态"""
        total_value = self.balance + (self.position * current_price)
        win_rate = self.winning_trades / self.trades if self.trades > 0 else 0
        
        print(f"\n📊 【虞姬实战报告】 {datetime.now().strftime('%H:%M:%S')}")
        print(f"💰 总资产: {total_value:.4f} USDT")
        print(f"💵 可用资金: {self.balance:.4f} USDT")
        print(f"📈 持仓: {self.position:.6f} BTC")
        print(f"🎯 总利润: {self.profit:.4f} USDT")
        print(f"🔢 交易次数: {self.trades}")
        print(f"🎯 胜率: {win_rate:.1%}")
        
        # 计算百万目标进度
        progress = (total_value / 1000000) * 100
        print(f"🚀 百万目标进度: {progress:.8f}%")
        
        # 计算预计达成时间
        if progress > 0 and (datetime.now() - self.start_time).total_seconds() > 0:
            growth_rate = (total_value - 10) / 10 / (datetime.now() - self.start_time).total_seconds()
            if growth_rate > 0:
                days_to_target = (1000000 - total_value) / (total_value * growth_rate * 86400)
                if days_to_target > 0:
                    print(f"📅 预计达成: {days_to_target:.1f} 天")
        
        print("-" * 60)

# 立即启动交易
def start_immediate_trading():
    """立即启动交易"""
    print("🚀 虞姬立即启动币安测试网实战交易!")
    
    bot = BinanceFixedBot()
    
    try:
        bot.run_live_trading()
    except KeyboardInterrupt:
        print("\n⏹️ 交易停止")
        final_price = bot.get_market_price()
        if final_price:
            bot.report_status(final_price)

if __name__ == "__main__":
    start_immediate_trading()