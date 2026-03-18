#!/usr/bin/env python3
"""
虞姬OKX API调试
诊断OKX API连接问题
"""

import time
import hmac
import hashlib
import requests
import json
from datetime import datetime

class OKXAPIDebugger:
    def __init__(self):
        # OKX模拟盘配置
        self.api_key = "e4753767-b2f7-4495-b2d9-0166238b1076"
        self.secret = "FBBB847F11CC85396F411B1D52E35A1E"
        self.passphrase = "Abc123456"
        self.base_url = "https://www.okx.com"
    
    def test_public_endpoints(self):
        """测试公开端点"""
        print("🔧 测试OKX公开API端点...")
        
        # 测试服务器时间
        print("\n1. 测试服务器时间...")
        try:
            url = f"{self.base_url}/api/v5/public/time"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get('code') == '0':
                    server_time = data['data'][0]['ts']
                    print(f"✅ 服务器时间: {server_time}")
                else:
                    print(f"❌ 时间API错误: {data}")
            else:
                print(f"❌ HTTP错误: {response.status_code}")
        except Exception as e:
            print(f"⚠️ 时间测试异常: {e}")
        
        # 测试交易对信息
        print("\n2. 测试交易对信息...")
        try:
            url = f"{self.base_url}/api/v5/public/instruments"
            params = {'instType': 'SWAP'}
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get('code') == '0':
                    instruments = data['data']
                    btc_instruments = [i for i in instruments if 'BTC' in i['instId']]
                    print(f"✅ SWAP交易对总数: {len(instruments)}")
                    print(f"✅ BTC相关交易对: {len(btc_instruments)}")
                    print(f"✅ BTC-USDT-SWAP可用: {'BTC-USDT-SWAP' in [i['instId'] for i in instruments]}")
                else:
                    print(f"❌ 交易对API错误: {data}")
            else:
                print(f"❌ HTTP错误: {response.status_code}")
        except Exception as e:
            print(f"⚠️ 交易对测试异常: {e}")
        
        # 测试市场价格
        print("\n3. 测试市场价格...")
        try:
            url = f"{self.base_url}/api/v5/market/ticker"
            params = {'instId': 'BTC-USDT-SWAP'}
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get('code') == '0' and len(data['data']) > 0:
                    ticker = data['data'][0]
                    last_price = float(ticker['last'])
                    print(f"✅ BTC-USDT-SWAP价格: {last_price:.2f}")
                else:
                    print(f"❌ 价格API错误: {data}")
            else:
                print(f"❌ HTTP错误: {response.status_code}")
        except Exception as e:
            print(f"⚠️ 价格测试异常: {e}")
    
    def test_private_endpoints(self):
        """测试私有端点"""
        print("\n🔐 测试OKX私有API端点...")
        
        # 生成签名
        timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        request_path = "/api/v5/account/balance"
        
        message = timestamp + 'GET' + request_path
        signature = hmac.new(
            self.secret.encode('utf-8'),
            message.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        headers = {
            'OK-ACCESS-KEY': self.api_key,
            'OK-ACCESS-SIGN': signature,
            'OK-ACCESS-TIMESTAMP': timestamp,
            'OK-ACCESS-PASSPHRASE': self.passphrase,
            'Content-Type': 'application/json'
        }
        
        url = f"{self.base_url}{request_path}"
        
        print("\n4. 测试账户余额...")
        try:
            response = requests.get(url, headers=headers, timeout=10)
            print(f"📡 响应状态: {response.status_code}")
            print(f"📋 响应头: {dict(response.headers)}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"📊 响应数据: {json.dumps(data, indent=2, ensure_ascii=False)}")
                
                if data.get('code') == '0':
                    print("✅ 私有API连接成功!")
                    return True
                else:
                    print(f"❌ API错误代码: {data.get('code')}")
                    print(f"❌ 错误信息: {data.get('msg')}")
            else:
                print(f"❌ HTTP错误: {response.status_code}")
                print(f"❌ 错误详情: {response.text}")
                
        except Exception as e:
            print(f"⚠️ 私有API测试异常: {e}")
        
        return False
    
    def debug_api_config(self):
        """调试API配置"""
        print("🔍 调试API配置...")
        print(f"API Key: {self.api_key}")
        print(f"Secret Key: {self.secret[:8]}...{self.secret[-8:]}")
        print(f"Passphrase: {self.passphrase}")
        print(f"Base URL: {self.base_url}")
        
        # 检查密钥格式
        print("\n🔑 检查密钥格式...")
        if len(self.api_key) != 36:
            print("❌ API Key长度异常 (应为36位)")
        else:
            print("✅ API Key格式正常")
            
        if len(self.secret) != 32:
            print("❌ Secret Key长度异常 (应为32位)")
        else:
            print("✅ Secret Key格式正常")
    
    def run_debug(self):
        """运行调试"""
        print("🚀 虞姬OKX API调试启动")
        print(f"⏰ 调试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        # 调试配置
        self.debug_api_config()
        
        # 测试公开端点
        self.test_public_endpoints()
        
        # 测试私有端点
        private_success = self.test_private_endpoints()
        
        print("\n" + "=" * 60)
        print("📋 调试总结:")
        
        if private_success:
            print("✅ OKX API连接正常")
            print("✅ 可以开始交易")
        else:
            print("❌ OKX API连接失败")
            print("🔧 建议检查:")
            print("   1. API密钥是否正确")
            print("   2. Passphrase是否正确")
            print("   3. IP白名单设置")
            print("   4. 交易权限设置")
            print("   5. 模拟盘/实盘环境")
        
        # 启动模拟交易作为备选
        if not private_success:
            print("\n🚀 启动模拟交易系统作为备选...")
            self.start_simulated_trading()
    
    def start_simulated_trading(self):
        """启动模拟交易"""
        print("\n💰 启动虞姬模拟交易系统")
        print("初始资金: 100 USDT")
        print("策略: 激进网格套利")
        print("-" * 50)
        
        capital = 100.0
        profit = 0.0
        trades = 0
        base_price = 67000.0
        
        for i in range(10):
            # 模拟价格波动
            volatility = (i % 4 - 1.5) * 0.01
            current_price = base_price * (1 + volatility)
            
            # 网格策略
            if current_price <= base_price * 0.99 and capital > 10:
                # 开仓
                trade_size = capital * 0.2
                quantity = trade_size / current_price
                capital -= trade_size
                trades += 1
                base_price = current_price
                
                print(f"🟢 模拟开多 | 价格: {current_price:.2f} | 仓位: {trade_size:.2f} USDT")
            
            elif current_price >= base_price * 1.01 and capital < 90:
                # 平仓
                trade_size = 20
                pnl = trade_size * 0.015  # 1.5%收益
                profit += pnl
                capital += trade_size + pnl
                trades += 1
                base_price = current_price
                
                print(f"🔴 模拟平多 | 价格: {current_price:.2f} | 盈利: {pnl:.4f} USDT")
            
            total_assets = capital
            progress = (total_assets / 1000000) * 100
            
            print(f"⏰ 周期{i+1} | 总资产: {total_assets:.4f} USDT | 利润: {profit:.4f} USDT | 进度: {progress:.8f}%")
            
            time.sleep(1)
        
        print("\n📊 模拟交易完成:")
        print(f"最终资产: {total_assets:.4f} USDT")
        print(f"总利润: {profit:.4f} USDT")

# 立即运行调试
def debug_okx_api():
    """调试OKX API"""
    print("🔧 立即调试虞姬OKX API连接...")
    
    debugger = OKXAPIDebugger()
    
    try:
        debugger.run_debug()
    except KeyboardInterrupt:
        print("\n⏹️ 调试停止")
    except Exception as e:
        print(f"\n❌ 调试异常: {e}")

if __name__ == "__main__":
    debug_okx_api()