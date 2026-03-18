#!/usr/bin/env python3
"""
交易监控心跳脚本
定期检查币安测试网状态和交易机会
"""

import sys
import os
import json
from datetime import datetime

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from binance_trader import BinanceTrader
from trading_manager import TradingManager
from crypto_config import TRADING_PAIRS

def check_binance_status():
    """检查币安测试网状态"""
    try:
        binance = BinanceTrader()
        
        # 获取余额
        balance = binance.get_balance()
        
        # 获取价格
        prices = {}
        for pair in TRADING_PAIRS:
            symbol = f"{pair[:-4]}/{pair[-4:]}"
            ticker = binance.get_ticker(symbol)
            if isinstance(ticker, dict):
                prices[pair] = ticker.get('last', 0)
        
        # 获取未成交订单
        orders = binance.get_open_orders()
        
        return {
            'status': 'connected',
            'balance': balance,
            'prices': prices,
            'open_orders': len(orders) if isinstance(orders, list) else 0,
            'timestamp': datetime.now().isoformat()
        }
    except Exception as e:
        return {
            'status': 'error',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }

def check_trading_opportunities():
    """检查交易机会"""
    try:
        manager = TradingManager()
        
        # 检测套利机会
        arbitrage_opps = manager.arbitrage_opportunity()
        
        # 执行简单策略
        strategy_results = {}
        for pair in TRADING_PAIRS:
            symbol = f"{pair[:-4]}/{pair[-4:]}"
            result = manager.simple_strategy(symbol)
            strategy_results[pair] = result
        
        return {
            'arbitrage_opportunities': len(arbitrage_opps),
            'strategy_results': strategy_results,
            'timestamp': datetime.now().isoformat()
        }
    except Exception as e:
        return {
            'status': 'error',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }

def save_heartbeat_log(status_data, opportunity_data):
    """保存心跳日志"""
    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'binance_status': status_data,
        'trading_opportunities': opportunity_data
    }
    
    # 读取现有日志
    try:
        with open('/root/.openclaw/workspace/heartbeat_log.json', 'r') as f:
            logs = json.load(f)
    except FileNotFoundError:
        logs = []
    
    # 添加新日志（保留最近100条）
    logs.append(log_entry)
    if len(logs) > 100:
        logs = logs[-100:]
    
    # 保存日志
    with open('/root/.openclaw/workspace/heartbeat_log.json', 'w') as f:
        json.dump(logs, f, indent=2)

def main():
    """主监控函数"""
    print("🔔 交易监控心跳检查")
    print("=" * 50)
    
    # 检查币安状态
    print("检查币安测试网状态...")
    binance_status = check_binance_status()
    
    if binance_status['status'] == 'connected':
        print("✓ 币安测试网连接正常")
        print(f"  余额: {binance_status['balance']}")
        print(f"  价格: {binance_status['prices']}")
        print(f"  未成交订单: {binance_status['open_orders']}")
    else:
        print(f"✗ 币安连接异常: {binance_status['error']}")
    
    # 检查交易机会
    print("\n检查交易机会...")
    opportunities = check_trading_opportunities()
    
    if opportunities.get('status') == 'error':
        print(f"✗ 机会检测异常: {opportunities['error']}")
    else:
        print(f"✓ 套利机会数量: {opportunities['arbitrage_opportunities']}")
        for pair, result in opportunities['strategy_results'].items():
            if isinstance(result, dict):
                print(f"  {pair}: {result.get('action', 'No Signal')}")
    
    # 保存日志
    save_heartbeat_log(binance_status, opportunities)
    
    print(f"\n✅ 心跳检查完成 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()