#!/usr/bin/env python3
"""
虞姬USDT激进高倍合约测试 v1.1
目标：10U起步，高频率交易
策略：更激进的网格交易
"""

import random
import time
from datetime import datetime

def aggressive_usdt_trading():
    capital = 10.0  # 10 USDT
    position = 0.0
    leverage = 20
    profit = 0.0
    trades = 0
    winning_trades = 0
    base_price = 50000.0
    
    print("🚀 虞姬USDT激进高倍合约测试")
    print(f"💰 初始资金: {capital} USDT")
    print(f"📈 杠杆倍数: {leverage}x")
    print(f"⚡ 交易频率: 高")
    print("-" * 50)
    
    # 模拟15分钟交易
    for minute in range(15):
        # 模拟更大价格波动
        volatility = random.uniform(-0.03, 0.03)  # ±3%
        current_price = base_price * (1 + volatility)
        
        # 每2分钟交易一次
        if minute % 2 == 0:
            # 网格交易策略（更激进）
            grid_buy_price = base_price * 0.97  # 下跌3%买入
            grid_sell_price = base_price * 1.03  # 上涨3%卖出
            
            if current_price <= grid_buy_price and position < capital * 0.5:
                # 开多仓
                trade_size = capital * 0.2  # 20%仓位
                position_amount = (trade_size * leverage) / current_price
                position += position_amount
                capital -= trade_size
                entry_price = current_price
                
                print(f"🟢 激进开多 | 价格: {current_price:.2f} | 仓位: {trade_size:.2f} USDT")
                trades += 1
                
                # 立即设置止盈止损
                take_profit = entry_price * 1.05  # 5%止盈
                stop_loss = entry_price * 0.98    # 2%止损
                
            elif current_price >= grid_sell_price and position > 0:
                # 平多仓
                close_amount = position * 0.5  # 平一半仓位
                pnl = (current_price - base_price) * close_amount
                
                if pnl > 0:
                    winning_trades += 1
                    status = "✅ 盈利"
                else:
                    status = "❌ 亏损"
                
                profit += pnl
                capital += pnl + (close_amount * base_price)
                position -= close_amount
                
                print(f"🔴 平多仓 | 价格: {current_price:.2f} | {status} | PnL: {pnl:.4f} USDT")
                trades += 1
        
        # 更新基础价格
        base_price = current_price
        
        # 每分钟报告
        total_value = capital + (position * current_price if position > 0 else 0)
        win_rate = winning_trades / trades if trades > 0 else 0
        
        print(f"⏰ {minute+1}分钟 | 总资产: {total_value:.4f} USDT | 利润: {profit:.4f} USDT | 胜率: {win_rate:.1%}")
        
        time.sleep(0.1)  # 快速测试
    
    print("-" * 50)
    print(f"📊 15分钟激进交易总结:")
    print(f"💰 最终资产: {total_value:.4f} USDT")
    print(f"📈 总利润: {profit:.4f} USDT")
    print(f"🔢 交易次数: {trades}")
    print(f"🎯 胜率: {win_rate:.1%}")
    print(f"📈 收益率: {(profit / 10) * 100:.2f}%")
    
    # 计算年化收益率
    if profit > 0:
        annual_return = (profit / 10) * 100 * 35040  # 15分钟测试，年化计算
        print(f"🚀 年化收益率: {annual_return:.2f}%")
    
    return total_value, profit, trades, win_rate

if __name__ == "__main__":
    aggressive_usdt_trading()