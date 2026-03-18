import ccxt
import time
import json
from datetime import datetime
from crypto_config import OKX_CONFIG

class OKXTrader:
    def __init__(self):
        # 在ccxt 1.40.1中OKX叫okex，需要手动设置测试网URL
        self.exchange = ccxt.okex({
            'apiKey': OKX_CONFIG['api_key'],
            'secret': OKX_CONFIG['api_secret'],
            'password': OKX_CONFIG['passphrase'],
            'sandbox': OKX_CONFIG['sandbox'],
            'enableRateLimit': True
        })
        
        # 手动设置测试网URL
        if OKX_CONFIG['sandbox']:
            self.exchange.urls['api'] = 'https://testnet.okex.com'
    
    def get_balance(self):
        """获取账户余额"""
        try:
            balance = self.exchange.fetch_balance()
            # 检查balance结构
            if isinstance(balance, dict):
                return {
                    'total': balance.get('total', {}),
                    'free': balance.get('free', {}),
                    'used': balance.get('used', {})
                }
            else:
                return f"余额结构异常: {type(balance)}"
        except Exception as e:
            return f"获取余额失败: {e}"
    
    def get_ticker(self, symbol='BTC/USDT'):
        """获取交易对价格"""
        try:
            # 先检查交易所是否支持该交易对
            markets = self.exchange.load_markets()
            if symbol not in markets:
                return f"交易对 {symbol} 不支持"
            
            ticker = self.exchange.fetch_ticker(symbol)
            return {
                'symbol': symbol,
                'last': ticker.get('last', 0),
                'bid': ticker.get('bid', 0),
                'ask': ticker.get('ask', 0),
                'volume': ticker.get('baseVolume', 0)
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
    
    def set_leverage(self, symbol, leverage):
        """设置杠杆"""
        try:
            result = self.exchange.set_leverage(leverage, symbol)
            return result
        except Exception as e:
            return f"设置杠杆失败: {e}"

# 使用示例
def test_okx():
    trader = OKXTrader()
    
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
    test_okx()