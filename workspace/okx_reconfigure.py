#!/usr/bin/env python3
"""
虞姬OKX重新配置
使用账号密码重新配置API连接
"""

import time
import hmac
import hashlib
import requests
import json
from datetime import datetime

class OKXReconfigurator:
    def __init__(self):
        # OKX账号信息
        self.username = ""  # 需要账号
        self.password = "Qlzwqc2012."
        
        # API配置（需要重新生成）
        self.api_key = "e4753767-b2f7-4495-b2d9-0166238b1076"
        self.secret = "FBBB847F11CC85396F411B1D52E35A1E"
        self.passphrase = "Abc123456"
        self.base_url = "https://www.okx.com"
    
    def test_current_api(self):
        """测试当前API配置"""
        print("🔧 测试当前API配置...")
        
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
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            print(f"📡 响应状态: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"📊 响应数据: {json.dumps(data, indent=2, ensure_ascii=False)}")
                
                if data.get('code') == '0':
                    print("✅ 当前API配置正常!")
                    return True
                else:
                    print(f"❌ API错误: {data.get('msg')}")
                    return False
            else:
                print(f"❌ HTTP错误: {response.status_code}")
                print(f"❌ 错误详情: {response.text}")
                return False
                
        except Exception as e:
            print(f"⚠️ API测试异常: {e}")
            return False
    
    def check_public_data(self):
        """检查公开数据"""
        print("\n🌐 检查公开市场数据...")
        
        endpoints = [
            ("/api/v5/public/time", "服务器时间"),
            ("/api/v5/public/instruments?instType=SWAP", "交易对信息"),
            ("/api/v5/market/ticker?instId=BTC-USDT-SWAP", "BTC价格")
        ]
        
        for endpoint, description in endpoints:
            try:
                url = f"{self.base_url}{endpoint}"
                response = requests.get(url, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get('code') == '0':
                        print(f"✅ {description}: 正常")
                    else:
                        print(f"❌ {description}: {data.get('msg')}")
                else:
                    print(f"❌ {description}: HTTP {response.status_code}")
                    
            except Exception as e:
                print(f"⚠️ {description}检查异常: {e}")
    
    def generate_new_api_guide(self):
        """生成新API配置指南"""
        print("\n🔑 生成新API配置指南...")
        print("=" * 60)
        print("📋 OKX API重新配置步骤:")
        print("")
        print("1. 登录OKX官网")
        print("   访问: https://www.okx.com")
        print("   使用账号密码登录")
        print("")
        print("2. 进入API管理")
        print("   • 点击右上角用户头像")
        print("   • 选择『API管理』")
        print("   • 点击『创建API』")
        print("")
        print("3. 配置API权限")
        print("   • API名称: 虞姬量化交易")
        print("   • 权限设置: 勾选『交易』权限")
        print("   • 密码: 使用交易密码")
        print("   • IP限制: 建议设置IP白名单")
        print("")
        print("4. 获取新API密钥")
        print("   • 复制API Key")
        print("   • 复制Secret Key")
        print("   • 记住Passphrase")
        print("")
        print("5. 更新配置文件")
        print("   • 替换现有的API配置")
        print("   • 测试新API连接")
        print("=" * 60)
    
    def create_simulation_system(self):
        """创建模拟交易系统"""
        print("\n🚀 创建虞姬高级模拟交易系统...")
        print("💰 初始资金: 200 USDT")
        print("📈 策略: 多策略组合")
        print("-" * 50)
        
        capital = 200.0
        profit = 0.0
        trades = 0
        strategies = ['网格套利', '趋势跟踪', '均值回归']
        
        for i in range(15):
            # 多策略执行
            current_strategy = strategies[i % len(strategies)]
            
            # 模拟价格
            base_price = 67000 + (i % 10 - 5) * 500
            volatility = (i % 7 - 3) * 0.008
            current_price = base_price * (1 + volatility)
            
            # 策略执行
            if current_strategy == '网格套利':
                # 网格策略
                if current_price <= base_price * 0.99 and capital > 40:
                    trade_size = capital * 0.15
                    capital -= trade_size
                    trades += 1
                    print(f"🟢 网格开多 | 价格: {current_price:.2f} | 策略: {current_strategy}")
                elif current_price >= base_price * 1.01 and capital < 160:
                    pnl = 20 * 0.02  # 2%收益
                    profit += pnl
                    capital += 20 + pnl
                    trades += 1
                    print(f"🔴 网格平多 | 价格: {current_price:.2f} | 盈利: {pnl:.4f}")
            
            elif current_strategy == '趋势跟踪':
                # 趋势策略
                if i % 3 == 0 and capital > 50:
                    trade_size = capital * 0.1
                    capital -= trade_size
                    trades += 1
                    print(f"🟡 趋势开仓 | 价格: {current_price:.2f} | 策略: {current_strategy}")
                elif i % 5 == 0 and capital < 150:
                    pnl = 15 * 0.025  # 2.5%收益
                    profit += pnl
                    capital += 15 + pnl
                    trades += 1
                    print(f"🟣 趋势平仓 | 价格: {current_price:.2f} | 盈利: {pnl:.4f}")
            
            else:  # 均值回归
                # 均值回归策略
                if abs(current_price - base_price) / base_price > 0.015 and capital > 30:
                    trade_size = capital * 0.12
                    capital -= trade_size
                    trades += 1
                    print(f"🔵 回归开仓 | 价格: {current_price:.2f} | 策略: {current_strategy}")
                elif abs(current_price - base_price) / base_price < 0.005 and capital < 170:
                    pnl = 18 * 0.018  # 1.8%收益
                    profit += pnl
                    capital += 18 + pnl
                    trades += 1
                    print(f"🟠 回归平仓 | 价格: {current_price:.2f} | 盈利: {pnl:.4f}")
            
            total_assets = capital
            progress = (total_assets / 1000000) * 100
            
            print(f"⏰ 周期{i+1} | 总资产: {total_assets:.4f} USDT | 利润: {profit:.4f} USDT | 进度: {progress:.8f}%")
            
            time.sleep(1.5)
        
        print("\n" + "=" * 50)
        print("📊 高级模拟交易完成:")
        print(f"💰 最终资产: {total_assets:.4f} USDT")
        print(f"📈 总利润: {profit:.4f} USDT")
        print(f"🔢 交易次数: {trades}")
        print(f"🎯 使用策略: {', '.join(strategies)}")
        print(f"🚀 百万进度: {progress:.8f}%")
    
    def run_reconfiguration(self):
        """运行重新配置"""
        print("🚀 虞姬OKX重新配置启动")
        print(f"⏰ 配置时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        # 测试当前API
        api_working = self.test_current_api()
        
        # 检查公开数据
        self.check_public_data()
        
        if not api_working:
            print("\n❌ 当前API配置无效")
            print("🔧 需要重新生成API密钥")
            
            # 生成配置指南
            self.generate_new_api_guide()
            
            # 启动高级模拟系统
            print("\n💡 在修复API期间，启动高级模拟交易系统...")
            self.create_simulation_system()
        else:
            print("\n✅ 当前API配置正常，可以开始交易!")

# 立即运行重新配置
def reconfigure_okx():
    """重新配置OKX"""
    print("🔧 立即重新配置虞姬OKX连接...")
    
    configurator = OKXReconfigurator()
    
    try:
        configurator.run_reconfiguration()
    except KeyboardInterrupt:
        print("\n⏹️ 配置停止")
    except Exception as e:
        print(f"\n❌ 配置异常: {e}")

if __name__ == "__main__":
    reconfigure_okx()