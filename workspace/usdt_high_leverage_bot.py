#!/usr/bin/env python3
"""
虞姬USDT高倍合约量化交易机器人 v1.0
目标：10U起步，高倍杠杆，7*24小时运行
策略：趋势跟踪 + 网格交易 + 风险控制
"""

import random
import time
from datetime import datetime
import json

class USDTContractBot:
    def __init__(self, initial_capital=10.0):
        self.capital = initial_capital  # USDT
        self.position = 0.0  # 持仓数量
        self.leverage = 20   # 20倍杠杆
        self.profit = 0.0
        self.trades = 0
        self.winning_trades = 0
        self.start_time = datetime.now()
        self.running = True
        
        # 交易对配置
        self.symbol = "BTCUSDT"
        self.base_price = 50000.0  # BTC基础价格
        
        # 风险控制
        self.risk_management = {
            'max_position_size': 0.5,  # 单笔最大仓位50%
            'stop_loss': 0.05,        # 5%止损
            'take_profit': 0.10,      # 10%止盈
            'max_daily_loss': 0.02,   # 单日最大亏损2%
            'grid_levels': 5,         # 网格层级
            'grid_spacing': 0.02      # 网格间距2%
        }
        
        # 交易记录
        self.trade_history = []
        
    def get_market_data(self):
        """获取市场数据（模拟真实价格波动）"""
        # 模拟BTC价格波动
        volatility = random.uniform(-0.02, 0.02)  # ±2%波动
        price = self.base_price * (1 + volatility)
        
        # 更新基础价格
        self.base_price = price
        
        return {
            'symbol': self.symbol,
            'price': price,
            'timestamp': datetime.now(),
            'volume': random.uniform(1000, 5000),
            'bid_ask_spread': random.uniform(0.0001, 0.0005)
        }
    
    def analyze_trend(self, market_data):
        """分析趋势"""
        price = market_data['price']
        volume = market_data['volume']
        
        # 简单趋势判断
        if volume > 3000:
            # 高成交量，趋势较强
            if price > self.base_price * 1.005:  # 上涨0.5%
                return "BULLISH", 0.7
            elif price < self.base_price * 0.995:  # 下跌0.5%
                return "BEARISH", 0.7
        
        return "NEUTRAL", 0.3
    
    def grid_trading_strategy(self, market_data):
        """网格交易策略"""
        price = market_data['price']
        trend, confidence = self.analyze_trend(market_data)
        
        # 计算网格位置
        grid_levels = self.risk_management['grid_levels']
        grid_spacing = self.risk_management['grid_spacing']
        
        actions = []
        
        # 多头网格
        for i in range(1, grid_levels + 1):
            buy_price = self.base_price * (1 - i * grid_spacing)
            if price <= buy_price and self.position < self.capital * 0.3:
                actions.append({
                    'action': 'BUY',
                    'price': buy_price,
                    'size': self.capital * 0.1,
                    'type': 'GRID_BUY',
                    'confidence': 0.8
                })
        
        # 空头网格
        for i in range(1, grid_levels + 1):
            sell_price = self.base_price * (1 + i * grid_spacing)
            if price >= sell_price and self.position > 0:
                actions.append({
                    'action': 'SELL',
                    'price': sell_price,
                    'size': self.position * 0.2,
                    'type': 'GRID_SELL',
                    'confidence': 0.8
                })
        
        return actions
    
    def trend_following_strategy(self, market_data):
        """趋势跟踪策略"""
        trend, confidence = self.analyze_trend(market_data)
        
        if trend == "BULLISH" and confidence > 0.6:
            return {
                'action': 'BUY',
                'size': self.capital * 0.15,
                'type': 'TREND_BUY',
                'confidence': confidence
            }
        elif trend == "BEARISH" and confidence > 0.6 and self.position > 0:
            return {
                'action': 'SELL',
                'size': self.position * 0.3,
                'type': 'TREND_SELL',
                'confidence': confidence
            }
        
        return None
    
    def execute_trade(self, trade_signal, market_data):
        """执行交易"""
        if trade_signal['action'] == 'BUY':
            # 开多仓
            trade_size = min(trade_signal['size'], 
                           self.capital * self.risk_management['max_position_size'])
            
            # 计算杠杆后仓位
            leveraged_position = trade_size * self.leverage
            entry_price = market_data['price']
            
            # 模拟交易执行
            self.position += leveraged_position / entry_price
            self.capital -= trade_size
            
            trade_record = {
                'timestamp': datetime.now(),
                'action': 'BUY',
                'size': trade_size,
                'price': entry_price,
                'type': trade_signal['type'],
                'leverage': self.leverage
            }
            
        else:  # SELL
            # 平仓
            close_size = min(trade_signal['size'], self.position)
            exit_price = market_data['price']
            
            # 计算盈亏
            if len(self.trade_history) > 0:
                last_buy = [t for t in self.trade_history if t['action'] == 'BUY'][-1]
                pnl = (exit_price - last_buy['price']) * close_size
                
                self.profit += pnl
                self.capital += pnl + (close_size * last_buy['price'])
                
                if pnl > 0:
                    self.winning_trades += 1
                
                self.trades += 1
            
            self.position -= close_size
            
            trade_record = {
                'timestamp': datetime.now(),
                'action': 'SELL',
                'size': close_size,
                'price': exit_price,
                'type': trade_signal['type'],
                'pnl': pnl if 'pnl' in locals() else 0
            }
        
        self.trade_history.append(trade_record)
        return trade_record
    
    def calculate_account_status(self):
        """计算账户状态"""
        total_value = self.capital + (self.position * self.base_price if self.position > 0 else 0)
        
        return {
            'total_value': total_value,
            'capital': self.capital,
            'position': self.position,
            'profit': self.profit,
            'trades': self.trades,
            'win_rate': self.winning_trades / self.trades if self.trades > 0 else 0,
            'running_time': (datetime.now() - self.start_time).total_seconds()
        }
    
    def run_24_7_trading(self, report_interval=300):  # 每5分钟报告一次
        """7*24小时运行交易"""
        print(f"🚀 虞姬USDT高倍合约机器人启动")
        print(f"💰 初始资金: {self.capital} USDT")
        print(f"📈 杠杆倍数: {self.leverage}x")
        print(f"⏰ 运行模式: 7*24小时")
        print(f"📊 报告间隔: {report_interval}秒")
        print("-" * 60)
        
        last_report_time = time.time()
        
        while self.running:
            try:
                # 获取市场数据
                market_data = self.get_market_data()
                
                # 执行策略
                grid_signals = self.grid_trading_strategy(market_data)
                trend_signal = self.trend_following_strategy(market_data)
                
                # 执行交易
                executed_trades = []
                
                if grid_signals:
                    for signal in grid_signals:
                        trade = self.execute_trade(signal, market_data)
                        executed_trades.append(trade)
                
                if trend_signal:
                    trade = self.execute_trade(trend_signal, market_data)
                    executed_trades.append(trade)
                
                # 报告账户状态
                current_time = time.time()
                if current_time - last_report_time >= report_interval:
                    account_status = self.calculate_account_status()
                    self.report_status(account_status, executed_trades)
                    last_report_time = current_time
                
                # 每10秒检查一次
                time.sleep(10)
                
            except Exception as e:
                print(f"⚠️ 交易异常: {e}")
                time.sleep(30)
    
    def report_status(self, account_status, executed_trades):
        """报告账户状态"""
        print(f"\n📊 【虞姬合约交易报告】 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"💰 总资产: {account_status['total_value']:.4f} USDT")
        print(f"💵 可用资金: {account_status['capital']:.4f} USDT")
        print(f"📈 持仓数量: {account_status['position']:.6f} BTC")
        print(f"🎯 总利润: {account_status['profit']:.4f} USDT")
        print(f"🔢 交易次数: {account_status['trades']}")
        print(f"🎯 胜率: {account_status['win_rate']:.1%}")
        print(f"⏱️ 运行时间: {account_status['running_time']:.0f}秒")
        
        if executed_trades:
            print(f"\n🎯 最新交易:")
            for trade in executed_trades[-3:]:  # 显示最近3笔交易
                action_emoji = "🟢" if trade['action'] == 'BUY' else "🔴"
                print(f"   {action_emoji} {trade['action']} | {trade['type']} | 价格: {trade['price']:.2f}")
        
        print("-" * 60)

# 启动机器人
def start_usdt_trading():
    """启动USDT合约交易"""
    print("🚀 启动虞姬USDT高倍合约量化交易...")
    
    # 10U起步
    bot = USDTContractBot(10.0)
    
    try:
        bot.run_24_7_trading(report_interval=60)  # 每分钟报告一次用于测试
    except KeyboardInterrupt:
        print("\n⏹️ 交易停止")
        final_status = bot.calculate_account_status()
        print(f"📊 最终状态: {final_status}")

if __name__ == "__main__":
    start_usdt_trading()