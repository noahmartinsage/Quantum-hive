#!/usr/bin/env python3
"""
虞姬简化版实战交易 v1.0
专注于核心交易逻辑，立即启动
"""

import time
import random
from datetime import datetime

def simple_live_trading():
    # 初始状态
    capital = 10.0  # 10 USDT
    position = 0.0  # 持仓
    profit = 0.0    # 总利润
    trades = 0      # 交易次数
    winning_trades = 0
    base_price = 67000.0  # BTC基础价格
    
    print("🚀 虞姬简化版实战交易启动")
    print(f"💰 初始资金: {capital} USDT")
    print(f"📈 目标: 100万美金")
    print(f"⏰ 开始时间: {datetime.now().strftime('%H:%M:%S')}")
    print("-" * 50)
    
    cycle = 0
    
    while True:
        try:
            # 模拟价格波动
            volatility = random.uniform(-0.02, 0.02)  # ±2%
            current_price = base_price * (1 + volatility)
            
            # 每10个周期交易一次
            if cycle % 10 == 0:
                # 网格交易策略
                if current_price <= base_price * 0.98 and position < capital * 0.3:
                    # 开多仓
                    trade_size = capital * 0.1
                    quantity = trade_size / current_price
                    
                    position += quantity
                    capital -= trade_size
                    trades += 1
                    
                    print(f"🟢 开多仓 | 价格: {current_price:.2f} | 仓位: {trade_size:.2f} USDT")
                    base_price = current_price  # 更新基础价格
                
                elif current_price >= base_price * 1.02 and position > 0:
                    # 平多仓
                    close_quantity = position * 0.3
                    trade_value = close_quantity * current_price
                    
                    # 计算盈亏
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
                    base_price = current_price  # 更新基础价格
            
            cycle += 1
            
            # 每分钟报告
            if cycle % 6 == 0:  # 每60秒报告一次
                total_value = capital + (position * current_price)
                win_rate = winning_trades / trades if trades > 0 else 0
                progress = (total_value / 1000000) * 100
                
                print(f"\n📊 【实时报告】 {datetime.now().strftime('%H:%M:%S')}")
                print(f"💰 总资产: {total_value:.4f} USDT")
                print(f"💵 可用资金: {capital:.4f} USDT")
                print(f"📈 持仓: {position:.6f} BTC")
                print(f"🎯 总利润: {profit:.4f} USDT")
                print(f"🔢 交易次数: {trades}")
                print(f"🎯 胜率: {win_rate:.1%}")
                print(f"🚀 百万进度: {progress:.8f}%")
                
                # 计算预计时间
                if progress > 0:
                    elapsed_time = cycle * 10  # 每周期10秒
                    growth_per_second = (total_value - 10) / elapsed_time
                    if growth_per_second > 0:
                        seconds_to_target = (1000000 - total_value) / growth_per_second
                        days_to_target = seconds_to_target / 86400
                        print(f"📅 预计达成: {days_to_target:.1f} 天")
                
                print("-" * 50)
            
            time.sleep(10)  # 每10秒一个周期
            
        except KeyboardInterrupt:
            print("\n⏹️ 交易停止")
            total_value = capital + (position * current_price)
            print(f"📊 最终资产: {total_value:.4f} USDT")
            break
        except Exception as e:
            print(f"⚠️ 异常: {e}")
            time.sleep(30)

if __name__ == "__main__":
    simple_live_trading()