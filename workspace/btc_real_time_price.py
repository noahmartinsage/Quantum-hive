#!/usr/bin/env python3
"""
虞姬BTC实时报价系统
使用OKX公开API获取BTC实时价格数据
"""

import requests
import json
from datetime import datetime

class BTCPriceChecker:
    def __init__(self):
        self.base_url = "https://www.okx.com"
        self.session = requests.Session()
        self.session.trust_env = False  # 不信任环境代理
    
    def get_btc_real_time_price(self):
        """获取BTC实时价格"""
        print("🔍 获取BTC实时报价...")
        print("=" * 60)
        
        try:
            # 使用OKX公开API获取BTC-USDT价格
            url = f"{self.base_url}/api/v5/market/ticker?instId=BTC-USDT"
            
            print("\n1. 发送BTC价格查询请求...")
            response = self.session.get(url, timeout=10)
            
            print(f"   HTTP状态码: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('code') == '0':
                    print("   ✅ API请求成功")
                    return self.parse_price_data(data)
                else:
                    error_msg = data.get('msg', '未知错误')
                    print(f"   ❌ API错误: {error_msg}")
                    return None
            else:
                print(f"   ❌ HTTP错误: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"   ❌ 请求异常: {e}")
            return None
    
    def parse_price_data(self, data):
        """解析价格数据"""
        print("\n2. 解析BTC价格数据...")
        
        try:
            ticker_data = data.get('data', [{}])[0]
            
            if not ticker_data:
                print("   ⚠️ 价格数据为空")
                return None
            
            price_info = {
                'symbol': ticker_data.get('instId', ''),
                'last_price': ticker_data.get('last', '0'),
                'open_24h': ticker_data.get('open24h', '0'),
                'high_24h': ticker_data.get('high24h', '0'),
                'low_24h': ticker_data.get('low24h', '0'),
                'volume_24h': ticker_data.get('vol24h', '0'),
                'volume_currency_24h': ticker_data.get('volCcy24h', '0'),
                'timestamp': ticker_data.get('ts', ''),
                'sod_utc0': ticker_data.get('sodUtc0', '0'),
                'sod_utc8': ticker_data.get('sodUtc8', '0')
            }
            
            print("   ✅ 价格数据解析成功")
            return price_info
            
        except Exception as e:
            print(f"   ❌ 数据解析异常: {e}")
            return None
    
    def get_multiple_btc_pairs(self):
        """获取多个BTC交易对价格"""
        print("\n3. 获取多个BTC交易对价格...")
        
        btc_pairs = [
            ("BTC-USDT", "BTC/USDT现货"),
            ("BTC-USDT-SWAP", "BTC/USDT永续合约"),
            ("BTC-USD-SWAP", "BTC/USD永续合约")
        ]
        
        all_prices = {}
        
        for pair, description in btc_pairs:
            try:
                url = f"{self.base_url}/api/v5/market/ticker?instId={pair}"
                response = self.session.get(url, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get('code') == '0':
                        ticker_data = data.get('data', [{}])[0]
                        if ticker_data:
                            all_prices[description] = {
                                'last': ticker_data.get('last', '0'),
                                'change_24h': ticker_data.get('last', '0'),
                                'high_24h': ticker_data.get('high24h', '0'),
                                'low_24h': ticker_data.get('low24h', '0'),
                                'volume_24h': ticker_data.get('vol24h', '0')
                            }
                            print(f"   ✅ {description}: 获取成功")
                        else:
                            print(f"   ❌ {description}: 数据为空")
                    else:
                        print(f"   ❌ {description}: API错误")
                else:
                    print(f"   ❌ {description}: HTTP错误")
                    
            except Exception as e:
                print(f"   ❌ {description}: 请求异常 - {e}")
        
        return all_prices
    
    def generate_price_report(self, price_info, all_prices):
        """生成价格报告"""
        if not price_info:
            print("\n❌ 无法获取BTC价格信息")
            return
        
        print("\n💰 【BTC实时报价报告】")
        print(f"📅 报告时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📡 数据源: OKX交易所")
        print("=" * 70)
        
        # BTC-USDT现货价格
        print("\n📊 【BTC-USDT现货价格】")
        last_price = float(price_info['last_price'])
        open_price = float(price_info['open_24h'])
        
        price_change = last_price - open_price
        price_change_percent = (price_change / open_price) * 100 if open_price > 0 else 0
        
        print(f"   当前价格: {last_price:,.2f} USDT")
        print(f"   24小时开盘: {open_price:,.2f} USDT")
        
        if price_change >= 0:
            print(f"   24小时涨跌: +{price_change:,.2f} USDT (+{price_change_percent:.2f}%)")
        else:
            print(f"   24小时涨跌: {price_change:,.2f} USDT ({price_change_percent:.2f}%)")
        
        print(f"   24小时最高: {float(price_info['high_24h']):,.2f} USDT")
        print(f"   24小时最低: {float(price_info['low_24h']):,.2f} USDT")
        print(f"   24小时成交量: {float(price_info['volume_24h']):.2f} BTC")
        print(f"   24小时成交额: {float(price_info['volume_currency_24h']):,.2f} USDT")
        
        # 时间戳
        if price_info['timestamp']:
            timestamp = datetime.fromtimestamp(int(price_info['timestamp']) / 1000)
            print(f"   数据更新时间: {timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # 多交易对对比
        if all_prices:
            print("\n🔍 【多交易对价格对比】")
            
            for description, price_data in all_prices.items():
                current_price = float(price_data['last'])
                
                if description == "BTC/USDT现货":
                    # 这是基准价格
                    print(f"   📍 {description}: {current_price:,.2f} USDT (基准)")
                else:
                    # 计算与现货的价差
                    spot_price = last_price
                    price_diff = current_price - spot_price
                    price_diff_percent = (price_diff / spot_price) * 100 if spot_price > 0 else 0
                    
                    if price_diff > 0:
                        print(f"   📈 {description}: {current_price:,.2f} USDT (+{price_diff_percent:.3f}%)")
                    else:
                        print(f"   📉 {description}: {current_price:,.2f} USDT ({price_diff_percent:.3f}%)")
        
        # 价格分析
        print("\n💡 【价格分析】")
        
        if price_change_percent > 2:
            print("   🚀 强势上涨趋势")
        elif price_change_percent > 0.5:
            print("   📈 温和上涨")
        elif price_change_percent > -0.5:
            print("   ➡️ 横盘整理")
        elif price_change_percent > -2:
            print("   📉 温和下跌")
        else:
            print("   🔻 显著下跌")
        
        # 交易建议
        print("\n🎯 【交易建议】")
        
        if price_change_percent > 1:
            print("   💡 建议: 考虑趋势跟踪策略")
        elif price_change_percent < -1:
            print("   💡 建议: 考虑均值回归策略")
        else:
            print("   💡 建议: 考虑网格交易策略")
    
    def run_complete_price_check(self):
        """运行完整价格检查"""
        print("🚀 虞姬BTC实时报价系统")
        print(f"⏰ 检查时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)
        
        # 获取BTC-USDT价格
        price_info = self.get_btc_real_time_price()
        
        # 获取多交易对价格
        all_prices = self.get_multiple_btc_pairs()
        
        # 生成报告
        self.generate_price_report(price_info, all_prices)
        
        print("\n" + "=" * 70)
        
        if price_info:
            print("✅ 价格检查完成!")
            
            # 提取价格用于交易决策
            btc_price = float(price_info['last_price'])
            print(f"💰 BTC当前价格: {btc_price:,.2f} USDT")
            print("🚀 可以基于实时价格进行交易决策!")
        else:
            print("⚠️ 价格检查失败")
            print("💡 建议: 检查网络连接或使用备用数据源")

# 立即运行价格检查
def check_btc_price():
    """检查BTC价格"""
    print("🔍 立即获取虞姬BTC实时报价...")
    
    checker = BTCPriceChecker()
    
    try:
        checker.run_complete_price_check()
    except Exception as e:
        print(f"❌ 价格检查异常: {e}")

if __name__ == "__main__":
    check_btc_price()