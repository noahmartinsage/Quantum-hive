import ccxt
import time
import json
from datetime import datetime
from crypto_config import BINANCE_CONFIG

class BinanceTrader:
    def __init__(self):
        self.exchange = ccxt.binance({
            'apiKey': BINANCE_CONFIG['api_key'],
            'secret': BINANCE_CONFIG['api_secret'],
            'sandbox': BINANCE_CONFIG['testnet'],
            'enableRateLimit': True
        })
    
    def get_balance(self):
        """获取账户余额"""
        try:
            balance = self.exchange.fetch_balance()
            return {
                'total': balance['total'],
                'free': balance['free'],
                'used': balance['used']
            }
        except Exception as e:
            return f"获取余额失败: {e}"
    
    def get_ticker(self, symbol='BTC/USDT'):
        """获取交易对价格"""
        try:
            ticker = self.exchange.fetch_ticker(symbol)
            return {
                'symbol': symbol,
                'last': ticker['last'],
                'bid': ticker['bid'],
                'ask': ticker['ask'],
                'volume': ticker['baseVolume']
            }
        except Exception as e:
            return f"获取价格失败: {e}"
    
    def create_order(self, symbol, side, amount, price=None):
        """创建订单"""
        try:
            if price:
                order = self.exchange.create_order(symbol, 'limit', side, amount, price)
            else:
                order = self.exchange.create_order(symbol, 'market', side, amount)
            return order
        except Exception as e:
            return f"创建订单失败: {e}"
    
    def get_open_orders(self, symbol=None):
        """获取未成交订单"""
        try:
            if symbol:
                orders = self.exchange.fetch_open_orders(symbol)
            else:
                orders = self.exchange.fetch_open_orders()
            return orders
        except Exception as e:
            return f"获取订单失败: {e}"

# 使用示例
def test_binance():
    trader = BinanceTrader()
    
    # 获取余额
    print("账户余额:")
    print(trader.get_balance())
    
    # 获取价格
    print("\nBTC价格:")
    print(trader.get_ticker('BTC/USDT'))
    
    # 获取未成交订单
    print("\n未成交订单:")
    print(trader.get_open_orders())

if __name__ == "__main__":
    test_binance()