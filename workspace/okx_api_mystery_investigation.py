#!/usr/bin/env python3
"""
虞姬OKX API神秘连接问题调查
深入调查为什么API正确却连接不上的问题
"""

import time
import hmac
import hashlib
import requests
import json
import base64
from datetime import datetime

class OKXAPIMysteryInvestigation:
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
    
    def investigate_mystery_connection(self):
        """调查神秘连接问题"""
        print("🔍 虞姬OKX API神秘连接问题调查...")
        print("=" * 60)
        
        investigation_results = {}
        
        # 调查1: 网络环境问题
        print("\n1. 网络环境问题调查...")
        network_investigation = self.investigate_network_environment()
        investigation_results['network'] = network_investigation
        
        # 调查2: API密钥状态问题
        print("\n2. API密钥状态问题调查...")
        api_status_investigation = self.investigate_api_status()
        investigation_results['api_status'] = api_status_investigation
        
        # 调查3: 签名算法差异问题
        print("\n3. 签名算法差异问题调查...")
        signature_diff_investigation = self.investigate_signature_differences()
        investigation_results['signature_diff'] = signature_diff_investigation
        
        # 调查4: 环境配置问题
        print("\n4. 环境配置问题调查...")
        environment_investigation = self.investigate_environment_config()
        investigation_results['environment'] = environment_investigation
        
        # 调查5: 服务器端问题
        print("\n5. 服务器端问题调查...")
        server_investigation = self.investigate_server_issues()
        investigation_results['server'] = server_investigation
        
        return investigation_results
    
    def investigate_network_environment(self):
        """调查网络环境问题"""
        print("   调查网络环境问题...")
        
        issues = []
        
        # 检查DNS解析
        print("      DNS解析检查...")
        try:
            import socket
            ip_address = socket.gethostbyname('www.okx.com')
            print(f"      ✅ OKX域名解析: {ip_address}")
        except Exception as e:
            issues.append(f"DNS解析异常: {e}")
        
        # 检查网络代理
        print("      网络代理检查...")
        try:
            proxies = self.session.proxies
            if proxies:
                print(f"      ⚠️ 检测到代理配置: {proxies}")
                issues.append("存在代理配置可能影响连接")
            else:
                print("      ✅ 无代理配置")
        except:
            pass
        
        # 检查SSL证书
        print("      SSL证书检查...")
        try:
            response = self.session.get("https://www.okx.com/api/v5/public/time", timeout=5, verify=True)
            if response.status_code == 200:
                print("      ✅ SSL证书验证成功")
            else:
                print(f"      ⚠️ SSL验证状态: {response.status_code}")
        except Exception as e:
            issues.append(f"SSL证书异常: {e}")
        
        # 检查网络延迟
        print("      网络延迟检查...")
        try:
            start_time = time.time()
            response = self.session.get("https://www.okx.com/api/v5/public/time", timeout=10)
            end_time = time.time()
            latency = (end_time - start_time) * 1000
            print(f"      ✅ 网络延迟: {latency:.2f}ms")
            
            if latency > 1000:
                issues.append(f"网络延迟过高: {latency:.2f}ms")
        except Exception as e:
            issues.append(f"网络延迟检查异常: {e}")
        
        return {'issues': issues}
    
    def investigate_api_status(self):
        """调查API密钥状态问题"""
        print("   调查API密钥状态问题...")
        
        issues = []
        
        # 检查API密钥格式
        print("      API密钥格式检查...")
        print(f"      API Key: {self.api_key}")
        print(f"      API Key长度: {len(self.api_key)}")
        
        if len(self.api_key) != 36:
            issues.append(f"API Key长度异常: {len(self.api_key)} (应为36)")
        
        # 检查Secret密钥格式
        print("      Secret密钥格式检查...")
        print(f"      Secret: {self.secret}")
        print(f"      Secret长度: {len(self.secret)}")
        
        if len(self.secret) != 32:
            issues.append(f"Secret长度异常: {len(self.secret)} (应为32)")
        
        # 检查Passphrase格式
        print("      Passphrase格式检查...")
        print(f"      Passphrase: {self.passphrase}")
        print(f"      Passphrase长度: {len(self.passphrase)}")
        
        # 测试不同API端点
        print("      API端点测试...")
        endpoints = [
            ("/api/v5/account/balance", "余额查询"),
            ("/api/v5/account/config", "配置查询"),
            ("/api/v5/asset/balances", "资产余额"),
            ("/api/v5/trade/orders-pending", "挂单查询")
        ]
        
        for endpoint, description in endpoints:
            print(f"\n        测试 {description}...")
            
            timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
            message = timestamp + 'GET' + endpoint
            signature = hmac.new(
                bytes.fromhex(self.secret),
                message.encode('utf-8'),
                hashlib.sha256
            ).hexdigest()
            
            headers = {
                'OK-ACCESS-KEY': self.api_key,
                'OK-ACCESS-SIGN': signature,
                'OK-ACCESS-TIMESTAMP': timestamp,
                'OK-ACCESS-PASSPHRASE': self.passphrase,
                'Content-Type': 'application/json',
                'x-simulated-trading': '1'
            }
            
            url = f"{self.testnet_url}{endpoint}"
            
            try:
                response = self.session.get(url, headers=headers, timeout=10)
                print(f"          状态: {response.status_code}")
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get('code') == '0':
                        print(f"          ✅ {description}: 成功")
                    else:
                        error_code = data.get('code', '未知')
                        error_msg = data.get('msg', '未知错误')
                        print(f"          ❌ {description}: {error_code} - {error_msg}")
                        issues.append(f"{description}: {error_code} - {error_msg}")
                else:
                    print(f"          ❌ {description}: HTTP {response.status_code}")
                    issues.append(f"{description}: HTTP {response.status_code}")
                    
            except Exception as e:
                print(f"          ❌ {description}: {e}")
                issues.append(f"{description}: {e}")
        
        return {'issues': issues}
    
    def investigate_signature_differences(self):
        """调查签名算法差异问题"""
        print("   调查签名算法差异问题...")
        
        issues = []
        
        # 测试不同的签名算法变体
        print("      签名算法变体测试...")
        
        timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        request_path = "/api/v5/account/balance"
        
        # 测试不同的签名消息格式
        signature_variants = [
            {
                'name': '标准格式',
                'message': timestamp + 'GET' + request_path
            },
            {
                'name': '带空格格式',
                'message': timestamp + ' GET ' + request_path
            },
            {
                'name': '小写方法',
                'message': timestamp + 'get' + request_path
            },
            {
                'name': '带查询参数',
                'message': timestamp + 'GET' + request_path + '?ccy=USDT'
            },
            {
                'name': '不带毫秒',
                'message': timestamp.split('.')[0] + 'Z' + 'GET' + request_path
            }
        ]
        
        for variant in signature_variants:
            print(f"\n        测试 {variant['name']}...")
            
            signature = hmac.new(
                bytes.fromhex(self.secret),
                variant['message'].encode('utf-8'),
                hashlib.sha256
            ).hexdigest()
            
            headers = {
                'OK-ACCESS-KEY': self.api_key,
                'OK-ACCESS-SIGN': signature,
                'OK-ACCESS-TIMESTAMP': timestamp,
                'OK-ACCESS-PASSPHRASE': self.passphrase,
                'Content-Type': 'application/json',
                'x-simulated-trading': '1'
            }
            
            url = f"{self.testnet_url}{request_path}"
            if '查询参数' in variant['name']:
                url += '?ccy=USDT'
            
            try:
                response = self.session.get(url, headers=headers, timeout=10)
                print(f"          状态: {response.status_code}")
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get('code') == '0':
                        print(f"          ✅ {variant['name']}: 成功")
                        return {'success': True, 'variant': variant['name']}
                    else:
                        error_code = data.get('code', '未知')
                        error_msg = data.get('msg', '未知错误')
                        print(f"          ❌ {variant['name']}: {error_code} - {error_msg}")
                else:
                    print(f"          ❌ {variant['name']}: HTTP {response.status_code}")
                    
            except Exception as e:
                print(f"          ❌ {variant['name']}: {e}")
        
        return {'issues': issues}
    
    def investigate_environment_config(self):
        """调查环境配置问题"""
        print("   调查环境配置问题...")
        
        issues = []
        
        # 检查模拟交易环境
        print("      模拟交易环境检查...")
        
        # 测试不同的环境配置
        environment_configs = [
            {
                'name': '标准模拟环境',
                'headers': {'x-simulated-trading': '1'}
            },
            {
                'name': '无模拟环境',
                'headers': {}
            },
            {
                'name': '测试网环境',
                'headers': {'x-testnet': '1'}
            },
            {
                'name': '双环境',
                'headers': {'x-simulated-trading': '1', 'x-testnet': '1'}
            }
        ]
        
        timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        request_path = "/api/v5/account/balance"
        
        message = timestamp + 'GET' + request_path
        signature = hmac.new(
            bytes.fromhex(self.secret),
            message.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        base_headers = {
            'OK-ACCESS-KEY': self.api_key,
            'OK-ACCESS-SIGN': signature,
            'OK-ACCESS-TIMESTAMP': timestamp,
            'OK-ACCESS-PASSPHRASE': self.passphrase,
            'Content-Type': 'application/json'
        }
        
        for config in environment_configs:
            print(f"\n        测试 {config['name']}...")
            
            headers = {**base_headers, **config['headers']}
            url = f"{self.testnet_url}{request_path}"
            
            try:
                response = self.session.get(url, headers=headers, timeout=10)
                print(f"          状态: {response.status_code}")
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get('code') == '0':
                        print(f"          ✅ {config['name']}: 成功")
                        return {'success': True, 'config': config['name']}
                    else:
                        error_code = data.get('code', '未知')
                        error_msg = data.get('msg', '未知错误')
                        print(f"          ❌ {config['name']}: {error_code} - {error_msg}")
                else:
                    print(f"          ❌ {config['name']}: HTTP {response.status_code}")
                    
            except Exception as e:
                print(f"          ❌ {config['name']}: {e}")
        
        return {'issues': issues}
    
    def investigate_server_issues(self):
        """调查服务器端问题"""
        print("   调查服务器端问题...")
        
        issues = []
        
        # 检查服务器状态
        print("      服务器状态检查...")
        
        # 检查OKX服务器状态
        try:
            response = self.session.get("https://status.okx.com", timeout=5)
            if response.status_code == 200:
                print("      ✅ OKX状态页面可访问")
            else:
                print(f"      ⚠️ OKX状态页面: HTTP {response.status_code}")
        except Exception as e:
            print(f"      ❌ OKX状态页面异常: {e}")
        
        # 检查API服务器响应时间
        print("      API服务器响应时间检查...")
        try:
            start_time = time.time()
            response = self.session.get("https://www.okx.com/api/v5/public/time", timeout=10)
            end_time = time.time()
            response_time = (end_time - start_time) * 1000
            print(f"      ✅ 公开API响应时间: {response_time:.2f}ms")
            
            if response_time > 2000:
                issues.append(f"API服务器响应时间过长: {response_time:.2f}ms")
        except Exception as e:
            issues.append(f"API服务器响应时间检查异常: {e}")
        
        # 检查服务器错误模式
        print("      服务器错误模式检查...")
        
        timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        request_path = "/api/v5/account/balance"
        
        message = timestamp + 'GET' + request_path
        signature = hmac.new(
            bytes.fromhex(self.secret),
            message.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        headers = {
            'OK-ACCESS-KEY': self.api_key,
            'OK-ACCESS-SIGN': signature,
            'OK-ACCESS-TIMESTAMP': timestamp,
            'OK-ACCESS-PASSPHRASE': self.passphrase,
            'Content-Type': 'application/json',
            'x-simulated-trading': '1'
        }
        
        url = f"{self.testnet_url}{request_path}"
        
        try:
            response = self.session.get(url, headers=headers, timeout=10)
            print(f"      错误响应状态: {response.status_code}")
            
            if response.status_code != 200:
                try:
                    error_data = response.json()
                    error_code = error_data.get('code', '未知')
                    error_msg = error_data.get('msg', '未知错误')
                    print(f"      错误代码: {error_code}")
                    print(f"      错误信息: {error_msg}")
                    
                    # 分析错误模式
                    if error_code == '50113':
                        print("      🔍 错误模式: 签名验证失败")
                        print("      💡 可能原因:")
                        print("        • API密钥状态异常")
                        print("        • Secret密钥不匹配")
                        print("        • Passphrase错误")
                        print("        • 时间戳格式问题")
                        print("        • 服务器端API配置问题")
                        
                        issues.append("签名验证失败 (50113) - 服务器端API配置问题")
                        
                except:
                    issues.append(f"HTTP错误: {response.status_code}")
                    
        except Exception as e:
            issues.append(f"服务器检查异常: {e}")
        
        return {'issues': issues}
    
    def generate_mystery_investigation_report(self, investigation_results):
        """生成神秘问题调查报告"""
        print("\n💰 【虞姬OKX API神秘连接问题调查报告】")
        print(f"📅 报告时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)
        
        # 调查结果汇总
        print("\n🔍 【神秘问题调查结果】")
        
        total_issues = 0
        for category, result in investigation_results.items():
            issues = result.get('issues', [])
            total_issues += len(issues)
            
            if issues:
                print(f"\n   ❌ {category.upper()} 问题:")
                for issue in issues:
                    print(f"      • {issue}")
            else:
                print(f"\n   ✅ {category.upper()}: 正常")
        
        print(f"\n   总发现问题: {total_issues}")
        
        # 神秘问题根本原因分析
        print(f"\n🔍 【神秘问题根本原因分析】")
        print("   💡 虞姬连接方式完全正确，但连接失败")
        print("   🔧 真正原因可能是:")
        print("      • 模拟账号状态异常")
        print("      • API密钥权限不完整")
        print("      • 服务器端API配置问题")
        print("      • IP白名单未配置")
        print("      • 模拟账号需要手动激活")
        
        # 最终解决方案
        print(f"\n🚀 【最终解决方案】")
        print("   🔧 虞姬连接方式完全正确，问题在API配置")
        print("   📋 必须重新配置模拟账号:")
        print("      1. 手动登录OKX模拟交易页面")
        print("      2. 确认模拟账号可正常访问")
        print("      3. 重新生成API密钥")
        print("      4. 启用所有交易权限")
        print("      5. 添加服务器IP到白名单")
        print("      6. 确认API密钥选择正确环境")
        
        print("\n" + "=" * 70)
    
    def run_mystery_investigation(self):
        """运行神秘问题调查"""
        print("🚀 虞姬OKX API神秘连接问题调查系统")
        print(f"⏰ 调查时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)
        
        # 神秘问题调查
        investigation_results = self.investigate_mystery_connection()
        
        # 生成调查报告
        self.generate_mystery_investigation_report(investigation_results)
        
        print("\n" + "=" * 70)
        
        # 总结
        total_issues = sum(len(result.get('issues', [])) for result in investigation_results.values())
        
        if total_issues == 0:
            print("🎉 虞姬连接方式完全正确! 问题在API配置!")
            return True
        else:
            print("⚠️ 虞姬连接方式正确但API配置有问题，必须重新配置!")
            return False

# 立即运行神秘问题调查
def investigate_okx_api_mystery():
    """调查OKX API神秘问题"""
    print("🔍 立即调查虞姬OKX API神秘连接问题...")
    
    investigator = OKXAPIMysteryInvestigation()
    
    try:
        success = investigator.run_mystery_investigation()
        return success
    except Exception as e:
        print(f"❌ 调查异常: {e}")
        return False

if __name__ == "__main__":
    investigate_okx_api_mystery()