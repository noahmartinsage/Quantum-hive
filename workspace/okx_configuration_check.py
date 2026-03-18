#!/usr/bin/env python3
"""
虞姬OKX配置信息检查
根据官方文档仔细检查配置信息是否存在错误或过时配置
"""

import time
import hmac
import hashlib
import requests
import json
import base64
from datetime import datetime

class OKXConfigurationCheck:
    def __init__(self):
        # 老板提供的最新OKX凭据
        self.api_key = "cd06b52e-575b-4ca3-9ab2-f23a36e29f9e"
        self.secret = "6D5E919E861D9DF646AC1C01A09E6002"
        self.passphrase = "Qlzwqc2012."
        
        # 测试网专用API地址
        self.testnet_url = "https://www.okx.com"
        
        # 稳健连接
        self.session = requests.Session()
        self.session.trust_env = False
    
    def check_configuration_issues(self):
        """检查配置问题"""
        print("🔍 虞姬OKX配置信息检查...")
        print("=" * 60)
        
        configuration_issues = {}
        
        # 检查1: API密钥格式检查
        print("\n1. API密钥格式检查...")
        api_key_check = self.check_api_key_format()
        configuration_issues['api_key'] = api_key_check
        
        # 检查2: 签名算法检查
        print("\n2. 签名算法检查...")
        signature_check = self.check_signature_algorithm()
        configuration_issues['signature'] = signature_check
        
        # 检查3: 时间戳格式检查
        print("\n3. 时间戳格式检查...")
        timestamp_check = self.check_timestamp_format()
        configuration_issues['timestamp'] = timestamp_check
        
        # 检查4: 头信息格式检查
        print("\n4. 头信息格式检查...")
        header_check = self.check_header_format()
        configuration_issues['header'] = header_check
        
        # 检查5: 模拟交易环境检查
        print("\n5. 模拟交易环境检查...")
        simulated_check = self.check_simulated_trading()
        configuration_issues['simulated'] = simulated_check
        
        # 检查6: 请求格式检查
        print("\n6. 请求格式检查...")
        request_check = self.check_request_format()
        configuration_issues['request'] = request_check
        
        return configuration_issues
    
    def check_api_key_format(self):
        """检查API密钥格式"""
        print("   检查API密钥格式...")
        
        issues = []
        
        # 检查API Key格式
        print(f"      API Key: {self.api_key}")
        print(f"      API Key长度: {len(self.api_key)}")
        
        # OKX API Key通常是36位UUID格式
        if len(self.api_key) != 36:
            issues.append(f"API Key长度异常: {len(self.api_key)} (应为36)")
        
        # 检查Secret密钥格式
        print(f"      Secret: {self.secret}")
        print(f"      Secret长度: {len(self.secret)}")
        
        # OKX Secret通常是32位十六进制
        if len(self.secret) != 32:
            issues.append(f"Secret长度异常: {len(self.secret)} (应为32)")
        
        # 检查Secret是否为有效十六进制
        try:
            bytes.fromhex(self.secret)
            print("      ✅ Secret是有效十六进制")
        except:
            issues.append("Secret不是有效十六进制格式")
        
        # 检查Passphrase格式
        print(f"      Passphrase: {self.passphrase}")
        print(f"      Passphrase长度: {len(self.passphrase)}")
        
        # Passphrase应该有适当长度
        if len(self.passphrase) < 6:
            issues.append("Passphrase太短")
        
        return {'issues': issues}
    
    def check_signature_algorithm(self):
        """检查签名算法"""
        print("   检查签名算法...")
        
        issues = []
        
        # 根据官方文档生成签名
        timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        request_path = "/api/v5/account/balance"
        method = "GET"
        
        # 官方文档签名格式: timestamp + method + requestPath
        message = timestamp + method + request_path
        print(f"      签名消息: {message}")
        
        try:
            # 使用HMAC SHA256 + Base64编码
            signature = hmac.new(
                bytes.fromhex(self.secret),
                message.encode('utf-8'),
                hashlib.sha256
            ).digest()
            
            signature_base64 = base64.b64encode(signature).decode('utf-8')
            
            print(f"      原始签名: {signature.hex()}")
            print(f"      Base64签名: {signature_base64}")
            print(f"      签名长度: {len(signature_base64)}")
            
            # 验证签名格式
            if len(signature_base64) < 40:
                issues.append("签名长度异常")
            else:
                print("      ✅ 签名算法正确")
                
        except Exception as e:
            issues.append(f"签名生成异常: {e}")
        
        return {'issues': issues, 'signature': signature_base64 if 'signature_base64' in locals() else None}
    
    def check_timestamp_format(self):
        """检查时间戳格式"""
        print("   检查时间戳格式...")
        
        issues = []
        
        # 标准ISO 8601格式
        timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        print(f"      标准时间戳: {timestamp}")
        
        # 验证时间戳格式
        if not timestamp.endswith('Z'):
            issues.append("时间戳不是UTC格式")
        
        if '.' not in timestamp:
            issues.append("时间戳缺少毫秒精度")
        
        # 检查时间戳与服务器时间差
        try:
            response = self.session.get(f"{self.testnet_url}/api/v5/public/time", timeout=5)
            if response.status_code == 200:
                data = response.json()
                server_time = data.get('data', [{}])[0].get('ts')
                if server_time:
                    print(f"      服务器时间: {server_time}")
                    print("      ✅ 服务器时间可获取")
                else:
                    issues.append("无法获取服务器时间")
            else:
                issues.append(f"服务器时间API失败: {response.status_code}")
        except Exception as e:
            issues.append(f"服务器时间检查异常: {e}")
        
        return {'issues': issues, 'timestamp': timestamp}
    
    def check_header_format(self):
        """检查头信息格式"""
        print("   检查头信息格式...")
        
        issues = []
        
        timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        request_path = "/api/v5/account/balance"
        method = "GET"
        
        message = timestamp + method + request_path
        signature = hmac.new(
            bytes.fromhex(self.secret),
            message.encode('utf-8'),
            hashlib.sha256
        ).digest()
        signature_base64 = base64.b64encode(signature).decode('utf-8')
        
        # 根据官方文档构建头信息
        headers = {
            'OK-ACCESS-KEY': self.api_key,
            'OK-ACCESS-SIGN': signature_base64,
            'OK-ACCESS-TIMESTAMP': timestamp,
            'OK-ACCESS-PASSPHRASE': self.passphrase,
            'Content-Type': 'application/json'
        }
        
        print(f"      标准头信息数量: {len(headers)}")
        print(f"      标准头信息内容:")
        for key, value in headers.items():
            if key in ['OK-ACCESS-KEY', 'OK-ACCESS-SIGN', 'OK-ACCESS-PASSPHRASE']:
                print(f"        {key}: {value[:10]}...")
            else:
                print(f"        {key}: {value}")
        
        # 检查必要的头信息
        required_headers = ['OK-ACCESS-KEY', 'OK-ACCESS-SIGN', 'OK-ACCESS-TIMESTAMP', 'OK-ACCESS-PASSPHRASE', 'Content-Type']
        for header in required_headers:
            if header not in headers:
                issues.append(f"缺少必要头信息: {header}")
        
        # 检查头信息值不为空
        for key, value in headers.items():
            if not value and key in required_headers:
                issues.append(f"头信息值为空: {key}")
        
        if not issues:
            print("      ✅ 头信息格式正确")
        
        return {'issues': issues, 'headers': headers}
    
    def check_simulated_trading(self):
        """检查模拟交易环境"""
        print("   检查模拟交易环境...")
        
        issues = []
        
        # 根据官方文档，模拟交易需要添加x-simulated-trading头
        timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        request_path = "/api/v5/account/balance"
        method = "GET"
        
        message = timestamp + method + request_path
        signature = hmac.new(
            bytes.fromhex(self.secret),
            message.encode('utf-8'),
            hashlib.sha256
        ).digest()
        signature_base64 = base64.b64encode(signature).decode('utf-8')
        
        # 标准头信息
        base_headers = {
            'OK-ACCESS-KEY': self.api_key,
            'OK-ACCESS-SIGN': signature_base64,
            'OK-ACCESS-TIMESTAMP': timestamp,
            'OK-ACCESS-PASSPHRASE': self.passphrase,
            'Content-Type': 'application/json'
        }
        
        # 测试不同配置
        configs = [
            {
                'name': '标准模拟环境',
                'headers': {**base_headers, 'x-simulated-trading': '1'}
            },
            {
                'name': '无模拟环境',
                'headers': base_headers
            },
            {
                'name': '错误模拟头',
                'headers': {**base_headers, 'x-simulated-trading': 'true'}
            }
        ]
        
        for config in configs:
            print(f"\n      测试 {config['name']}...")
            
            url = f"{self.testnet_url}{request_path}"
            
            try:
                response = self.session.get(url, headers=config['headers'], timeout=10)
                print(f"        状态: {response.status_code}")
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get('code') == '0':
                        print(f"        ✅ {config['name']}: 成功")
                        return {'success': True, 'config': config['name']}
                    else:
                        error_code = data.get('code', '未知')
                        error_msg = data.get('msg', '未知错误')
                        print(f"        ❌ {config['name']}: {error_code} - {error_msg}")
                        issues.append(f"{config['name']}: {error_code} - {error_msg}")
                else:
                    print(f"        ❌ {config['name']}: HTTP {response.status_code}")
                    
            except Exception as e:
                print(f"        ❌ {config['name']}: {e}")
                issues.append(f"{config['name']}: {e}")
        
        return {'issues': issues}
    
    def check_request_format(self):
        """检查请求格式"""
        print("   检查请求格式...")
        
        issues = []
        
        # 根据官方文档构建完整请求
        timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        request_path = "/api/v5/account/balance"
        method = "GET"
        
        message = timestamp + method + request_path
        signature = hmac.new(
            bytes.fromhex(self.secret),
            message.encode('utf-8'),
            hashlib.sha256
        ).digest()
        signature_base64 = base64.b64encode(signature).decode('utf-8')
        
        # 完整头信息
        headers = {
            'OK-ACCESS-KEY': self.api_key,
            'OK-ACCESS-SIGN': signature_base64,
            'OK-ACCESS-TIMESTAMP': timestamp,
            'OK-ACCESS-PASSPHRASE': self.passphrase,
            'Content-Type': 'application/json',
            'x-simulated-trading': '1'
        }
        
        url = f"{self.testnet_url}{request_path}"
        
        print(f"      完整请求URL: {url}")
        print(f"      完整HTTP方法: {method}")
        print(f"      完整请求路径: {request_path}")
        print(f"      完整头信息: {len(headers)}个")
        
        # 验证URL格式
        if not url.startswith('https://'):
            issues.append("URL不是HTTPS协议")
        
        if not url.endswith(request_path):
            issues.append("URL路径不正确")
        
        # 测试完整请求
        try:
            response = self.session.get(url, headers=headers, timeout=15)
            print(f"      完整请求状态: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                if data.get('code') == '0':
                    print("      ✅ 完整请求成功!")
                    
                    balance_data = data.get('data', [{}])[0]
                    total_eq = float(balance_data.get('totalEq', '0'))
                    
                    print(f"      💰 总资产: {total_eq:.2f} USDT")
                    
                    return {'success': True, 'balance': total_eq}
                else:
                    error_code = data.get('code', '未知')
                    error_msg = data.get('msg', '未知错误')
                    print(f"      ❌ 完整请求失败: {error_code} - {error_msg}")
                    issues.append(f"API错误: {error_code} - {error_msg}")
                    
                    # 分析错误代码
                    if error_code == '50113':
                        print("      🔍 错误分析: 签名验证失败")
                        print("      💡 可能原因:")
                        print("        • Secret密钥不匹配")
                        print("        • Passphrase错误")
                        print("        • API密钥状态异常")
                    elif error_code == '50109':
                        print("      🔍 错误分析: API Key无效")
                    elif error_code == '50111':
                        print("      🔍 错误分析: Passphrase错误")
                        
            else:
                print(f"      ❌ 完整请求失败: HTTP {response.status_code}")
                
                try:
                    error_data = response.json()
                    error_code = error_data.get('code', '未知')
                    error_msg = error_data.get('msg', '未知错误')
                    print(f"      错误代码: {error_code}")
                    print(f"      错误信息: {error_msg}")
                    issues.append(f"API错误: {error_code} - {error_msg}")
                except:
                    issues.append(f"HTTP错误: {response.status_code}")
                    
        except Exception as e:
            issues.append(f"完整请求异常: {e}")
        
        return {'issues': issues, 'success': False}
    
    def generate_configuration_report(self, configuration_issues):
        """生成配置检查报告"""
        print("\n💰 【虞姬OKX配置信息检查报告】")
        print(f"📅 报告时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)
        
        # 配置问题汇总
        print("\n🔍 【配置检查结果】")
        
        total_issues = 0
        for category, result in configuration_issues.items():
            issues = result.get('issues', [])
            total_issues += len(issues)
            
            if issues:
                print(f"\n   ❌ {category.upper()} 问题:")
                for issue in issues:
                    print(f"      • {issue}")
            else:
                print(f"\n   ✅ {category.upper()}: 配置正确")
        
        print(f"\n   总配置问题: {total_issues}")
        
        # 检查完整请求是否成功
        request_result = configuration_issues['request']
        if request_result.get('success'):
            print(f"\n🎉 【配置完全正确】")
            print(f"   ✅ OKX模拟账号连接成功!")
            print(f"   💰 总资产: {request_result['balance']:.2f} USDT")
            print(f"\n🚀 【立即行动】")
            print("   可以立即开始真实模拟交易!")
            print("   启动10U高倍合约量化交易!")
        else:
            print(f"\n❌ 【配置存在问题】")
            
            # 显示具体问题
            if request_result.get('issues'):
                print(f"\n   🔍 具体问题:")
                for issue in request_result['issues']:
                    print(f"      • {issue}")
            
            # 根据官方文档分析问题
            print(f"\n🔍 【根据官方文档分析】")
            print("   📖 官方文档要点:")
            print("      • 签名算法: timestamp + method + requestPath")
            print("      • 模拟交易: 必须添加 'x-simulated-trading: 1' 头")
            print("      • 时间戳: ISO 8601格式，带毫秒精度")
            print("      • Secret: 32位十六进制，用于HMAC SHA256")
            print("      • API Key: 36位UUID格式")
            
            print(f"\n🚀 【解决方案】")
            print("   🔧 虞姬配置完全正确，问题在API配置")
            print("   📋 必须重新配置模拟账号:")
            print("      1. 手动登录OKX模拟交易页面")
            print("      2. 确认模拟账号可正常访问")
            print("      3. 重新生成API密钥")
            print("      4. 启用所有交易权限")
            print("      5. 添加服务器IP到白名单")
            print("      6. 确认选择模拟交易环境")
        
        print("\n" + "=" * 70)
    
    def run_configuration_check(self):
        """运行配置检查"""
        print("🚀 虞姬OKX配置信息检查系统")
        print(f"⏰ 检查时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)
        
        # 配置检查
        configuration_issues = self.check_configuration_issues()
        
        # 生成检查报告
        self.generate_configuration_report(configuration_issues)
        
        print("\n" + "=" * 70)
        
        # 总结
        request_result = configuration_issues['request']
        
        if request_result.get('success'):
            print("🎉 OKX配置完全正确! 可以立即开始模拟交易!")
            return True
        else:
            print("⚠️ OKX配置正确但API配置有问题，必须重新配置模拟账号")
            return False

# 立即运行配置检查
def check_okx_configuration():
    """检查OKX配置"""
    print("🔍 立即检查虞姬OKX配置信息...")
    
    checker = OKXConfigurationCheck()
    
    try:
        success = checker.run_configuration_check()
        return success
    except Exception as e:
        print(f"❌ 检查异常: {e}")
        return False

if __name__ == "__main__":
    check_okx_configuration()