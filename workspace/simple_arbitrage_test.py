#!/usr/bin/env python3
"""
虞姬简单套利测试
"""

import random

def test_arbitrage():
    capital = 50.0
    profit = 0
    trades = 0
    
    print("🚀 虞姬套利测试开始")
    print(f"💰 初始资金: ${capital:.2f}")
    
    for i in range(10):
        # 模拟价格差异
        price_a = 100 + random.uniform(-2, 2)
        price_b = 100 + random.uniform(-2, 2)
        
        spread = abs(price_a - price_b)
        
        if spread > 1.5:
            trade_profit = capital * 0.1 * (spread / 100)
            capital += trade_profit
            profit += trade_profit
            trades += 1
            print(f"🎯 套利成功! 价差: {spread:.2f}% | 利润: ${trade_profit:.4f}")
    
    print(f"\n📊 测试结果:")
    print(f"💰 最终资金: ${capital:.2f}")
    print(f"📈 总利润: ${profit:.4f}")
    print(f"🔢 交易次数: {trades}")
    print(f"📈 收益率: {(profit / 50) * 100:.2f}%")

if __name__ == "__main__":
    test_arbitrage()