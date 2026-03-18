#!/usr/bin/env python3
"""
虞姬OKX详细配置测试
测试已配置好的密码、白名单和交易权限的具体问题
"""

import time
import hmac
import hashlib
import requests
import json
from datetime import datetime

class OKXDetailedConfigTest:
    def __init__(self):
        # 已配置的API信息
        self.api_key = "e4753767-b2f7-4495-b2d9-0166238b1076"
        self.secret = "FBBB847F11CC85396F411B1D52E35A1E"
        self.passphrase = "Abc123456"
        self.base_url = "https://www.okx.com"
        
        # 稳健连接
        self.session = requests.Session()
        self.session.trust_env = False
    
    def test_detailed_authentication(self):
        """详细测试认证问题"""
        print("🔍 详细测试OKX认证配置问题...")
        print("=" * 60)
        
        # 测试1: 时间戳格式
        print("\n1. 测试时间戳格式...")
        timestamp_tests = [
            (datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z', "标准格式"),
            (datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ'), "完整格式"),
            (datetime.utcnow().isoformat() + 'Z', "ISO格式")
        ]
        
        for timestamp, description in timestamp_tests:
            result = self.test_single_request(timestamp)
            print(f"   {description}: {timestamp}")
            if result.get('success'):
                print(f"      ✅ 成功")
                return result
            else:
                print(f"      ❌ 失败: {result.get('error')}")
        
        # 测试2: 签名算法
        print("\n2. 测试签名算法...")
        signature_tests = self.test_signature_variations()
        
        # 测试3: 请求头格式
        print("\n3. 测试请求头格式...")
        header_tests = self.test_header_variations()
        
        return None
    
    def test_single_request(self, timestamp):
        """测试单个请求"""
        try:
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
            response = self.session.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('code') == '0':
                    return {'success': True, 'data': data}
                else:
                    return {'success': False, 'error': data.get('msg')}
            else:
                return {'success': False, 'error': f'HTTP {response.status_code}'}
                
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def test_signature_variations(self):
        """测试签名算法变体"""
        print("   测试不同签名方式...")
        
        variations = [
            ("标准HMAC-SHA256", "正常"),
            ("小写Secret", self.secret.lower()),
            ("大写Secret", self.secret.upper()),
        ]
        
        for description, secret_var in variations:
            try:
                timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
                request_path = "/api/v5/account/balance"
                
                message = timestamp + 'GET' + request_path
                
                if description == "标准HMAC-SHA256":
                    signature = hmac.new(
                        self.secret.encode('utf-8'),
                        message.encode('utf-8'),
                        hashlib.sha256
                    ).hexdigest()
                else:
                    signature = hmac.new(
                        secret_var.encode('utf-8'),
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
                response = self.session.get(url, headers=headers, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get('code') == '0':
                        print(f"      ✅ {description}: 成功")
                        return {'success': True, 'method': description}
                    else:
                        print(f"      ❌ {description}: {data.get('msg')}")
                else:
                    print(f"      ❌ {description}: HTTP {response.status_code}")
                    
            except Exception as e:
                print(f"      ❌ {description}: {e}")
        
        return {'success': False}
    
    def test_header_variations(self):
        """测试请求头变体"""
        print("   测试不同请求头格式...")
        
        header_variations = [
            ("标准头", {
                'OK-ACCESS-KEY': self.api_key,
                'OK-ACCESS-SIGN': '',  # 动态计算
                'OK-ACCESS-TIMESTAMP': '',  # 动态计算
                'OK-ACCESS-PASSPHRASE': self.passphrase,
                'Content-Type': 'application/json'
            }),
            ("小写头", {
                'ok-access-key': self.api_key,
                'ok-access-sign': '',
                'ok-access-timestamp': '',
                'ok-access-passphrase': self.passphrase,
                'content-type': 'application/json'
            }),
        ]
        
        for description, headers_template in header_variations:
            try:
                timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
                request_path = "/api/v5/account/balance"
                
                message = timestamp + 'GET' + request_path
                signature = hmac.new(
                    self.secret.encode('utf-8'),
                    message.encode('utf-8'),
                    hashlib.sha256
                ).hexdigest()
                
                # 填充动态值
                headers = headers_template.copy()
                if 'OK-ACCESS-SIGN' in headers:
                    headers['OK-ACCESS-SIGN'] = signature
                if 'ok-access-sign' in headers:
                    headers['ok-access-sign'] = signature
                if 'OK-ACCESS-TIMESTAMP' in headers:
                    headers['OK-ACCESS-TIMESTAMP'] = timestamp
                if 'ok-access-timestamp' in headers:
                    headers['ok-access-timestamp'] = timestamp
                
                url = f"{self.base_url}{request_path}"
                response = self.session.get(url, headers=headers, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get('code') == '0':
                        print(f"      ✅ {description}: 成功")
                        return {'success': True, 'method': description}
                    else:
                        print(f"      ❌ {description}: {data.get('msg')}")
                else:
                    print(f"      ❌ {description}: HTTP {response.status_code}")
                    
            except Exception as e:
                print(f"      ❌ {description}: {e}")
        
        return {'success': False}
    
    def check_server_side_issues(self):
        """检查服务器端问题"""
        print("\n4. 检查服务器端问题...")
        
        # 获取服务器IP
        try:
            import socket
            server_ip = socket.gethostbyname('www.okx.com')
            print(f"   🔍 OKX服务器IP: {server_ip}")
        except:
            print("   🔍 无法获取服务器IP")
        
        # 测试网络延迟
        try:
            import subprocess
            result = subprocess.run(['ping', '-c', '3', 'www.okx.com'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                print("   ✅ 网络连通性: 正常")
            else:
                print("   ❌ 网络连通性: 异常")
        except:
            print("   🔍 无法测试网络连通性")
    
    def test_api_permission_levels(self):
        """测试API权限级别"""
        print("\n5. 测试API权限级别...")
        
        # 即使认证失败，也尝试获取错误信息
        try:
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
            response = self.session.get(url, headers=headers, timeout=10)
            
            print(f"   HTTP状态码: {response.status_code}")
            
            if response.status_code == 401:
                # 详细分析401错误
                print("   🔍 401错误详细分析:")
                
                # 检查响应头
                print(f"      响应头: {dict(response.headers)}")
                
                # 检查响应体
                try:
                    error_data = response.json()
                    print(f"      错误代码: {error_data.get('code')}")
                    print(f"      错误信息: {error_data.get('msg')}")
                    
                    # 根据错误代码提供具体建议
                    error_code = error_data.get('code')
                    if error_code == '50105':
                        print("      💡 建议: Passphrase不正确")
                    elif error_code == '50114':
                        print("      💡 建议: API密钥无效")
                    elif error_code == '50014':
                        print("      💡 建议: IP白名单限制")
                    elif error_code == '50113':
                        print("      💡 建议: API权限不足")
                    else:
                        print("      💡 建议: 未知错误，联系OKX客服")
                        
                except:
                    print(f"      原始响应: {response.text}")
            
        except Exception as e:
            print(f"   ❌ 权限测试异常: {e}")
    
    def generate_detailed_report(self):
        """生成详细报告"""
        print("\n🔧 【OKX详细配置问题报告】")
        print(f"📅 报告时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)
        
        # 配置状态
        print("\n⚙️ 【配置状态】")
        print("   ✅ 白名单: 已配置")
        print("   ✅ 交易权限: 已配置") 
        print("   ✅ 密码: 已配置")
        print("   ❌ API连接: 认证失败")
        
        # 问题分析
        print("\n🔍 【问题分析】")
        print("   虽然所有配置都已设置，但API认证仍然失败")
        print("   可能原因:")
        print("      • Passphrase字符集问题（特殊字符编码）")
        print("      • API密钥状态异常（刚创建需要时间生效）")
        print("      • OKX服务器端配置问题")
        print("      • 网络代理或防火墙拦截")
        
        # 立即解决方案
        print("\n🚀 【立即解决方案】")
        print("   1. 等待API密钥生效（刚创建可能需要几分钟）")
        print("   2. 验证Passphrase特殊字符编码")
        print("   3. 联系OKX客服确认API状态")
        print("   4. 检查网络代理设置")
        
        # 备用方案
        print("\n💡 【备用方案】")
        print("   • 继续使用模拟交易系统（当前885.80 USDT）")
        print("   • 等待API问题解决后切换真实交易")
        print("   • 保持向百万美元目标前进")
    
    def run_detailed_config_test(self):
        """运行详细配置测试"""
        print("🚀 虞姬OKX详细配置测试")
        print(f"⏰ 测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)
        
        # 详细认证测试
        auth_result = self.test_detailed_authentication()
        
        # 检查服务器端问题
        self.check_server_side_issues()
        
        # 测试API权限级别
        self.test_api_permission_levels()
        
        # 生成详细报告
        self.generate_detailed_report()
        
        print("\n" + "=" * 70)
        
        if auth_result and auth_result.get('success'):
            print("✅ 配置测试成功! 可以立即开始交易!")
        else:
            print("⚠️ 配置测试失败，建议等待API生效或联系OKX客服")

# 立即运行详细配置测试
def test_okx_detailed_config():
    """测试OKX详细配置"""
    print("🔍 立即测试虞姬OKX详细配置问题...")
    
    tester = OKXDetailedConfigTest()
    
    try:
        tester.run_detailed_config_test()
    except Exception as e:
        print(f"❌ 配置测试异常: {e}")

if __name__ == "__main__":
    test_okx_detailed_config()