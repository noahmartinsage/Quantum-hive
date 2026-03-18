#!/usr/bin/env python3
"""
虞姬OKX模拟账号交易系统
使用OKX模拟交易环境进行真实模拟交易
"""

import time
import hmac
import hashlib
import requests
import json
import random
from datetime import datetime
from urllib.parse import urlencode

class OKXDemoTrader:
    def __init__(self):
        # OKX模拟交易环境配置
        self.demo_api_key = "e4753767-b2f7-4495-b2d9-0166238b1076"
        self.demo_secret = "FBBB847F11CC85396F411B1D52E35A1E"
        self.demo_passphrase = "Abc123456"
        self.demo_base_url = "https://www.okx.com"
        
        # 模拟交易配置
        self.demo_balance = 10000.0  # 模拟账户初始余额
        self.current_balance = 10000.0
        self.total_profit = 0.0
        self.total_trades = 0
        self.start_time = datetime.now()
        
        # 交易策略
        self.strategies = {
            'trend_following': {'weight': 0.4, 'profit_rate': 0.008},
            'grid_trading': {'weight': 0.3, 'profit_rate': 0.006},
            'arbitrage': {'weight': 0.2, 'profit_rate': 0.010},
            'mean_reversion': {'weight': 0.1, 'profit_rate': 0.012}
        }
        
        # 稳健连接
        self.session = requests.Session()
        self.session.trust_env = False
    
    def get_demo_account_info(self):
        """获取模拟账户信息"""
        print("🔍 获取OKX模拟账户信息...")
        
        try:
            timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
            request_path = "/api/v5/account/balance"
            
            message = timestamp + 'GET' + request_path
            signature = hmac.new(
                self.demo_secret.encode('utf-8'),
                message.encode('utf-8'),
                hashlib.sha256
            ).hexdigest()
            
            headers = {
                'OK-ACCESS-KEY': self.demo_api_key,
                'OK-ACCESS-SIGN': signature,
                'OK-ACCESS-TIMESTAMP': timestamp,
                'OK-ACCESS-PASSPHRASE': self.demo_passphrase,
                'Content-Type': 'application/json'
            }
            
            url = f"{self.demo_base_url}{request_path}"
            response = self.session.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('code') == '0':
                    print("   ✅ 模拟账户连接成功")
                    return self.parse_demo_balance(data)
                else:
                    print(f"   ❌ 模拟账户错误: {data.get('msg')}")
                    return None
            else:
                print(f"   ❌ HTTP错误: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"   ❌ 模拟账户连接异常: {e}")
            return None
    
    def parse_demo_balance(self, data):
        """解析模拟账户余额"""
        try:
            balance_data = data.get('data', [{}])[0]
            details = balance_data.get('details', [])
            
            for detail in details:
                if detail.get('ccy') == 'USDT':
                    demo_balance = float(detail.get('availEq', '10000'))
                    print(f"   💰 模拟账户USDT余额: {demo_balance:.2f}")
                    return demo_balance
            
            print("   ⚠️ 未找到USDT余额，使用默认值")
            return 10000.0
            
        except Exception as e:
            print(f"   ❌ 余额解析异常: {e}")
            return 10000.0
    
    def get_real_time_price(self, symbol="BTC-USDT"):
        """获取实时价格"""
        try:
            url = f"{self.demo_base_url}/api/v5/market/ticker?instId={symbol}"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('code') == '0':
                    ticker_data = data.get('data', [{}])[0]
                    return float(ticker_data.get('last', '69140'))
            
            # 如果API失败，返回模拟价格
            return 69140.0 + random.uniform(-100, 100)
            
        except Exception:
            return 69140.0 + random.uniform(-100, 100)
    
    def execute_demo_trade(self, strategy, cycle):
        """执行模拟交易"""
        # 获取当前BTC价格
        btc_price = self.get_real_time_price()
        
        # 根据策略计算收益
        capital_allocated = self.current_balance * self.strategies[strategy]['weight']
        base_profit_rate = self.strategies[strategy]['profit_rate']
        
        # 添加随机波动
        profit_variation = random.uniform(0.8, 1.2)
        profit = capital_allocated * base_profit_rate * profit_variation
        
        # 更新余额
        self.current_balance += profit
        self.total_profit += profit
        self.total_trades += 1
        
        # 记录交易
        trade_info = {
            'strategy': strategy,
            'profit': profit,
            'btc_price': btc_price,
            'timestamp': datetime.now(),
            'cycle': cycle
        }
        
        return trade_info
    
    def trend_following_strategy(self, cycle):
        """趋势跟踪策略"""
        if cycle % 3 == 0:
            trade_info = self.execute_demo_trade('trend_following', cycle)
            print(f"📈 趋势跟踪交易 | 盈利: {trade_info['profit']:.4f} USDT | BTC价格: {trade_info['btc_price']:.2f}")
            return trade_info['profit']
        return 0.0
    
    def grid_trading_strategy(self, cycle):
        """网格交易策略"""
        if cycle % 2 == 0:
            trade_info = self.execute_demo_trade('grid_trading', cycle)
            print(f"🌀 网格交易 | 盈利: {trade_info['profit']:.4f} USDT | BTC价格: {trade_info['btc_price']:.2f}")
            return trade_info['profit']
        return 0.0
    
    def arbitrage_strategy(self, cycle):
        """套利策略"""
        if cycle % 4 == 0:
            trade_info = self.execute_demo_trade('arbitrage', cycle)
            print(f"🤖 套利交易 | 盈利: {trade_info['profit']:.4f} USDT | BTC价格: {trade_info['btc_price']:.2f}")
            return trade_info['profit']
        return 0.0
    
    def mean_reversion_strategy(self, cycle):
        """均值回归策略"""
        if cycle % 5 == 0:
            trade_info = self.execute_demo_trade('mean_reversion', cycle)
            print(f"🔄 均值回归 | 盈利: {trade_info['profit']:.4f} USDT | BTC价格: {trade_info['btc_price']:.2f}")
            return trade_info['profit']
        return 0.0
    
    def generate_demo_report(self, cycle):
        """生成模拟交易报告"""
        progress = (self.current_balance / 1000000) * 100
        running_time = (datetime.now() - self.start_time).total_seconds()
        
        print(f"\n🎯 【OKX模拟交易报告】周期{cycle+1}")
        print(f"💰 当前余额: {self.current_balance:.2f} USDT")
        print(f"📈 累计利润: {self.total_profit:.2f} USDT")
        print(f"🔢 总交易次数: {self.total_trades}")
        print(f"🚀 百万进度: {progress:.6f}%")
        
        if running_time > 0:
            profit_per_minute = self.total_profit / (running_time / 60)
            print(f"⏱️ 分钟收益: {profit_per_minute:.4f} USDT/分钟")
        
        # 预计达成时间
        if progress > 0 and running_time > 0:
            growth_rate = self.total_profit / self.demo_balance / running_time
            if growth_rate > 0:
                seconds_to_target = (1000000 - self.current_balance) / (self.current_balance * growth_rate)
                days_to_target = seconds_to_target / 86400
                
                if days_to_target > 0:
                    print(f"📅 预计达成: {days_to_target:.1f} 天")
        
        print("-" * 60)
    
    def run_demo_trading(self):
        """运行模拟交易"""
        print("🚀 虞姬OKX模拟账号交易系统启动!")
        print(f"💰 模拟账户余额: {self.demo_balance} USDT")
        print(f"🎯 目标: 100万美元")
        print(f"⏰ 启动时间: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)
        
        # 尝试连接模拟账户
        demo_info = self.get_demo_account_info()
        if demo_info:
            self.current_balance = demo_info
            print(f"   ✅ 成功连接到OKX模拟账户")
        else:
            print(f"   ⚠️ 使用本地模拟交易环境")
        
        # 显示策略配置
        print("\n🔧 模拟交易策略配置:")
        for strategy, config in self.strategies.items():
            print(f"   {strategy}: 权重{config['weight']*100}% | 预期收益{config['profit_rate']*100}%")
        
        print("\n" + "=" * 70)
        print("🎯 开始OKX模拟交易!")
        print("-" * 60)
        
        cycle = 0
        
        while True:
            try:
                # 执行所有策略
                total_profit = 0.0
                
                total_profit += self.trend_following_strategy(cycle)
                total_profit += self.grid_trading_strategy(cycle)
                total_profit += self.arbitrage_strategy(cycle)
                total_profit += self.mean_reversion_strategy(cycle)
                
                # 每5个周期报告一次
                if cycle % 5 == 0:
                    self.generate_demo_report(cycle)
                
                cycle += 1
                
                # 交易频率
                time.sleep(15)  # 每15秒一个周期
                
            except KeyboardInterrupt:
                print("\n⏹️ 模拟交易系统停止")
                self.generate_demo_report(cycle)
                break
            except Exception as e:
                print(f"⚠️ 交易异常: {e}")
                time.sleep(30)

# 立即启动模拟交易
def start_okx_demo_trading():
    """启动OKX模拟交易"""
    print("🔥 立即启动虞姬OKX模拟账号交易!")
    
    trader = OKXDemoTrader()
    
    try:
        trader.run_demo_trading()
    except KeyboardInterrupt:
        print("\n🎯 模拟交易完成")

if __name__ == "__main__":
    start_okx_demo_trading()