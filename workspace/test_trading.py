#!/usr/bin/env python3
"""
测试币安和OKX交易环境
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from binance_trader import BinanceTrader
from okx_trader import OKXTrader
from trading_manager import TradingManager
from crypto_config import BINANCE_CONFIG, OKX_CONFIG

def test_api_connection():
    """测试API连接"""
    print("=== 测试API连接 ===")
    
    # 检查配置
    if not BINANCE_CONFIG['api_key'] or not BINANCE_CONFIG['api_secret']:
        print("⚠️ 币安API密钥未配置，请在 crypto_config.py 中填写")
    else:
        try:
            binance = BinanceTrader()
            print("✓ 币安API连接成功")
        except Exception as e:
            print(f"✗ 币安API连接失败: {e}")
    
    if not OKX_CONFIG['api_key'] or not OKX_CONFIG['api_secret']:
        print("⚠️ OKX API密钥未配置，请在 crypto_config.py 中填写")
    else:
        try:
            okx = OKXTrader()
            print("✓ OKX API连接成功")
        except Exception as e:
            print(f"✗ OKX API连接失败: {e}")

def test_market_data():
    """测试市场数据获取"""
    print("\n=== 测试市场数据 ===")
    
    try:
        manager = TradingManager()
        status = manager.get_market_status()
        
        for pair, prices in status.items():
            print(f"{pair}:")
            if isinstance(prices['binance'], dict):
                print(f"  币安: {prices['binance'].get('last', 'N/A')}")
            else:
                print(f"  币安: {prices['binance']}")
                
            if isinstance(prices['okx'], dict):
                print(f"  OKX: {prices['okx'].get('last', 'N/A')}")
            else:
                print(f"  OKX: {prices['okx']}")
    except Exception as e:
        print(f"市场数据获取失败: {e}")

def test_arbitrage():
    """测试套利检测"""
    print("\n=== 测试套利检测 ===")
    
    try:
        manager = TradingManager()
        opportunities = manager.arbitrage_opportunity()
        
        if opportunities:
            for opp in opportunities:
                print(f"套利机会: {opp['pair']} - {opp['spread']:.4%} - {opp['direction']}")
        else:
            print("暂无套利机会")
    except Exception as e:
        print(f"套利检测失败: {e}")

def main():
    print("🚀 币安和OKX交易环境测试")
    print("=" * 50)
    
    test_api_connection()
    test_market_data()
    test_arbitrage()
    
    print("\n" + "=" * 50)
    print("✅ 测试完成")
    print("\n下一步:")
    print("1. 编辑 crypto_config.py 填写API密钥")
    print("2. 运行测试确保连接正常")
    print("3. 开始交易！")

if __name__ == "__main__":
    main()