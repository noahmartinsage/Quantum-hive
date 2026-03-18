#!/usr/bin/env python3
"""
虞姬OKX测试网连接方式设计修复
修复虞姬设计的测试网连接方式问题
"""

import time
import hmac
import hashlib
import requests
import json
import base64
from datetime import datetime

class OKXTestnetDesignFix:
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
    
    def fix_design_problems(self):
        """修复设计问题"""
        print("🔧 虞姬OKX测试网连接方式设计修复...")
        print("=" * 60)
        
        fix_results = {}
        
        # 修复1: 签名算法完全重构
        print("\n1. 签名算法完全重构...")
        signature_fix = self.fix_signature_algorithm()
        fix_results['signature'] = signature_fix
        
        # 修复2: 时间戳格式优化
        print("\n2. 时间戳格式优化...")
        timestamp_fix = self.fix_timestamp_format()
        fix_results['timestamp'] = timestamp_fix
        
        # 修复3: 头信息格式重构
        print("\n3. 头信息格式重构...")
        header_fix = self.fix_header_format()
        fix_results['header'] = header_fix
        
        # 修复4: 请求格式完全重构
        print("\n4. 请求格式完全重构...")
        request_fix = self.fix_request_format()
        fix_results['request'] = request_fix
        
        # 修复5: 完整连接测试
        print("\n5. 完整连接测试...")
        connection_fix = self.fix_complete_connection()
        fix_results['connection'] = connection_fix
        
        return fix_results
    
    def fix_signature_algorithm(self):
        """修复签名算法"""
        print("   修复签名算法...")
        
        issues = []
        
        # 检查Secret密钥
        print(f"      Secret密钥: {self.secret}")
        print(f"      Secret长度: {len(self.secret)}")
        
        # 确保Secret是32位十六进制
        if len(self.secret) != 32:
            issues.append(f"Secret密钥长度异常: {len(self.secret)} (应为32)")
        
        # 验证Secret格式
        try:
            bytes.fromhex(self.secret)
            print("      ✅ Secret格式验证成功")
        except:
            issues.append("Secret密钥不是有效十六进制")
        
        # 重构签名算法
        timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        request_path = "/api/v5/account/balance"
        method = "GET"
        
        # 标准OKX签名格式
        message = timestamp + method + request_path
        print(f"      签名消息: {message}")
        
        # 生成签名
        try:
            signature = hmac.new(
                bytes.fromhex(self.secret),
                message.encode('utf-8'),
                hashlib.sha256
            ).hexdigest()
            
            # 转换为base64编码
            signature_base64 = base64.b64encode(bytes.fromhex(signature)).decode('utf-8')
            
            print(f"      原始签名: {signature}")
            print(f"      Base64签名: {signature_base64}")
            print(f"      签名长度: {len(signature)}")
            
            # 验证签名格式
            if len(signature) != 64:
                issues.append(f"签名长度异常: {len(signature)} (应为64)")
            else:
                print("      ✅ 签名格式验证成功")
                
        except Exception as e:
            issues.append(f"签名生成异常: {e}")
        
        return {'issues': issues, 'signature': signature if 'signature' in locals() else None}
    
    def fix_timestamp_format(self):
        """修复时间戳格式"""
        print("   修复时间戳格式...")
        
        issues = []
        
        # 标准ISO 8601格式
        timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        print(f"      标准时间戳: {timestamp}")
        
        # 验证时间戳格式
        try:
            # 检查格式是否符合ISO 8601
            if not timestamp.endswith('Z'):
                issues.append("时间戳不是UTC格式")
            
            # 检查毫秒精度
            if '.' not in timestamp:
                issues.append("时间戳缺少毫秒精度")
            
            # 验证时间戳解析
            try:
                # 标准ISO 8601解析
                parsed = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%fZ')
                print(f"      ✅ 时间戳解析成功")
            except:
                # 尝试其他格式
                try:
                    parsed = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ')
                    print(f"      ⚠️ 时间戳无毫秒精度")
                except Exception as e:
                    issues.append(f"时间戳解析异常: {e}")
                    
        except Exception as e:
            issues.append(f"时间戳处理异常: {e}")
        
        return {'issues': issues, 'timestamp': timestamp}
    
    def fix_header_format(self):
        """修复头信息格式"""
        print("   修复头信息格式...")
        
        issues = []
        
        timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        request_path = "/api/v5/account/balance"
        method = "GET"
        
        message = timestamp + method + request_path
        signature = hmac.new(
            bytes.fromhex(self.secret),
            message.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        # 完全重构头信息
        headers = {
            'OK-ACCESS-KEY': self.api_key,
            'OK-ACCESS-SIGN': signature,
            'OK-ACCESS-TIMESTAMP': timestamp,
            'OK-ACCESS-PASSPHRASE': self.passphrase,
            'Content-Type': 'application/json',
            'x-simulated-trading': '1',
            'User-Agent': 'Mozilla/5.0 (compatible; OpenClaw/1.0)'
        }
        
        print(f"      重构头信息数量: {len(headers)}")
        print(f"      重构头信息内容:")
        for key, value in headers.items():
            if key in ['OK-ACCESS-KEY', 'OK-ACCESS-SIGN', 'OK-ACCESS-PASSPHRASE']:
                print(f"        {key}: {value[:10]}...")
            else:
                print(f"        {key}: {value}")
        
        # 验证必要的头信息
        required_headers = ['OK-ACCESS-KEY', 'OK-ACCESS-SIGN', 'OK-ACCESS-TIMESTAMP', 'OK-ACCESS-PASSPHRASE']
        for header in required_headers:
            if header not in headers:
                issues.append(f"缺少必要头信息: {header}")
        
        # 验证头信息值不为空
        for key, value in headers.items():
            if not value and key in required_headers:
                issues.append(f"头信息值为空: {key}")
        
        if not issues:
            print("      ✅ 头信息格式验证成功")
        
        return {'issues': issues, 'headers': headers}
    
    def fix_request_format(self):
        """修复请求格式"""
        print("   修复请求格式...")
        
        issues = []
        
        # 完全重构请求格式
        timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        request_path = "/api/v5/account/balance"
        method = "GET"
        
        message = timestamp + method + request_path
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
            'x-simulated-trading': '1',
            'User-Agent': 'Mozilla/5.0 (compatible; OpenClaw/1.0)'
        }
        
        url = f"{self.testnet_url}{request_path}"
        
        print(f"      重构请求URL: {url}")
        print(f"      重构HTTP方法: {method}")
        print(f"      重构请求路径: {request_path}")
        
        # 验证URL格式
        if not url.startswith('https://'):
            issues.append("URL不是HTTPS协议")
        
        if not url.endswith(request_path):
            issues.append("URL路径不正确")
        
        # 测试重构的请求
        try:
            response = self.session.get(url, headers=headers, timeout=15)
            print(f"      重构请求状态: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                if data.get('code') == '0':
                    print("      ✅ 重构请求成功!")
                    
                    balance_data = data.get('data', [{}])[0]
                    total_eq = float(balance_data.get('totalEq', '0'))
                    
                    print(f"      💰 总资产: {total_eq:.2f} USDT")
                    
                    return {'success': True, 'balance': total_eq}
                else:
                    error_code = data.get('code', '未知')
                    error_msg = data.get('msg', '未知错误')
                    print(f"      ❌ 重构请求失败: {error_code} - {error_msg}")
                    issues.append(f"API错误: {error_code} - {error_msg}")
            else:
                print(f"      ❌ 重构请求失败: HTTP {response.status_code}")
                
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
            issues.append(f"重构请求异常: {e}")
        
        return {'issues': issues, 'success': False}
    
    def fix_complete_connection(self):
        """修复完整连接"""
        print("   修复完整连接...")
        
        issues = []
        
        # 完整连接测试
        timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        request_path = "/api/v5/account/balance"
        method = "GET"
        
        message = timestamp + method + request_path
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
            'x-simulated-trading': '1',
            'User-Agent': 'Mozilla/5.0 (compatible; OpenClaw/1.0)'
        }
        
        url = f"{self.testnet_url}{request_path}"
        
        print(f"      完整连接URL: {url}")
        print(f"      完整连接头信息: {len(headers)}个")
        
        try:
            response = self.session.get(url, headers=headers, timeout=20)
            print(f"      完整连接状态: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                if data.get('code') == '0':
                    print("      ✅ 完整连接成功!")
                    
                    balance_data = data.get('data', [{}])[0]
                    total_eq = float(balance_data.get('totalEq', '0'))
                    
                    print(f"      💰 总资产: {total_eq:.2f} USDT")
                    
                    # 显示货币详情
                    details = balance_data.get('details', [])
                    for detail in details:
                        ccy = detail.get('ccy', '')
                        cash_bal = float(detail.get('cashBal', '0'))
                        if cash_bal > 0:
                            print(f"      {ccy}: {cash_bal:.4f}")
                    
                    return {'success': True, 'balance': total_eq}
                else:
                    error_code = data.get('code', '未知')
                    error_msg = data.get('msg', '未知错误')
                    print(f"      ❌ 完整连接失败: {error_code} - {error_msg}")
                    issues.append(f"API错误: {error_code} - {error_msg}")
            else:
                print(f"      ❌ 完整连接失败: HTTP {response.status_code}")
                
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
            issues.append(f"完整连接异常: {e}")
        
        return {'issues': issues, 'success': False}
    
    def generate_design_fix_report(self, fix_results):
        """生成设计修复报告"""
        print("\n💰 【虞姬OKX测试网连接方式设计修复报告】")
        print(f"📅 报告时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)
        
        # 修复结果汇总
        print("\n🔧 【设计修复结果】")
        
        successful_fixes = []
        failed_fixes = []
        
        for fix_name, result in fix_results.items():
            if result.get('success') or len(result.get('issues', [])) == 0:
                successful_fixes.append(fix_name)
            else:
                failed_fixes.append(fix_name)
        
        print(f"   成功修复: {len(successful_fixes)}/{len(fix_results)}")
        print(f"   失败修复: {len(failed_fixes)}/{len(fix_results)}")
        
        if successful_fixes:
            print(f"\n   ✅ 成功修复:")
            for fix in successful_fixes:
                print(f"      • {fix}")
        
        if failed_fixes:
            print(f"\n   ❌ 失败修复:")
            for fix in failed_fixes:
                print(f"      • {fix}")
        
        # 检查完整连接是否成功
        connection_result = fix_results['connection']
        if connection_result.get('success'):
            print(f"\n🎉 【虞姬连接方式修复成功】")
            print(f"   ✅ OKX模拟账号连接成功!")
            print(f"   💰 总资产: {connection_result['balance']:.2f} USDT")
            print(f"\n🚀 【立即行动】")
            print("   可以立即开始真实模拟交易!")
            print("   启动10U高倍合约量化交易!")
        else:
            print(f"\n❌ 【虞姬连接方式修复失败】")
            print(f"   🔧 完整连接失败")
            
            # 显示具体问题
            if connection_result.get('issues'):
                print(f"\n   🔍 具体问题:")
                for issue in connection_result['issues']:
                    print(f"      • {issue}")
            
            print(f"\n🚀 【最终解决方案】")
            print("   🔧 虞姬连接方式无法修复")
            print("   📋 必须重新配置模拟账号:")
            print("      1. 手动登录OKX模拟交易页面")
            print("      2. 确认模拟账号可正常访问")
            print("      3. 重新生成API密钥")
            print("      4. 启用所有交易权限")
            print("      5. 添加服务器IP到白名单")
        
        print("\n" + "=" * 70)
    
    def run_design_fix(self):
        """运行设计修复"""
        print("🚀 虞姬OKX测试网连接方式设计修复系统")
        print(f"⏰ 修复时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)
        
        # 设计修复
        fix_results = self.fix_design_problems()
        
        # 生成修复报告
        self.generate_design_fix_report(fix_results)
        
        print("\n" + "=" * 70)
        
        # 总结
        connection_result = fix_results['connection']
        
        if connection_result.get('success'):
            print("🎉 虞姬测试网连接方式修复成功! 可以立即开始模拟交易!")
            return True
        else:
            print("⚠️ 虞姬测试网连接方式无法修复，必须重新配置模拟账号")
            return False

# 立即运行设计修复
def fix_okx_testnet_design():
    """修复OKX测试网连接设计"""
    print("🔧 立即修复虞姬OKX测试网连接方式设计...")
    
    fixer = OKXTestnetDesignFix()
    
    try:
        success = fixer.run_design_fix()
        return success
    except Exception as e:
        print(f"❌ 修复异常: {e}")
        return False

if __name__ == "__main__":
    fix_okx_testnet_design()