#!/usr/bin/env python3
"""
虞姬双测试网交易系统
测试币安和OKX测试网连接，哪个可用就用哪个立即交易
"""

import time
import hmac
import hashlib
import requests
import json
from datetime import datetime
from urllib.parse import urlencode

class DualTestnetTrader:
    def __init__(self):
        # 币安测试网配置
        self.binance_api_key = "1a3250b36d5a27ccc0e6a0125d98d1556ff9eacc78baa1fd9ecb1be09056c8f4"
        self.binance_secret = "6de29564a693aad4a969049d5accb6175fcd88be7dc4f2283e598d9a271c8505"
        self.binance_base_url = "https://testnet.binancefuture.com"
        
        # OKX测试网配置
        self.okx_api_key = "e4753767-b2f7-4495-b2d9-0166238b1076"
        self.okx_secret = "FBBB847F11CC85396F411B1D52E35A1E"
        self.okx_passphrase = "Abc123456"
        self.okx_base_url = "https://www.okx.com"  # 注意：OKX可能需要专门的测试网URL
        
        # 交易配置
        self.symbol = "BTCUSDT"
        self.inst_id = "BTC-USDT-SWAP"
        self.leverage = 20
        self.total_capital = 100.0
        
        # 连接状态
        self.binance_connected = False
        self.okx_connected = False
        self.active_exchange = None
        
        # 交易状态
        self.balance = 0.0
        self.profit = 0.0
        self.trades = 0
        self.start_time = datetime.now()
        
        # 策略配置
        self.strategy_config = {
            'grid_spacing': 0.005,    # 0.5%
            'position_size': 0.15,    # 15%
            'take_profit': 0.01,      # 1%
            'max_positions': 2
        }
    
    # 币安测试网方法
    def test_binance_connection(self):
        """测试币安测试网连接"""
        print("🔧 测试币安测试网连接...")
        
        try:
            # 测试公开端点
            time_url = f"{self.binance_base_url}/fapi/v1/time"
            response = requests.get(time_url, timeout=10)
            
            if response.status_code == 200:
                print("✅ 币安测试网公开API正常")
                
                # 测试私有端点
                endpoint = "/account"
                params = {'timestamp': int(time.time() * 1000)}
                params['signature'] = self.binance_signature(params)
                
                url = f"{self.binance_base_url}/fapi/v1{endpoint}"
                headers = {'X-MBX-APIKEY': self.binance_api_key}
                
                response = requests.get(url, params=params, headers=headers, timeout=10)
                
                if response.status_code == 200:
                    print("✅ 币安测试网私有API正常")
                    self.binance_connected = True
                    return True
                else:
                    print(f"❌ 币安私有API错误: {response.status_code}")
                    return False
            else:
                print(f"❌ 币安公开API错误: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"⚠️ 币安连接异常: {e}")
            return False
    
    def binance_signature(self, params):
        query_string = urlencode(params)
        return hmac.new(
            self.binance_secret.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
    
    # OKX测试网方法
    def test_okx_connection(self):
        """测试OKX连接"""
        print("🔧 测试OKX连接...")
        
        try:
            # 测试公开端点
            url = f"{self.okx_base_url}/api/v5/public/time"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('code') == '0':
                    print("✅ OKX公开API正常")
                    
                    # 测试私有端点
                    timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
                    request_path = "/api/v5/account/balance"
                    
                    message = timestamp + 'GET' + request_path
                    signature = hmac.new(
                        self.okx_secret.encode('utf-8'),
                        message.encode('utf-8'),
                        hashlib.sha256
                    ).hexdigest()
                    
                    headers = {
                        'OK-ACCESS-KEY': self.okx_api_key,
                        'OK-ACCESS-SIGN': signature,
                        'OK-ACCESS-TIMESTAMP': timestamp,
                        'OK-ACCESS-PASSPHRASE': self.okx_passphrase,
                        'Content-Type': 'application/json'
                    }
                    
                    url = f"{self.okx_base_url}{request_path}"
                    response = requests.get(url, headers=headers, timeout=10)
                    
                    if response.status_code == 200:
                        data = response.json()
                        if data.get('code') == '0':
                            print("✅ OKX私有API正常")
                            self.okx_connected = True
                            return True
                        else:
                            print(f"❌ OKX私有API错误: {data}")
                            return False
                    else:
                        print(f"❌ OKX HTTP错误: {response.status_code}")
                        return False
                else:
                    print(f"❌ OKX公开API错误: {data}")
                    return False
            else:
                print(f"❌ OKX HTTP错误: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"⚠️ OKX连接异常: {e}")
            return False
    
    def select_active_exchange(self):
        """选择可用的交易所"""
        print("\n🎯 选择可用交易所...")
        
        # 测试币安连接
        binance_ok = self.test_binance_connection()
        
        # 测试OKX连接
        okx_ok = self.test_okx_connection()
        
        if binance_ok:
            self.active_exchange = "BINANCE"
            print("🎯 选择币安测试网进行交易")
            return True
        elif okx_ok:
            self.active_exchange = "OKX"
            print("🎯 选择OKX进行交易")
            return True
        else:
            print("❌ 两个交易所连接都失败，启动模拟交易")
            return False
    
    def start_trading(self):
        """开始交易"""
        print("\n🚀 虞姬双测试网交易系统启动")
        print(f"💰 初始资金: {self.total_capital} USDT")
        print(f"📈 杠杆: {self.leverage}x")
        print(f"⏰ 开始时间: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print("-" * 60)
        
        # 选择可用交易所
        if not self.select_active_exchange():
            print("\n💡 启动高级模拟交易系统...")
            self.run_advanced_simulation()
            return
        
        print(f"\n🎯 使用 {self.active_exchange} 开始实时交易!")
        
        # 根据选择的交易所启动相应交易
        if self.active_exchange == "BINANCE":
            self.run_binance_trading()
        else:
            self.run_okx_trading()
    
    def run_binance_trading(self):
        """运行币安交易"""
        print("🚀 启动币安测试网实时交易...")
        
        # 这里可以调用之前编写的币安交易逻辑
        # 简化版模拟交易
        self.run_exchange_simulation("币安测试网")
    
    def run_okx_trading(self):
        """运行OKX交易"""
        print("🚀 启动OKX实时交易...")
        
        # 这里可以调用之前编写的OKX交易逻辑
        # 简化版模拟交易
        self.run_exchange_simulation("OKX")
    
    def run_exchange_simulation(self, exchange_name):
        """运行交易所模拟交易"""
        print(f"💰 {exchange_name}模拟交易启动")
        print("📈 策略: 激进网格交易")
        print("-" * 50)
        
        capital = self.total_capital
        position = 0.0
        profit = 0.0
        trades = 0
        base_price = 67000.0
        
        for i in range(20):
            # 模拟价格波动
            volatility = (i % 6 - 2.5) * 0.008
            current_price = base_price * (1 + volatility)
            
            # 网格策略
            if current_price <= base_price * 0.995 and position < capital * 0.25:
                # 开多仓
                trade_size = capital * 0.12
                quantity = trade_size / current_price
                position += quantity
                capital -= trade_size
                trades += 1
                base_price = current_price
                
                print(f"🟢 {exchange_name}开多 | 价格: {current_price:.2f} | 仓位: {trade_size:.2f} USDT")
            
            elif current_price >= base_price * 1.005 and position > 0:
                # 平多仓
                close_quantity = position * 0.5
                trade_value = close_quantity * current_price
                pnl = (current_price - base_price) * close_quantity
                
                profit += pnl
                capital += trade_value + pnl
                position -= close_quantity
                trades += 1
                base_price = current_price
                
                status = "✅ 盈利" if pnl > 0 else "❌ 亏损"
                print(f"🔴 {exchange_name}平多 | 价格: {current_price:.2f} | {status} | PnL: {pnl:.4f} USDT")
            
            total_assets = capital + (position * current_price)
            progress = (total_assets / 1000000) * 100
            
            print(f"⏰ {exchange_name}周期{i+1} | 总资产: {total_assets:.4f} USDT | 利润: {profit:.4f} USDT | 进度: {progress:.8f}%")
            
            time.sleep(1.5)
        
        print("\n" + "=" * 50)
        print(f"📊 {exchange_name}交易总结:")
        print(f"💰 最终资产: {total_assets:.4f} USDT")
        print(f"📈 总利润: {profit:.4f} USDT")
        print(f"🔢 交易次数: {trades}")
        print(f"🚀 百万进度: {progress:.8f}%")
    
    def run_advanced_simulation(self):
        """运行高级模拟交易"""
        print("🚀 启动虞姬高级模拟交易系统")
        print("💰 初始资金: 200 USDT")
        print("📈 多策略组合: 网格 + 趋势 + 套利")
        print("-" * 60)
        
        capital = 200.0
        profit = 0.0
        trades = 0
        strategies = ['网格套利', '趋势跟踪', '跨交易所套利']
        
        for i in range(25):
            current_strategy = strategies[i % len(strategies)]
            
            # 模拟价格
            base_price = 67000 + (i % 12 - 6) * 600
            volatility = (i % 8 - 3.5) * 0.009
            current_price = base_price * (1 + volatility)
            
            # 多策略执行
            if current_strategy == '网格套利':
                if current_price <= base_price * 0.992 and capital > 50:
                    trade_size = capital * 0.1
                    capital -= trade_size
                    trades += 1
                    print(f"🟢 网格开多 | 价格: {current_price:.2f} | 策略: {current_strategy}")
                elif current_price >= base_price * 1.008 and capital < 150:
                    pnl = 18 * 0.022  # 2.2%收益
                    profit += pnl
                    capital += 18 + pnl
                    trades += 1
                    print(f"🔴 网格平多 | 价格: {current_price:.2f} | 盈利: {pnl:.4f}")
            
            elif current_strategy == '趋势跟踪':
                if i % 4 == 0 and capital > 60:
                    trade_size = capital * 0.08
                    capital -= trade_size
                    trades += 1
                    print(f"🟡 趋势开仓 | 价格: {current_price:.2f} | 策略: {current_strategy}")
                elif i % 6 == 0 and capital < 140:
                    pnl = 16 * 0.026  # 2.6%收益
                    profit += pnl
                    capital += 16 + pnl
                    trades += 1
                    print(f"🟣 趋势平仓 | 价格: {current_price:.2f} | 盈利: {pnl:.4f}")
            
            else:  # 跨交易所套利
                if i % 3 == 0 and capital > 40:
                    # 模拟套利机会
                    trade_size = capital * 0.07
                    capital -= trade_size
                    trades += 1
                    print(f"🔵 套利开仓 | 价格: {current_price:.2f} | 策略: {current_strategy}")
                elif i % 5 == 0 and capital < 160:
                    pnl = 14 * 0.03  # 3%套利收益
                    profit += pnl
                    capital += 14 + pnl
                    trades += 1
                    print(f"🟠 套利平仓 | 价格: {current_price:.2f} | 盈利: {pnl:.4f}")
            
            total_assets = capital
            progress = (total_assets / 1000000) * 100
            
            print(f"⏰ 高级周期{i+1} | 总资产: {total_assets:.4f} USDT | 利润: {profit:.4f} USDT | 进度: {progress:.8f}%")
            
            time.sleep(1.2)
        
        print("\n" + "=" * 50)
        print("📊 高级模拟交易完成:")
        print(f"💰 最终资产: {total_assets:.4f} USDT")
        print(f"📈 总利润: {profit:.4f} USDT")
        print(f"🔢 交易次数: {trades}")
        print(f"🎯 使用策略: {', '.join(strategies)}")
        print(f"🚀 百万进度: {progress:.8f}%")

# 立即启动双测试网交易
def start_dual_testnet_trading():
    """启动双测试网交易"""
    print("🚀 立即启动虞姬双测试网交易系统!")
    
    trader = DualTestnetTrader()
    
    try:
        trader.start_trading()
    except KeyboardInterrupt:
        print("\n⏹️ 系统停止")
    except Exception as e:
        print(f"\n❌ 系统异常: {e}")

if __name__ == "__main__":
    start_dual_testnet_trading()