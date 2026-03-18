# 币安和OKX交易环境设置指南

## 第一步：获取API密钥

### 币安API密钥
1. 登录币安官网 (https://www.binance.com)
2. 进入"API管理"页面
3. 创建新的API密钥
4. 设置API权限（建议只开启交易和查询权限）
5. 复制API Key和Secret Key

### OKX API密钥
1. 登录OKX官网 (https://www.okx.com)
2. 进入"API管理"页面
3. 创建新的API密钥
4. 设置API权限（建议只开启交易和查询权限）
5. 复制API Key、Secret Key和Passphrase

## 第二步：配置API密钥

编辑 `crypto_config.py` 文件：

```python
# 币安配置
BINANCE_CONFIG = {
    'api_key': '你的币安API Key',
    'api_secret': '你的币安API Secret',
    'testnet': True  # 先在测试环境运行，设为False使用实盘
}

# OKX配置
OKX_CONFIG = {
    'api_key': '你的OKX API Key',
    'api_secret': '你的OKX API Secret',
    'passphrase': '你的OKX Passphrase',
    'sandbox': True  # 先在测试环境运行，设为False使用实盘
}
```

## 第三步：测试连接

运行测试脚本：
```bash
python3 test_trading.py
```

如果一切正常，你将看到：
- ✓ 币安API连接成功
- ✓ OKX API连接成功
- 各交易对的最新价格
- 套利机会检测

## 第四步：开始交易

### 基本交易功能
```python
from trading_manager import TradingManager

manager = TradingManager()

# 获取账户余额
balance = manager.binance.get_balance()
print("币安余额:", balance)

# 获取价格
ticker = manager.binance.get_ticker('BTC/USDT')
print("BTC价格:", ticker)

# 创建订单
order = manager.binance.create_order('BTC/USDT', 'buy', 0.001)
print("订单创建:", order)
```

### 套利交易
```python
# 检测套利机会
opportunities = manager.arbitrage_opportunity()

for opp in opportunities:
    print(f"套利机会: {opp['pair']} - {opp['spread']:.4%}")
    
    if opp['direction'] == 'buy_okx_sell_binance':
        # 在OKX买入，在币安卖出
        okx_order = manager.okx.create_order(opp['pair'], 'buy', 0.001)
        binance_order = manager.binance.create_order(opp['pair'], 'sell', 0.001)
```

## 安全注意事项

### API密钥安全
- 不要将API密钥上传到GitHub等公开平台
- 定期轮换API密钥
- 仅授予必要的API权限

### 交易安全
- 先在测试环境验证所有功能
- 从小额交易开始
- 设置止损止盈
- 定期监控交易表现

### 风险管理
- 不要投入超过承受能力的资金
- 分散投资
- 了解交易策略的风险

## 故障排除

### 常见问题
1. **API连接失败**
   - 检查API密钥是否正确
   - 检查网络连接
   - 检查API权限设置

2. **交易失败**
   - 检查账户余额
   - 检查最小交易量
   - 检查交易对是否支持

3. **价格获取失败**
   - 检查交易对名称
   - 检查交易所是否支持该交易对

### 调试方法
```python
# 检查API连接
try:
    trader = BinanceTrader()
    print("币安连接成功")
except Exception as e:
    print(f"币安连接失败: {e}")

# 检查价格获取
try:
    ticker = trader.get_ticker('BTC/USDT')
    print("价格获取成功:", ticker)
except Exception as e:
    print(f"价格获取失败: {e}")
```

## 进阶配置

### 自定义交易策略
编辑 `trading_manager.py` 中的 `simple_strategy` 方法，实现你自己的交易逻辑。

### 添加更多交易对
在 `crypto_config.py` 的 `TRADING_PAIRS` 列表中添加更多交易对。

### 调整交易参数
在 `crypto_config.py` 的 `TRADING_PARAMS` 中调整交易金额、止损止盈比例等参数。

## 技术支持

如果遇到问题，可以：
1. 查看ccxt文档：https://docs.ccxt.com/
2. 查看币安API文档：https://binance-docs.github.io/apidocs/
3. 查看OKX API文档：https://www.okx.com/docs/

祝交易顺利！🎯