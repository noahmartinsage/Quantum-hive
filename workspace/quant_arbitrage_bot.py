#!/usr/bin/env python3
"""
虞姬量化套利机器人 v1.0
目标：用1-100美元实现小额套利
策略：跨交易所价格差异套利
"""

import time
import random
from datetime import datetime

class ArbitrageBot:
    def __init__(self, initial_capital):
        self.capital = initial_capital
        self.profit = 0
        self.trades = 0
        self.start_time = datetime.now()
        
    def simulate_exchange_prices(self):
        """模拟两个交易所的价格差异"""
        base_price = 100.0  # 基础价格
        exchange_a = base_price + random.uniform(-2, 2)
        exchange_b = base_price + random.uniform(-2, 2)
        return exchange_a, exchange_b
    
    def find_arbitrage_opportunity(self, price_a, price_b):
        """寻找套利机会"""
        spread = abs(price_a - price_b)
        if spread > 1.5:  # 价差大于1.5%时套利
            if price_a < price_b:
                return "buy_a_sell_b", spread
            else:
                return "buy_b_sell_a", spread
        return None, 0
    
    def execute_trade(self, strategy, spread):
        """执行交易"""
        trade_amount = min(self.capital * 0.1, 10)  # 每次交易不超过资本的10%或10美元
        
        if strategy == "buy_a_sell_b":
            # 在A交易所低价买入，在B交易所高价卖出
            profit = trade_amount * (spread / 100)
        else:
            # 在B交易所低价买入，在A交易所高价卖出
            profit = trade_amount * (spread / 100)
            
        self.capital += profit
        self.profit += profit
        self.trades += 1
        
        return profit
    
    def run_simulation(self, duration_minutes=60):
        """运行模拟"""
        print(f"🚀 虞姬套利机器人启动")
        print(f"💰 初始资金: ${self.capital:.2f}")
        print(f"⏰ 运行时长: {duration_minutes}分钟")
        print("-" * 40)
        
        start_time = time.time()
        end_time = start_time + (duration_minutes * 60)
        
        while time.time() < end_time:
            # 获取价格
            price_a, price_b = self.simulate_exchange_prices()
            
            # 寻找套利机会
            strategy, spread = self.find_arbitrage_opportunity(price_a, price_b)
            
            if strategy:
                profit = self.execute_trade(strategy, spread)
                print(f"🎯 套利机会 | 策略: {strategy} | 价差: {spread:.2f}% | 利润: ${profit:.4f}")
            
            # 每秒检查一次
            time.sleep(1)
        
        # 输出结果
        print("-" * 40)
        print(f"📊 交易总结:")
        print(f"💰 最终资金: ${self.capital:.2f}")
        print(f"📈 总利润: ${self.profit:.4f}")
        print(f"🔢 交易次数: {self.trades}")
        print(f"⏱️ 运行时间: {duration_minutes}分钟")
        
        return self.capital, self.profit, self.trades

# 测试机器人
def test_arbitrage_bot():
    """测试套利机器人"""
    print("🧪 开始测试虞姬套利机器人...")
    
    # 用50美元启动
    bot = ArbitrageBot(50.0)
    final_capital, total_profit, total_trades = bot.run_simulation(5)  # 5分钟测试
    
    print(f"\n🎉 测试完成!")
    print(f"📈 收益率: {(total_profit / 50) * 100:.2f}%")
    
    return final_capital, total_profit, total_trades

if __name__ == "__main__":
    test_arbitrage_bot()