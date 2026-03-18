#!/usr/bin/env python3
"""
虞姬币安测试网USDT合约机器人 v1.1
修复版：更好的错误处理和账户初始化
"""

import time
import hmac
import hashlib
import requests
import json
from datetime import datetime
from urllib.parse import urlencode

class BinanceTestnetBot:
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
        self.initial_capital = 10.0  # 10 USDT
        
        # 账户状态
        self.balance = 0.0
        self.position = 0.0
        self.profit = 0.0
        self.trades = 0
        self.winning_trades = 0
        self.start_time = datetime.now()
        
        # 风险控制
        self.risk_config = {
            'max_position': 0.3,      # 最大仓位30%
            'stop_loss': 0.03,        # 3%止损
            'take_profit': 0.06,      # 6%止盈
            'grid_levels': 5,         # 网格层级
            'grid_spacing': 0.02      # 网格间距2%
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
        
        # 添加时间戳和签名
        params['timestamp'] = int(time.time() * 1000)
        params['signature'] = self.generate_signature(params)
        
        url = f"{self.fapi_url}{endpoint}"
        headers = {
            'X-MBX-APIKEY': self.api_key
        }
        
        try:
            if method == 'GET':
                response = requests.get(url, params=params, headers=headers, timeout=10)
            else:
                response = requests.post(url, params=params, headers=headers, timeout=10)
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"API错误: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"API请求错误: {e}")
            return None
    
    def get_account_info(self):
        """获取账户信息"""
        endpoint = "/account"
        account_data = self.send_request(endpoint)
        
        if account_data and 'assets' in account_data:
            for asset in account_data['assets']:
                if asset['asset'] == 'USDT':
                    self.balance = float(asset['walletBalance'])
                    print(f"💰 账户余额: {self.balance} USDT")
                    break
        else:
            print("⚠️ 无法获取账户信息")
        
        return account_data
    
    def get_position_info(self):
        """获取持仓信息"""
        endpoint = "/positionRisk"
        params = {'symbol': self.symbol}
        position_data = self.send_request(endpoint, params)
        
        if position_data and isinstance(position_data, list) and len(position_data) > 0:
            position = position_data[0]
            self.position = float(position['positionAmt'])
            self.profit = float(position['unRealizedProfit'])
            print(f"📈 持仓: {self.position} BTC | 浮动盈亏: {self.profit} USDT")
        else:
            print("📈 当前无持仓")
            self.position = 0.0
            self.profit = 0.0
        
        return position_data
    
    def get_market_price(self):
        """获取市场价格"""
        endpoint = "/ticker/price"
        params = {'symbol': self.symbol}
        price_data = self.send_request(endpoint, params)
        
        if price_data and 'price' in price_data:
            price = float(price_data['price'])
            print(f"🎯 当前价格: {price:.2f} USDT")
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
        result = self.send_request(endpoint, params, 'POST')
        
        if result and 'leverage' in result:
            print(f"✅ 杠杆设置成功: {result['leverage']}x")
        else:
            print("⚠️ 杠杆设置失败")
        
        return result
    
    def place_order(self, side, quantity, price=None, order_type='MARKET'):
        """下单"""
        endpoint = "/order"
        params = {
            'symbol': self.symbol,
            'side': side,
            'type': order_type,
            'quantity': quantity
        }
        
        if price and order_type == 'LIMIT':
            params['price'] = price
            params['timeInForce'] = 'GTC'
        
        result = self.send_request(endpoint, params, 'POST')
        
        if result and 'orderId' in result:
            self.trades += 1
            self.trade_history.append({
                'order_id': result['orderId'],
                'side': side,
                'quantity': quantity,
                'price': price,
                'timestamp': datetime.now()
            })
            
            print(f"✅ 下单成功 | {side} | 数量: {quantity} | 订单ID: {result['orderId']}")
            return True
        else:
            print(f"❌ 下单失败 | {side} | 数量: {quantity}")
            return False
    
    def grid_trading_strategy(self, current_price):
        """网格交易策略"""
        actions = []
        
        # 如果没有基础价格，设置当前价格为基准
        if not hasattr(self, 'base_price'):
            self.base_price = current_price
        
        # 计算网格买入点
        for i in range(1, self.risk_config['grid_levels'] + 1):
            buy_price = self.base_price * (1 - i * self.risk_config['grid_spacing'])
            if current_price <= buy_price and abs(self.position) < (self.balance * self.risk_config['max_position'] / current_price):
                quantity = (self.balance * 0.05) / current_price  # 5%仓位
                if quantity > 0.001:  # 最小交易量
                    actions.append({
                        'action': 'BUY',
                        'price': round(buy_price, 2),
                        'quantity': round(quantity, 6),
                        'type': 'LIMIT'
                    })
        
        # 计算网格卖出点
        for i in range(1, self.risk_config['grid_levels'] + 1):
            sell_price = self.base_price * (1 + i * self.risk_config['grid_spacing'])
            if current_price >= sell_price and self.position > 0:
                quantity = self.position * 0.2  # 平20%仓位
                if quantity > 0.001:
                    actions.append({
                        'action': 'SELL',
                        'price': round(sell_price, 2),
                        'quantity': round(quantity, 6),
                        'type': 'LIMIT'
                    })
        
        return actions
    
    def initialize_account(self):
        """初始化账户"""
        print("🔧 初始化币安测试网账户...")
        
        # 设置杠杆
        self.set_leverage()
        
        # 获取初始价格
        initial_price = self.get_market_price()
        if initial_price:
            self.base_price = initial_price
            print(f"✅ 基础价格设置: {self.base_price:.2f}")
        
        # 获取账户信息
        self.get_account_info()
        self.get_position_info()
        
        print("✅ 账户初始化完成")
    
    def run_testnet_trading(self):
        """运行测试网交易"""
        print("🚀 虞姬币安测试网USDT合约机器人启动")
        print(f"💰 目标: 100万美金")
        print(f"📈 杠杆: {self.leverage}x")
        print(f"⏰ 运行模式: 7*24小时")
        print(f"🎯 交易对: {self.symbol}")
        print("-" * 60)
        
        # 初始化账户
        self.initialize_account()
        
        last_report_time = time.time()
        trade_count = 0
        
        while True:
            try:
                # 获取市场数据
                current_price = self.get_market_price()
                if not current_price:
                    print("⏳ 等待市场价格...")
                    time.sleep(30)
                    continue
                
                # 获取账户状态
                self.get_account_info()
                self.get_position_info()
                
                # 执行网格策略（每10次循环执行一次）
                if trade_count % 10 == 0:
                    grid_actions = self.grid_trading_strategy(current_price)
                    
                    # 执行交易
                    for action in grid_actions:
                        if action['action'] == 'BUY':
                            success = self.place_order('BUY', action['quantity'], action['price'], action['type'])
                            if success:
                                time.sleep(1)  # 交易间隔
                        else:
                            success = self.place_order('SELL', action['quantity'], action['price'], action['type'])
                            if success:
                                time.sleep(1)
                
                trade_count += 1
                
                # 每2分钟报告状态
                current_time = time.time()
                if current_time - last_report_time >= 120:
                    self.report_status(current_price)
                    last_report_time = current_time
                
                # 每30秒检查一次
                time.sleep(30)
                
            except Exception as e:
                print(f"⚠️ 交易异常: {e}")
                time.sleep(60)
    
    def report_status(self, current_price):
        """报告状态"""
        total_value = self.balance + (self.position * current_price if self.position != 0 else 0)
        
        print(f"\n📊 【虞姬测试网交易报告】 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"💰 总资产: {total_value:.4f} USDT")
        print(f"💵 可用余额: {self.balance:.4f} USDT")
        print(f"📈 持仓: {self.position:.6f} BTC")
        print(f"🎯 浮动盈亏: {self.profit:.4f} USDT")
        print(f"🔢 交易次数: {self.trades}")
        print(f"⏱️ 运行时间: {(datetime.now() - self.start_time).total_seconds():.0f}秒")
        
        # 计算距离100万美金进度
        if total_value > 0:
            progress = (total_value / 1000000) * 100
            print(f"🚀 百万目标进度: {progress:.8f}%")
            
            # 计算预计达成时间
            if progress > 0:
                days_to_target = (100 - progress) / (progress / (datetime.now() - self.start_time).total_seconds() * 86400)
                if days_to_target > 0:
                    print(f"📅 预计达成时间: {days_to_target:.1f} 天")
        
        print("-" * 60)

# 启动测试网交易
def start_testnet_trading():
    """启动测试网交易"""
    print("🚀 启动虞姬币安测试网USDT合约交易...")
    
    bot = BinanceTestnetBot()
    
    try:
        bot.run_testnet_trading()
    except KeyboardInterrupt:
        print("\n⏹️ 测试网交易停止")
        final_price = bot.get_market_price()
        if final_price:
            bot.report_status(final_price)

if __name__ == "__main__":
    start_testnet_trading()