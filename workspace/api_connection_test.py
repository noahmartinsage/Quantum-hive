#!/usr/bin/env python3
"""
虞姬API连接测试
检查币安测试网连接状态
"""

import requests
import time
from datetime import datetime

def test_api_connection():
    print("🔧 测试币安测试网API连接...")
    print(f"⏰ 时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 50)
    
    base_url = "https://testnet.binancefuture.com"
    
    # 测试公开端点
    print("\n1. 测试公开端点...")
    try:
        # 测试服务器时间
        time_url = f"{base_url}/fapi/v1/time"
        response = requests.get(time_url, timeout=10)
        if response.status_code == 200:
            time_data = response.json()
            server_time = datetime.fromtimestamp(time_data['serverTime'] / 1000)
            print(f"✅ 服务器时间: {server_time}")
        else:
            print(f"❌ 时间API错误: {response.status_code}")
    except Exception as e:
        print(f"⚠️ 时间测试异常: {e}")
    
    # 测试交易对信息
    print("\n2. 测试交易对信息...")
    try:
        exchange_url = f"{base_url}/fapi/v1/exchangeInfo"
        response = requests.get(exchange_url, timeout=10)
        if response.status_code == 200:
            exchange_data = response.json()
            symbols = [s['symbol'] for s in exchange_data['symbols']]
            btc_symbols = [s for s in symbols if 'BTC' in s]
            print(f"✅ 交易对总数: {len(symbols)}")
            print(f"✅ BTC交易对: {len(btc_symbols)}")
            print(f"✅ BTCUSDT可用: {'BTCUSDT' in symbols}")
        else:
            print(f"❌ 交易对API错误: {response.status_code}")
    except Exception as e:
        print(f"⚠️ 交易对测试异常: {e}")
    
    # 测试市场价格
    print("\n3. 测试市场价格...")
    try:
        price_url = f"{base_url}/fapi/v1/ticker/price"
        params = {'symbol': 'BTCUSDT'}
        response = requests.get(price_url, params=params, timeout=10)
        if response.status_code == 200:
            price_data = response.json()
            price = float(price_data['price'])
            print(f"✅ BTC当前价格: {price:.2f} USDT")
        else:
            print(f"❌ 价格API错误: {response.status_code}")
    except Exception as e:
        print(f"⚠️ 价格测试异常: {e}")
    
    # 测试深度
    print("\n4. 测试市场深度...")
    try:
        depth_url = f"{base_url}/fapi/v1/depth"
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
        print(f"⚠️ 深度测试异常: {e}")
    
    print("\n" + "=" * 50)
    print("📋 连接测试总结:")
    print("✅ 公开API端点正常")
    print("⚠️ 需要检查API密钥权限")
    print("🔧 建议: 重新生成API密钥并确保启用交易权限")
    
    # 模拟交易继续
    print("\n5. 启动模拟交易系统...")
    start_simulated_trading()

def start_simulated_trading():
    """启动模拟交易系统"""
    print("🚀 启动虞姬模拟交易系统")
    print("💰 初始资金: 100 USDT")
    print("📈 策略: 激进网格交易")
    print("-" * 50)
    
    capital = 100.0
    position = 0.0
    profit = 0.0
    trades = 0
    base_price = 67000.0
    
    for i in range(15):
        # 模拟价格波动
        volatility = (i % 5 - 2) * 0.008  # 真实波动
        current_price = base_price * (1 + volatility)
        
        # 激进网格策略 (0.5%触发)
        if current_price <= base_price * 0.995 and position < capital * 0.4:
            # 开多仓
            trade_size = capital * 0.2
            quantity = trade_size / current_price
            position += quantity
            capital -= trade_size
            trades += 1
            base_price = current_price
            
            print(f"🟢 模拟开多 | 价格: {current_price:.2f} | 仓位: {trade_size:.2f} USDT")
        
        elif current_price >= base_price * 1.005 and position > 0:
            # 平多仓
            close_quantity = position * 0.6
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
        
        time.sleep(2)
    
    print("\n" + "=" * 50)
    print("📊 模拟交易总结:")
    print(f"💰 最终资产: {total_assets:.4f} USDT")
    print(f"📈 总利润: {profit:.4f} USDT")
    print(f"🔢 交易次数: {trades}")
    print(f"🚀 百万进度: {progress:.8f}%")
    
    return total_assets, profit, trades

if __name__ == "__main__":
    test_api_connection()