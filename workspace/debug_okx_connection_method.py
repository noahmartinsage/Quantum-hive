#!/usr/bin/env python3
"""
虞姬OKX连接方式调试
检查连接方式问题，不是API问题
"""

import time
import hmac
import hashlib
import requests
import json
from datetime import datetime

class OKXConnectionDebug:
    def __init__(self):
        # 老板提供的最新OKX凭据
        self.api_key = "cefedac1-1d25-4fae-861d-9f006e4cd654"
        self.secret = "EE66B6A88F9E57FBCAE6219081DABDE1"
        self.passphrase = "Qian1314."
        self.base_url = "https://www.okx.com"
        
        # 稳健连接
        self.session = requests.Session()
        self.session.trust_env = False
    
    def debug_connection_methods(self):
        """调试连接方式"""
        print("🔍 虞姬OKX连接方式调试...")
        print("=" * 60)
        
        debug_results = {}
        
        # 测试1: 基础签名方式
        print("\n1. 基础签名方式测试...")
        basic_signature = self.test_basic_signature_method()
        debug_results['basic_signature'] = basic_signature
        
        # 测试2: 时间戳格式测试
        print("\n2. 时间戳格式测试...")
        timestamp_test = self.test_timestamp_formats()
        debug_results['timestamp'] = timestamp_test
        
        # 测试3: 签名消息格式测试
        print("\n3. 签名消息格式测试...")
        message_format = self.test_message_formats()
        debug_results['message_format'] = message_format
        
        # 测试4: 头信息格式测试
        print("\n4. 头信息格式测试...")
        header_formats = self.test_header_formats()
        debug_results['header_formats'] = header_formats
        
        # 测试5: 模拟交易特殊配置
        print("\n5. 模拟交易特殊配置...")
        simulated_config = self.test_simulated_special_config()
        debug_results['simulated_config'] = simulated_config
        
        return debug_results
    
    def test_basic_signature_method(self):
        """测试基础签名方式"""
        print("   测试基础签名算法...")
        
        try:
            timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
            request_path = "/api/v5/account/balance"
            
            # 标准签名方法
            message = timestamp + 'GET' + request_path
            print(f"      标准签名消息: {message}")
            
            signature = hmac.new(
                self.secret.encode('utf-8'),
                message.encode('utf-8'),
                hashlib.sha256
            ).hexdigest()
            
            print(f"      标准签名: {signature}")
            
            # 测试不同的签名方法
            signature_methods = [
                {
                    'name': '标准签名',
                    'message': timestamp + 'GET' + request_path,
                    'secret': self.secret
                },
                {
                    'name': '小写签名',
                    'message': timestamp + 'get' + request_path,
                    'secret': self.secret
                },
                {
                    'name': '带空格的签名',
                    'message': timestamp + ' GET ' + request_path,
                    'secret': self.secret
                }
            ]
            
            for method in signature_methods:
                print(f"\n      测试 {method['name']}...")
                print(f"        签名消息: {method['message']}")
                
                signature = hmac.new(
                    method['secret'].encode('utf-8'),
                    method['message'].encode('utf-8'),
                    hashlib.sha256
                ).hexdigest()
                
                print(f"        生成签名: {signature}")
                
                headers = {
                    'OK-ACCESS-KEY': self.api_key,
                    'OK-ACCESS-SIGN': signature,
                    'OK-ACCESS-TIMESTAMP': timestamp,
                    'OK-ACCESS-PASSPHRASE': self.passphrase,
                    'Content-Type': 'application/json',
                    'x-simulated-trading': '1'
                }
                
                url = f"{self.base_url}{request_path}"
                response = self.session.get(url, headers=headers, timeout=10)
                
                print(f"        响应状态: {response.status_code}")
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get('code') == '0':
                        print(f"        ✅ {method['name']}: 成功")
                        return {'success': True, 'method': method['name']}
                    else:
                        error_msg = data.get('msg', '未知错误')
                        print(f"        ❌ {method['name']}: {error_msg}")
                else:
                    print(f"        ❌ {method['name']}: HTTP {response.status_code}")
            
            return {'success': False}
                
        except Exception as e:
            print(f"      ❌ 基础签名测试: {e}")
            return {'success': False, 'error': str(e)}
    
    def test_timestamp_formats(self):
        """测试时间戳格式"""
        print("   测试时间戳格式...")
        
        timestamp_formats = [
            {
                'name': '标准格式',
                'format': datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
            },
            {
                'name': '无毫秒格式',
                'format': datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S') + 'Z'
            },
            {
                'name': '无Z格式',
                'format': datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]
            },
            {
                'name': '简单格式',
                'format': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
            }
        ]
        
        for ts_format in timestamp_formats:
            print(f"\n      测试 {ts_format['name']}...")
            print(f"        时间戳: {ts_format['format']}")
            
            try:
                request_path = "/api/v5/account/balance"
                
                message = ts_format['format'] + 'GET' + request_path
                signature = hmac.new(
                    self.secret.encode('utf-8'),
                    message.encode('utf-8'),
                    hashlib.sha256
                ).hexdigest()
                
                headers = {
                    'OK-ACCESS-KEY': self.api_key,
                    'OK-ACCESS-SIGN': signature,
                    'OK-ACCESS-TIMESTAMP': ts_format['format'],
                    'OK-ACCESS-PASSPHRASE': self.passphrase,
                    'Content-Type': 'application/json',
                    'x-simulated-trading': '1'
                }
                
                url = f"{self.base_url}{request_path}"
                response = self.session.get(url, headers=headers, timeout=10)
                
                print(f"        响应状态: {response.status_code}")
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get('code') == '0':
                        print(f"        ✅ {ts_format['name']}: 成功")
                        return {'success': True, 'format': ts_format['name']}
                    else:
                        error_msg = data.get('msg', '未知错误')
                        print(f"        ❌ {ts_format['name']}: {error_msg}")
                else:
                    print(f"        ❌ {ts_format['name']}: HTTP {response.status_code}")
                    
            except Exception as e:
                print(f"        ❌ {ts_format['name']}: {e}")
        
        return {'success': False}
    
    def test_message_formats(self):
        """测试签名消息格式"""
        print("   测试签名消息格式...")
        
        timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        request_path = "/api/v5/account/balance"
        
        message_formats = [
            {
                'name': '标准格式',
                'message': timestamp + 'GET' + request_path
            },
            {
                'name': '带空格格式',
                'message': timestamp + ' GET ' + request_path
            },
            {
                'name': '小写格式',
                'message': timestamp + 'get' + request_path
            },
            {
                'name': '带查询参数格式',
                'message': timestamp + 'GET' + request_path + '?ccy=USDT'
            }
        ]
        
        for msg_format in message_formats:
            print(f"\n      测试 {msg_format['name']}...")
            print(f"        消息: {msg_format['message']}")
            
            try:
                signature = hmac.new(
                    self.secret.encode('utf-8'),
                    msg_format['message'].encode('utf-8'),
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
                
                url = f"{self.base_url}{request_path}"
                if '查询参数' in msg_format['name']:
                    url += '?ccy=USDT'
                
                response = self.session.get(url, headers=headers, timeout=10)
                
                print(f"        响应状态: {response.status_code}")
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get('code') == '0':
                        print(f"        ✅ {msg_format['name']}: 成功")
                        return {'success': True, 'format': msg_format['name']}
                    else:
                        error_msg = data.get('msg', '未知错误')
                        print(f"        ❌ {msg_format['name']}: {error_msg}")
                else:
                    print(f"        ❌ {msg_format['name']}: HTTP {response.status_code}")
                    
            except Exception as e:
                print(f"        ❌ {msg_format['name']}: {e}")
        
        return {'success': False}
    
    def test_header_formats(self):
        """测试头信息格式"""
        print("   测试头信息格式...")
        
        timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        request_path = "/api/v5/account/balance"
        
        message = timestamp + 'GET' + request_path
        signature = hmac.new(
            self.secret.encode('utf-8'),
            message.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        header_formats = [
            {
                'name': '标准头信息',
                'headers': {
                    'OK-ACCESS-KEY': self.api_key,
                    'OK-ACCESS-SIGN': signature,
                    'OK-ACCESS-TIMESTAMP': timestamp,
                    'OK-ACCESS-PASSPHRASE': self.passphrase,
                    'Content-Type': 'application/json',
                    'x-simulated-trading': '1'
                }
            },
            {
                'name': '小写头信息',
                'headers': {
                    'ok-access-key': self.api_key,
                    'ok-access-sign': signature,
                    'ok-access-timestamp': timestamp,
                    'ok-access-passphrase': self.passphrase,
                    'content-type': 'application/json',
                    'x-simulated-trading': '1'
                }
            },
            {
                'name': '无内容类型头',
                'headers': {
                    'OK-ACCESS-KEY': self.api_key,
                    'OK-ACCESS-SIGN': signature,
                    'OK-ACCESS-TIMESTAMP': timestamp,
                    'OK-ACCESS-PASSPHRASE': self.passphrase,
                    'x-simulated-trading': '1'
                }
            },
            {
                'name': '无模拟交易头',
                'headers': {
                    'OK-ACCESS-KEY': self.api_key,
                    'OK-ACCESS-SIGN': signature,
                    'OK-ACCESS-TIMESTAMP': timestamp,
                    'OK-ACCESS-PASSPHRASE': self.passphrase,
                    'Content-Type': 'application/json'
                }
            }
        ]
        
        for header_format in header_formats:
            print(f"\n      测试 {header_format['name']}...")
            
            try:
                url = f"{self.base_url}{request_path}"
                response = self.session.get(url, headers=header_format['headers'], timeout=10)
                
                print(f"        响应状态: {response.status_code}")
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get('code') == '0':
                        print(f"        ✅ {header_format['name']}: 成功")
                        return {'success': True, 'format': header_format['name']}
                    else:
                        error_msg = data.get('msg', '未知错误')
                        print(f"        ❌ {header_format['name']}: {error_msg}")
                else:
                    print(f"        ❌ {header_format['name']}: HTTP {response.status_code}")
                    
            except Exception as e:
                print(f"        ❌ {header_format['name']}: {e}")
        
        return {'success': False}
    
    def test_simulated_special_config(self):
        """测试模拟交易特殊配置"""
        print("   测试模拟交易特殊配置...")
        
        timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        request_path = "/api/v5/account/balance"
        
        message = timestamp + 'GET' + request_path
        signature = hmac.new(
            self.secret.encode('utf-8'),
            message.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        special_configs = [
            {
                'name': '模拟交易头值为0',
                'headers': {
                    'OK-ACCESS-KEY': self.api_key,
                    'OK-ACCESS-SIGN': signature,
                    'OK-ACCESS-TIMESTAMP': timestamp,
                    'OK-ACCESS-PASSPHRASE': self.passphrase,
                    'Content-Type': 'application/json',
                    'x-simulated-trading': '0'
                }
            },
            {
                'name': '模拟交易头值为true',
                'headers': {
                    'OK-ACCESS-KEY': self.api_key,
                    'OK-ACCESS-SIGN': signature,
                    'OK-ACCESS-TIMESTAMP': timestamp,
                    'OK-ACCESS-PASSPHRASE': self.passphrase,
                    'Content-Type': 'application/json',
                    'x-simulated-trading': 'true'
                }
            },
            {
                'name': '模拟交易头值为false',
                'headers': {
                    'OK-ACCESS-KEY': self.api_key,
                    'OK-ACCESS-SIGN': signature,
                    'OK-ACCESS-TIMESTAMP': timestamp,
                    'OK-ACCESS-PASSPHRASE': self.passphrase,
                    'Content-Type': 'application/json',
                    'x-simulated-trading': 'false'
                }
            },
            {
                'name': '无模拟交易头',
                'headers': {
                    'OK-ACCESS-KEY': self.api_key,
                    'OK-ACCESS-SIGN': signature,
                    'OK-ACCESS-TIMESTAMP': timestamp,
                    'OK-ACCESS-PASSPHRASE': self.passphrase,
                    'Content-Type': 'application/json'
                }
            }
        ]
        
        for config in special_configs:
            print(f"\n      测试 {config['name']}...")
            
            try:
                url = f"{self.base_url}{request_path}"
                response = self.session.get(url, headers=config['headers'], timeout=10)
                
                print(f"        响应状态: {response.status_code}")
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get('code') == '0':
                        print(f"        ✅ {config['name']}: 成功")
                        return {'success': True, 'config': config['name']}
                    else:
                        error_msg = data.get('msg', '未知错误')
                        print(f"        ❌ {config['name']}: {error_msg}")
                else:
                    print(f"        ❌ {config['name']}: HTTP {response.status_code}")
                    
            except Exception as e:
                print(f"        ❌ {config['name']}: {e}")
        
        return {'success': False}
    
    def generate_connection_debug_report(self, debug_results):
        """生成连接调试报告"""
        print("\n💰 【虞姬OKX连接方式调试报告】")
        print(f"📅 报告时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)
        
        # 连接方式分析
        print("\n🔧 【连接方式测试结果】")
        
        successful_tests = []
        failed_tests = []
        
        for test_name, result in debug_results.items():
            if result.get('success'):
                successful_tests.append(test_name)
            else:
                failed_tests.append(test_name)
        
        print(f"   成功测试: {len(successful_tests)}/{len(debug_results)}")
        print(f"   失败测试: {len(failed_tests)}/{len(debug_results)}")
        
        if successful_tests:
            print(f"\n   ✅ 成功测试:")
            for test in successful_tests:
                print(f"      • {test}")
        
        if failed_tests:
            print(f"\n   ❌ 失败测试:")
            for test in failed_tests:
                print(f"      • {test}")
        
        # 根本原因分析
        print(f"\n🔍 【根本原因分析】")
        if not any(result.get('success') for result in debug_results.values()):
            print("   🔧 问题根本原因: 连接方式完全失败")
            print("   💡 可能原因:")
            print("      • API密钥状态异常")
            print("      • 模拟账号配置问题")
            print("      • 服务器IP白名单问题")
            print("      • 模拟账号权限设置问题")
        
        # 最终解决方案
        print(f"\n🚀 【最终解决方案】")
        if any(result.get('success') for result in debug_results.values()):
            print("   ✅ 找到有效连接方式")
            print("   🎯 可以立即开始真实模拟交易")
        else:
            print("   🔧 所有连接方式都失败")
            print("   📋 必须重新配置模拟账号:")
            print("      1. 手动登录OKX模拟交易页面")
            print("      2. 确认模拟账号可正常访问")
            print("      3. 重新生成API密钥")
            print("      4. 设置极简Passphrase")
            print("      5. 启用所有交易权限")
            print("      6. 添加服务器IP到白名单")
        
        print("\n" + "=" * 70)
    
    def run_connection_debug(self):
        """运行连接调试"""
        print("🚀 虞姬OKX连接方式调试系统")
        print(f"⏰ 调试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)
        
        # 连接方式调试
        debug_results = self.debug_connection_methods()
        
        # 生成调试报告
        self.generate_connection_debug_report(debug_results)
        
        print("\n" + "=" * 70)
        
        # 总结
        if any(result.get('success') for result in debug_results.values()):
            print("🎉 找到有效连接方式! 可以立即开始模拟交易!")
            return True
        else:
            print("⚠️ 所有连接方式都失败，必须重新配置模拟账号")
            return False

# 立即运行连接调试
def debug_okx_connection():
    """调试OKX连接"""
    print("🔍 立即调试虞姬OKX连接方式...")
    
    debugger = OKXConnectionDebug()
    
    try:
        success = debugger.run_connection_debug()
        return success
    except Exception as e:
        print(f"❌ 调试异常: {e}")
        return False

if __name__ == "__main__":
    debug_okx_connection()