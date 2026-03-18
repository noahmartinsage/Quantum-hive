# 币安和OKX交易指南

## 快速开始

### 1. 配置API密钥
编辑 `crypto_config.py` 文件，填入你的API密钥：

```python
# 币安配置
BINANCE_CONFIG = {
    'api_key': '你的币安API Key',
    'api_secret': '你的币安API Secret',
    'testnet': True  # 测试环境，设为False使用实盘
}

# OKX配置
OKX_CONFIG = {
    'api_key': '你的OKX API Key',
    'api_secret': '你的OKX API Secret',
    'passphrase': '你的OKX Passphrase',
    'sandbox': True  # 测试环境，设为False使用实盘
}
```

### 2. 测试连接
运行测试脚本来验证API连接：

```bash
python3 test_trading.py
```

### 3. 开始交易
使用交易管理器：

```python
from trading_manager import TradingManager

manager = TradingManager()

# 获取市场状态
status = manager.get_market_status()

# 检测套利机会
opportunities = manager.arbitrage_opportunity()

# 执行简单策略
trade_result = manager.simple_strategy('BTC/USDT')
```

## 可用功能

### 币安交易器 (binance_trader.py)
- 获取账户余额
- 获取交易对价格
- 创建订单（市价/限价）
- 获取未成交订单

### OKX交易器 (okx_trader.py)
- 获取账户余额
- 获取交易对价格
- 创建订单（市价/限价）
- 设置杠杆
- 获取未成交订单

### 交易管理器 (trading_manager.py)
- 市场状态监控
- 套利机会检测
- 简单交易策略
- 交易日志记录

## 交易策略

### 套利策略
检测币安和OKX之间的价格差异，当差价超过0.1%时进行套利交易。

### 简单策略
- 价格低于40,000时买入BTC
- 价格高于45,000时卖出BTC
- 可根据市场情况调整阈值

## 安全建议

1. **测试环境优先**：先在测试环境验证所有功能
2. **小额测试**：使用小额资金进行测试交易
3. **API权限**：仅授予必要的API权限
4. **定期备份**：备份API密钥和配置文件
5. **监控日志**：定期检查交易日志

## 故障排除

### 常见问题
1. **API连接失败**：检查API密钥和网络连接
2. **权限不足**：检查API权限设置
3. **版本兼容**：确保ccxt版本兼容
4. **测试环境**：确认使用正确的测试环境

### 调试方法
```python
# 检查API连接
trader = BinanceTrader()
print(trader.get_balance())
print(trader.get_ticker('BTC/USDT'))
```

## 进阶功能

- 多交易所价格聚合
- 自动套利交易
- 风险管理
- 策略回测
- 实时监控

## 注意事项

⚠️ **风险提示**：加密货币交易存在高风险，请谨慎操作。

- 不要投入超过承受能力的资金
- 充分理解交易策略的风险
- 定期监控交易表现
- 设置止损止盈
- 分散投资降低风险