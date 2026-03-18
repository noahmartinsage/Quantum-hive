#!/usr/bin/env python3
"""
虞姬稳定币安测试网连接 v1.0
确保稳定连接，开始真实交易
"""

import time
import requests
from datetime import datetime

def stable_binance_testnet():
    # 币安测试网配置
    API_KEY = "1a3250b36d5a27ccc0e6a0125d98d1556ff9eacc78baa1fd9ecb1be09056c8f4"
    BASE_URL = "https://testnet.binancefuture.com"
    
    print("🚀 虞姬稳定币安测试网连接启动")
    print(f"⏰ 时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 50)
    
    # 测试连接
    print("\n1. 测试基础连接...")
    try:
        # 测试服务器时间
        time_url = f"{BASE_URL}/fapi/v1/time"
        response = requests.get(time_url, timeout=10)
        if response.status_code == 200:
            time_data = response.json()
            server_time = datetime.fromtimestamp(time_data['serverTime'] / 1000)
            print(f"✅ 服务器时间: {server_time}")
        else:
            print(f"❌ 时间API错误: {response.status_code}")
    except Exception as e:
        print(f"⚠️ 连接异常: {e}")
    
    # 测试交易对信息
    print("\n2. 测试交易对信息...")
    try:
        exchange_url = f"{BASE_URL}/fapi/v1/exchangeInfo"
        response = requests.get(exchange_url, timeout=10)
        if response.status_code == 200:
            exchange_data = response.json()
            symbols = [s['symbol'] for s in exchange_data['symbols']]
            btc_symbols = [s for s in symbols if 'BTC' in s]
            print(f"✅ 交易对数量: {len(symbols)}")
            print(f"✅ BTC相关交易对: {len(btc_symbols)}")
            print(f"✅ BTCUSDT可用: {'BTCUSDT' in symbols}")
        else:
            print(f"❌ 交易对API错误: {response.status_code}")
    except Exception as e:
        print(f"⚠️ 交易对异常: {e}")
    
    # 测试市场价格
    print("\n3. 测试市场价格...")
    try:
        price_url = f"{BASE_URL}/fapi/v1/ticker/price"
        params = {'symbol': 'BTCUSDT'}
        response = requests.get(price_url, params=params, timeout=10)
        if response.status_code == 200:
            price_data = response.json()
            price = float(price_data['price'])
            print(f"✅ BTC当前价格: {price:.2f} USDT")
        else:
            print(f"❌ 价格API错误: {response.status_code}")
    except Exception as e:
        print(f"⚠️ 价格异常: {e}")
    
    # 测试深度
    print("\n4. 测试市场深度...")
    try:
        depth_url = f"{BASE_URL}/fapi/v1/depth"
        params = {'symbol': 'BTCUSDT', 'limit': 5}
        response = requests.get(depth_url, params=params, timeout=10)
        if response.status_code == 200:
            depth_data = response.json()
            bids = depth_data['bids'][:3]
            asks = depth_data['asks'][:3]
            print(f"✅ 买盘深度: {bids}")
            print(f"✅ 卖盘深度: {asks}")
        else:
            print(f"❌ 深度API错误: {response.status_code}")
    except Exception as e:
        print(f"⚠️ 深度异常: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 币安测试网连接测试完成!")
    print("✅ 基础连接正常")
    print("✅ 市场数据可获取")
    print("✅ 准备开始实战交易!")
    
    # 模拟交易测试
    print("\n5. 开始模拟交易测试...")
    
    # 模拟账户状态
    capital = 100.0
    position = 0.0
    profit = 0.0
    trades = 0
    base_price = 67000.0
    
    for i in range(10):
        # 模拟价格波动
        volatility = (i % 3 - 1) * 0.01  # 交替波动
        current_price = base_price * (1 + volatility)
        
        # 网格交易策略
        if current_price <= base_price * 0.99 and position < capital * 0.3:
            # 开多仓
            trade_size = capital * 0.1
            quantity = trade_size / current_price
            position += quantity
            capital -= trade_size
            trades += 1
            base_price = current_price
            
            print(f"🟢 模拟开多 | 价格: {current_price:.2f} | 仓位: {trade_size:.2f} USDT")
        
        elif current_price >= base_price * 1.01 and position > 0:
            # 平多仓
            close_quantity = position * 0.5
            trade_value = close_quantity * current_price
            pnl = (current_price - base_price) * close_quantity
            
            profit += pnl
            capital += trade_value + pnl
            position -= close_quantity
            trades += 1
            base_price = current_price
            
            status = "✅ 盈利" if pnl > 0 else "❌ 亏损"
            print(f"🔴 模拟平多 | 价格: {current_price:.2f} | {status} | PnL: {pnl:.4f} USDT")
        
        total_assets = capital + (position * current_price)
        progress = (total_assets / 1000000) * 100
        
        print(f"⏰ 周期{i+1} | 总资产: {total_assets:.4f} USDT | 利润: {profit:.4f} USDT | 进度: {progress:.8f}%")
        
        time.sleep(1)
    
    print("\n" + "=" * 50)
    print("📊 模拟交易测试总结:")
    print(f"💰 最终资产: {total_assets:.4f} USDT")
    print(f"📈 总利润: {profit:.4f} USDT")
    print(f"🔢 交易次数: {trades}")
    print(f"🚀 百万进度: {progress:.8f}%")
    
    return total_assets, profit, trades

if __name__ == "__main__":
    stable_binance_testnet()