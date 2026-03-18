#!/usr/bin/env python3
"""
虞姬OKX V5交易系统
在OKX V5系统进行真实交易配置
"""

import time
import hmac
import hashlib
import requests
import json
from datetime import datetime

class OKXV5Trader:
    def __init__(self):
        # OKX V5 API配置
        self.api_key = "e4753767-b2f7-4495-b2d9-0166238b1076"
        self.secret = "FBBB847F11CC85396F411B1D52E35A1E"
        self.passphrase = "Abc123456"
        self.base_url = "https://www.okx.com"
        
        # 交易配置
        self.inst_id = "BTC-USDT-SWAP"
        self.leverage = 20
        self.total_capital = 100.0
        
        # 账户状态
        self.balance = 0.0
        self.positions = {}
        self.profit = 0.0
        self.trades = 0
        self.start_time = datetime.now()
        
        # V5交易策略
        self.strategy_config = {
            'grid_spacing': 0.005,    # 0.5%
            'position_size': 0.15,    # 15%
            'take_profit': 0.01,      # 1%
            'stop_loss': 0.005,       # 0.5%
            'td_mode': 'cross'        # 全仓模式
        }
    
    def generate_signature(self, timestamp, method, request_path, body=""):
        """生成V5签名"""
        message = timestamp + method + request_path + body
        signature = hmac.new(
            self.secret.encode('utf-8'),
            message.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        return signature
    
    def send_request(self, endpoint, params=None, method='GET'):
        """发送V5 API请求"""
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
                    print(f"❌ V5 API错误: {data}")
                    return None
            else:
                print(f"❌ V5 HTTP错误 {response.status_code}: {response.text}")
                return None
        except Exception as e:
            print(f"⚠️ V5请求异常: {e}")
            return None
    
    def get_account_balance(self):
        """获取V5账户余额"""
        endpoint = "/account/balance"
        balance_data = self.send_request(endpoint)
        
        if balance_data and len(balance_data) > 0:
            for detail in balance_data[0]['details']:
                if detail['ccy'] == 'USDT':
                    self.balance = float(detail['availEq'])
                    print(f"💰 V5账户余额: {self.balance} USDT")
                    return True
        return False
    
    def get_positions(self):
        """获取V5持仓信息"""
        endpoint = "/account/positions"
        positions_data = self.send_request(endpoint)
        
        if positions_data:
            self.positions = {}
            for position in positions_data:
                if position['instId'] == self.inst_id and float(position['pos']) != 0:
                    self.positions[self.inst_id] = {
                        'pos': float(position['pos']),
                        'avgPx': float(position['avgPx']),
                        'upl': float(position['upl'])
                    }
            if self.positions:
                print(f"📈 V5持仓信息: {self.positions}")
            else:
                print("📈 V5当前无持仓")
        return self.positions
    
    def get_market_price(self):
        """获取V5市场价格"""
        endpoint = "/market/ticker"
        params = {'instId': self.inst_id}
        price_data = self.send_request(endpoint, params)
        
        if price_data and len(price_data) > 0:
            price = float(price_data[0]['last'])
            print(f"🎯 V5市场价格: {price:.2f} USDT")
            return price
        return None
    
    def set_leverage(self):
        """设置V5杠杆"""
        endpoint = "/account/set-leverage"
        params = {
            'instId': self.inst_id,
            'lever': str(self.leverage),
            'mgnMode': self.strategy_config['td_mode']
        }
        result = self.send_request(endpoint, params, 'POST')
        
        if result:
            print(f"✅ V5杠杆设置成功: {self.leverage}x")
            return True
        else:
            print("⚠️ V5杠杆设置失败")
            return False
    
    def place_market_order(self, side, size):
        """下V5市价单"""
        endpoint = "/trade/order"
        params = {
            'instId': self.inst_id,
            'tdMode': self.strategy_config['td_mode'],
            'side': side,
            'ordType': 'market',
            'sz': str(size)
        }
        
        result = self.send_request(endpoint, params, 'POST')
        
        if result and len(result) > 0:
            self.trades += 1
            ord_id = result[0]['ordId']
            print(f"✅ V5市价单成功 | {side} | 数量: {size} | 订单ID: {ord_id}")
            return True
        
        print(f"❌ V5下单失败 | {side} | 数量: {size}")
        return False
    
    def v5_grid_strategy(self, current_price):
        """V5网格策略"""
        if not hasattr(self, 'base_price'):
            self.base_price = current_price
            print(f"🎯 V5设置基础价格: {self.base_price:.2f}")
        
        # 网格买入点 (0.5%下跌)
        buy_price = self.base_price * (1 - self.strategy_config['grid_spacing'])
        if current_price <= buy_price and self.balance > 0:
            # 开多仓
            trade_size = self.balance * self.strategy_config['position_size']
            size = trade_size / current_price
            
            if size >= 0.001:  # 最小交易量
                if self.place_market_order('buy', round(size, 6)):
                    self.base_price = current_price
                    return "BUY"
        
        # 网格卖出点 (0.5%上涨)
        sell_price = self.base_price * (1 + self.strategy_config['grid_spacing'])
        if current_price >= sell_price and self.inst_id in self.positions:
            # 平多仓
            position_size = abs(self.positions[self.inst_id]['pos'])
            if position_size >= 0.001:
                if self.place_market_order('sell', round(position_size, 6)):
                    # 记录盈亏
                    entry_price = self.positions[self.inst_id]['avgPx']
                    pnl = (current_price - entry_price) * position_size
                    self.profit += pnl
                    print(f"🎯 V5平仓盈亏: {pnl:.4f} USDT")
                    self.base_price = current_price
                    return "SELL"
        
        return "HOLD"
    
    def initialize_v5_trading(self):
        """初始化V5交易"""
        print("🔧 初始化OKX V5交易系统...")
        
        # 设置杠杆
        if not self.set_leverage():
            return False
        
        # 获取初始余额
        if not self.get_account_balance():
            return False
        
        # 获取初始价格
        initial_price = self.get_market_price()
        if not initial_price:
            return False
        
        self.base_price = initial_price
        print("✅ V5交易系统初始化完成")
        return True
    
    def run_v5_live_trading(self):
        """运行V5实时交易"""
        print("🚀 虞姬OKX V5实时交易启动")
        print(f"💰 初始资金: {self.total_capital} USDT")
        print(f"📈 杠杆: {self.leverage}x")
        print(f"🎯 交易对: {self.inst_id}")
        print(f"⚡ 策略: V5网格交易 (0.5%触发)")
        print(f"⏰ 开始时间: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print("-" * 60)
        
        # 初始化
        if not self.initialize_v5_trading():
            print("❌ V5系统初始化失败，启动V5模拟模式")
            self.run_v5_simulation()
            return
        
        last_report_time = time.time()
        cycle = 0
        
        while True:
            try:
                # 获取市场数据
                current_price = self.get_market_price()
                if not current_price:
                    print("⏳ 等待V5价格数据...")
                    time.sleep(30)
                    continue
                
                # 更新账户状态
                self.get_account_balance()
                self.get_positions()
                
                # 每3个周期执行一次交易
                if cycle % 3 == 0:
                    action = self.v5_grid_strategy(current_price)
                    if action != "HOLD":
                        print(f"🎯 V5执行动作: {action}")
                
                cycle += 1
                
                # 每分钟报告状态
                current_time = time.time()
                if current_time - last_report_time >= 60:
                    self.report_v5_status(current_price)
                    last_report_time = current_time
                
                time.sleep(20)  # 每20秒检查一次
                
            except KeyboardInterrupt:
                print("\n⏹️ V5实时交易停止")
                final_price = self.get_market_price()
                if final_price:
                    self.report_v5_status(final_price)
                break
            except Exception as e:
                print(f"⚠️ V5交易异常: {e}")
                time.sleep(30)
    
    def run_v5_simulation(self):
        """运行V5模拟交易"""
        print("🚀 启动虞姬V5模拟交易系统")
        print("💰 初始资金: 100 USDT")
        print("📈 策略: V5网格交易")
        print("-" * 60)
        
        capital = 100.0
        position = 0.0
        profit = 0.0
        trades = 0
        base_price = 67000.0
        
        for i in range(12):
            # 模拟价格波动
            volatility = (i % 5 - 2) * 0.007
            current_price = base_price * (1 + volatility)
            
            # V5网格策略
            if current_price <= base_price * 0.995 and position < capital * 0.3:
                # 开多仓
                trade_size = capital * 0.15
                quantity = trade_size / current_price
                position += quantity
                capital -= trade_size
                trades += 1
                base_price = current_price
                
                print(f"🟢 V5模拟开多 | 价格: {current_price:.2f} | 仓位: {trade_size:.2f} USDT")
            
            elif current_price >= base_price * 1.005 and position > 0:
                # 平多仓
                close_quantity = position * 0.6
                trade_value = close_quantity * current_price
                pnl = (current_price - base_price) * close_quantity
                
                profit += pnl
                capital += trade_value + pnl
                position -= close_quantity
                trades += 1
                base_price = current_price
                
                status = "✅ 盈利" if pnl > 0 else "❌ 亏损"
                print(f"🔴 V5模拟平多 | 价格: {current_price:.2f} | {status} | PnL: {pnl:.4f} USDT")
            
            total_assets = capital + (position * current_price)
            progress = (total_assets / 1000000) * 100
            
            print(f"⏰ V5周期{i+1} | 总资产: {total_assets:.4f} USDT | 利润: {profit:.4f} USDT | 进度: {progress:.8f}%")
            
            time.sleep(2)
        
        print("\n" + "=" * 50)
        print("📊 V5模拟交易总结:")
        print(f"💰 最终资产: {total_assets:.4f} USDT")
        print(f"📈 总利润: {profit:.4f} USDT")
        print(f"🔢 交易次数: {trades}")
        print(f"🚀 百万进度: {progress:.8f}%")
    
    def report_v5_status(self, current_price):
        """报告V5状态"""
        total_assets = self.balance
        position_value = 0
        
        if self.inst_id in self.positions:
            position_value = abs(self.positions[self.inst_id]['pos']) * current_price
            total_assets += position_value
        
        progress = (total_assets / 1000000) * 100
        running_time = (datetime.now() - self.start_time).total_seconds()
        
        print(f"\n📊 【V5交易报告】 {datetime.now().strftime('%H:%M:%S')}")
        print(f"💰 总资产: {total_assets:.4f} USDT")
        print(f"💵 可用余额: {self.balance:.4f} USDT")
        print(f"📈 持仓价值: {position_value:.4f} USDT")
        print(f"🎯 总利润: {self.profit:.4f} USDT")
        print(f"🔢 交易次数: {self.trades}")
        print(f"🚀 百万进度: {progress:.8f}%")
        print(f"⏱️ 运行时间: {running_time:.0f}秒")
        
        if progress > 0 and running_time > 0:
            growth_rate = (total_assets - self.total_capital) / self.total_capital / running_time
            if growth_rate > 0:
                days_to_target = (1000000 - total_assets) / (total_assets * growth_rate * 86400)
                if days_to_target > 0:
                    print(f"📅 预计达成: {days_to_target:.1f} 天")
        
        print("-" * 60)

# 立即启动V5交易
def start_okx_v5_trading():
    """启动OKX V5交易"""
    print("🚀 立即启动虞姬OKX V5交易系统!")
    
    trader = OKXV5Trader()
    
    try:
        trader.run_v5_live_trading()
    except KeyboardInterrupt:
        print("\n⏹️ V5系统停止")

if __name__ == "__main__":
    start_okx_v5_trading()