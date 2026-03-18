#!/usr/bin/env python3
"""
虞姬超快速测试 v1.0
立即验证交易逻辑，快速启动
"""

import random
from datetime import datetime

def ultra_fast_test():
    capital = 10.0
    position = 0.0
    profit = 0.0
    trades = 0
    winning_trades = 0
    base_price = 67000.0
    
    print("🚀 虞姬超快速测试启动")
    print(f"💰 初始资金: {capital} USDT")
    print(f"📈 目标: 100万美金")
    print("-" * 40)
    
    # 模拟30个交易周期
    for i in range(30):
        # 价格波动
        volatility = random.uniform(-0.03, 0.03)
        current_price = base_price * (1 + volatility)
        
        # 交易决策
        if i % 3 == 0:  # 每3个周期交易一次
            if current_price <= base_price * 0.97 and position < capital * 0.3:
                # 开多仓
                trade_size = capital * 0.15
                quantity = trade_size / current_price
                position += quantity
                capital -= trade_size
                trades += 1
                
                print(f"🟢 开多仓 | 价格: {current_price:.2f} | 仓位: {trade_size:.2f} USDT")
                base_price = current_price
                
            elif current_price >= base_price * 1.03 and position > 0:
                # 平多仓
                close_quantity = position * 0.4
                trade_value = close_quantity * current_price
                pnl = (current_price - base_price) * close_quantity
                
                profit += pnl
                capital += trade_value + pnl
                position -= close_quantity
                
                if pnl > 0:
                    winning_trades += 1
                    status = "✅ 盈利"
                else:
                    status = "❌ 亏损"
                
                trades += 1
                print(f"🔴 平多仓 | 价格: {current_price:.2f} | {status} | PnL: {pnl:.4f} USDT")
                base_price = current_price
        
        # 实时计算
        total_value = capital + (position * current_price)
        win_rate = winning_trades / trades if trades > 0 else 0
        progress = (total_value / 1000000) * 100
        
        print(f"⏰ 周期{i+1} | 总资产: {total_value:.4f} USDT | 利润: {profit:.4f} USDT | 胜率: {win_rate:.1%}")
    
    print("-" * 40)
    print(f"📊 快速测试总结:")
    print(f"💰 最终资产: {total_value:.4f} USDT")
    print(f"📈 总利润: {profit:.4f} USDT")
    print(f"🔢 交易次数: {trades}")
    print(f"🎯 胜率: {win_rate:.1%}")
    print(f"🚀 百万进度: {progress:.8f}%")
    
    # 计算年化收益率
    if profit > 0:
        annual_return = (profit / 10) * 100 * 52560  # 基于30周期年化
        print(f"📈 年化收益率: {annual_return:.2f}%")

if __name__ == "__main__":
    ultra_fast_test()