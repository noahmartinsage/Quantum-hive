import json
import time
from datetime import datetime
from binance_trader import BinanceTrader
from okx_trader import OKXTrader
from crypto_config import TRADING_PAIRS, TRADING_PARAMS

class TradingManager:
    def __init__(self):
        self.binance = BinanceTrader()
        self.okx = OKXTrader()
        self.trading_log = []
    
    def get_market_status(self):
        """获取市场状态"""
        status = {}
        
        for pair in TRADING_PAIRS:
            symbol = f"{pair[:-4]}/{pair[-4:]}"  # 转换为CCXT格式
            
            # 币安价格
            binance_price = self.binance.get_ticker(symbol)
            # OKX价格
            okx_price = self.okx.get_ticker(symbol)
            
            status[pair] = {
                'binance': binance_price,
                'okx': okx_price
            }
        
        return status
    
    def arbitrage_opportunity(self):
        """检测套利机会"""
        status = self.get_market_status()
        opportunities = []
        
        for pair, prices in status.items():
            if isinstance(prices['binance'], dict) and isinstance(prices['okx'], dict):
                binance_price = prices['binance'].get('last', 0)
                okx_price = prices['okx'].get('last', 0)
                
                if binance_price > 0 and okx_price > 0:
                    spread = abs(binance_price - okx_price) / min(binance_price, okx_price)
                    
                    if spread > 0.001:  # 0.1% 差价
                        opportunities.append({
                            'pair': pair,
                            'binance_price': binance_price,
                            'okx_price': okx_price,
                            'spread': spread,
                            'direction': 'buy_okx_sell_binance' if okx_price < binance_price else 'buy_binance_sell_okx'
                        })
        
        return opportunities
    
    def simple_strategy(self, pair='BTC/USDT'):
        """简单交易策略"""
        try:
            # 获取价格
            price = self.binance.get_ticker(pair)
            if isinstance(price, dict):
                current_price = price['last']
                
                # 简单策略：价格低于某个阈值时买入
                # 这里只是一个示例，实际策略需要更复杂的逻辑
                if current_price < 40000:  # 示例阈值
                    # 买入
                    amount = TRADING_PARAMS['amount_per_trade']
                    order = self.binance.create_order(pair, 'buy', amount)
                    
                    log_entry = {
                        'timestamp': datetime.now().isoformat(),
                        'action': 'BUY',
                        'pair': pair,
                        'price': current_price,
                        'amount': amount,
                        'order_id': order.get('id') if isinstance(order, dict) else 'N/A'
                    }
                    self.trading_log.append(log_entry)
                    return log_entry
                
                elif current_price > 45000:  # 示例阈值
                    # 卖出
                    amount = TRADING_PARAMS['amount_per_trade']
                    order = self.binance.create_order(pair, 'sell', amount)
                    
                    log_entry = {
                        'timestamp': datetime.now().isoformat(),
                        'action': 'SELL',
                        'pair': pair,
                        'price': current_price,
                        'amount': amount,
                        'order_id': order.get('id') if isinstance(order, dict) else 'N/A'
                    }
                    self.trading_log.append(log_entry)
                    return log_entry
            
            return "没有交易信号"
        except Exception as e:
            return f"策略执行失败: {e}"
    
    def save_log(self):
        """保存交易日志"""
        with open('/root/.openclaw/workspace/trading_log.json', 'w') as f:
            json.dump(self.trading_log, f, indent=2)
    
    def load_log(self):
        """加载交易日志"""
        try:
            with open('/root/.openclaw/workspace/trading_log.json', 'r') as f:
                self.trading_log = json.load(f)
        except FileNotFoundError:
            self.trading_log = []

def main():
    manager = TradingManager()
    
    print("=== 市场状态 ===")
    status = manager.get_market_status()
    for pair, prices in status.items():
        print(f"{pair}:")
        print(f"  币安: {prices['binance']}")
        print(f"  OKX: {prices['okx']}")
    
    print("\n=== 套利机会 ===")
    opportunities = manager.arbitrage_opportunity()
    for opp in opportunities:
        print(f"{opp['pair']}: {opp['spread']:.4%} - {opp['direction']}")
    
    print("\n=== 账户余额 ===")
    print("币安:", manager.binance.get_balance())
    print("OKX:", manager.okx.get_balance())

if __name__ == "__main__":
    main()