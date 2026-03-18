# 币安和OKX API配置

BINANCE_CONFIG = {
    'api_key': '1a3250b36d5a27ccc0e6a0125d98d1556ff9eacc78baa1fd9ecb1be09056c8f4',  # 币安测试网API Key
    'api_secret': '6de29564a693aad4a969049d5accb6175fcd88be7dc4f2283e598d9a271c8505',  # 币安测试网API Secret
    'testnet': True  # 测试环境，设为False使用实盘
}

OKX_CONFIG = {
    'api_key': 'c774166d-d18e-45b4-acf5-1ceb6bbc438d',  # OKX测试网API Key
    'api_secret': '1838D8DC9DADC01234D483A2A5CD2D87',  # OKX测试网API Secret
    'passphrase': 'Qlzwqc2012',  # OKX测试网Passphrase
    'sandbox': True  # 测试环境，设为False使用实盘
}

# 交易对配置
TRADING_PAIRS = [
    'BTCUSDT',
    'ETHUSDT',
    'BNBUSDT'
]

# 交易参数
TRADING_PARAMS = {
    'amount_per_trade': 0.001,  # 每次交易金额（BTC）
    'stop_loss': 0.02,  # 止损比例
    'take_profit': 0.05,  # 止盈比例
    'leverage': 3  # 杠杆倍数
}