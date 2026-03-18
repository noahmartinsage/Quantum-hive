#!/usr/bin/env python3
"""
虞姬USDT高倍合约快速测试 v1.0
目标：10U起步，快速验证策略
"""

import random
import time
from datetime import datetime

def quick_usdt_trading_test():
    capital = 10.0  # 10 USDT
    position = 0.0
    leverage = 20
    profit = 0.0
    trades = 0
    winning_trades = 0
    base_price = 50000.0
    
    print("🚀 虞姬USDT高倍合约快速测试")
    print(f"💰 初始资金: {capital} USDT")
    print(f"📈 杠杆倍数: {leverage}x")
    print(f"🎯 交易对: BTCUSDT")
    print("-" * 50)
    
    # 模拟30分钟交易
    for minute in range(30):
        # 模拟价格波动
        volatility = random.uniform(-0.015, 0.015)  # ±1.5%
        current_price = base_price * (1 + volatility)
        base_price = current_price
        
        # 策略决策
        if minute % 5 == 0:  # 每5分钟交易一次
            # 网格交易策略
            if current_price < base_price * 0.98 and position < capital * 0.3:
                # 开多仓
                trade_size = capital * 0.1
                position_amount = (trade_size * leverage) / current_price
                position += position_amount
                capital -= trade_size
                
                print(f"🟢 开多仓 | 价格: {current_price:.2f} | 仓位: {trade_size:.2f} USDT")
                trades += 1
                
            elif current_price > base_price * 1.02 and position > 0:
                # 平多仓
                close_amount = position * 0.3
                pnl = (current_price - base_price) * close_amount
                
                if pnl > 0:
                    winning_trades += 1
                
                profit += pnl
                capital += pnl + (close_amount * base_price)
                position -= close_amount
                
                status = "✅ 盈利" if pnl > 0 else "❌ 亏损"
                print(f"🔴 平多仓 | 价格: {current_price:.2f} | {status} | PnL: {pnl:.4f} USDT")
                trades += 1
        
        # 每分钟报告
        total_value = capital + (position * current_price if position > 0 else 0)
        win_rate = winning_trades / trades if trades > 0 else 0
        
        print(f"⏰ {minute+1}分钟 | 总资产: {total_value:.4f} USDT | 利润: {profit:.4f} USDT | 胜率: {win_rate:.1%}")
        
        time.sleep(0.1)  # 快速测试
    
    print("-" * 50)
    print(f"📊 30分钟交易总结:")
    print(f"💰 最终资产: {total_value:.4f} USDT")
    print(f"📈 总利润: {profit:.4f} USDT")
    print(f"🔢 交易次数: {trades}")
    print(f"🎯 胜率: {win_rate:.1%}")
    print(f"📈 收益率: {(profit / 10) * 100:.2f}%")
    
    return total_value, profit, trades, win_rate

if __name__ == "__main__":
    quick_usdt_trading_test()