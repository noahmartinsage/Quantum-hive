#!/usr/bin/env python3
"""
币安和OKX交易演示
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from binance_trader import BinanceTrader
from okx_trader import OKXTrader
from trading_manager import TradingManager
from crypto_config import BINANCE_CONFIG, OKX_CONFIG

def demo_basic_functions():
    """演示基本功能"""
    print("=== 基本功能演示 ===")
    
    # 创建交易器实例
    if BINANCE_CONFIG['api_key'] and BINANCE_CONFIG['api_secret']:
        binance = BinanceTrader()
        print("✓ 币安交易器创建成功")
        
        # 获取余额
        balance = binance.get_balance()
        print(f"币安余额: {balance}")
        
        # 获取价格
        btc_price = binance.get_ticker('BTC/USDT')
        print(f"BTC价格: {btc_price}")
    else:
        print("⚠️ 币安API密钥未配置")
    
    if OKX_CONFIG['api_key'] and OKX_CONFIG['api_secret']:
        okx = OKXTrader()
        print("✓ OKX交易器创建成功")
        
        # 获取余额
        balance = okx.get_balance()
        print(f"OKX余额: {balance}")
        
        # 获取价格
        btc_price = okx.get_ticker('BTC/USDT')
        print(f"BTC价格: {btc_price}")
    else:
        print("⚠️ OKX API密钥未配置")

def demo_market_monitoring():
    """演示市场监控"""
    print("\n=== 市场监控演示 ===")
    
    manager = TradingManager()
    
    # 获取市场状态
    status = manager.get_market_status()
    print("市场状态:")
    for pair, prices in status.items():
        print(f"{pair}:")
        if isinstance(prices['binance'], dict):
            print(f"  币安: {prices['binance'].get('last', 'N/A')}")
        if isinstance(prices['okx'], dict):
            print(f"  OKX: {prices['okx'].get('last', 'N/A')}")

def demo_arbitrage():
    """演示套利检测"""
    print("\n=== 套利检测演示 ===")
    
    manager = TradingManager()
    
    # 检测套利机会
    opportunities = manager.arbitrage_opportunity()
    
    if opportunities:
        print("发现套利机会:")
        for opp in opportunities:
            print(f"  {opp['pair']}:")
            print(f"    币安价格: {opp['binance_price']}")
            print(f"    OKX价格: {opp['okx_price']}")
            print(f"    差价: {opp['spread']:.4%}")
            print(f"    方向: {opp['direction']}")
            print()
    else:
        print("暂无套利机会")

def demo_trading_strategy():
    """演示交易策略"""
    print("\n=== 交易策略演示 ===")
    
    manager = TradingManager()
    
    # 执行简单策略
    result = manager.simple_strategy('BTC/USDT')
    print(f"策略执行结果: {result}")

def main():
    print("🎯 币安和OKX交易演示")
    print("=" * 50)
    
    demo_basic_functions()
    demo_market_monitoring()
    demo_arbitrage()
    demo_trading_strategy()
    
    print("\n" + "=" * 50)
    print("✅ 演示完成")
    print("\n要开始实际交易，请:")
    print("1. 编辑 crypto_config.py 填写API密钥")
    print("2. 将 testnet/sandbox 设为 False")
    print("3. 运行 python3 demo_trading.py")

if __name__ == "__main__":
    main()