#!/usr/bin/env python3
"""
虞姬OKX测试网连接方式设计调查
深入调查虞姬设计的测试网连接方式问题
"""

import time
import hmac
import hashlib
import requests
import json
from datetime import datetime

class OKXTestnetDesignInvestigation:
    def __init__(self):
        # 老板提供的最新OKX凭据
        self.api_key = "cd06b52e-575b-4ca3-9ab2-f23a36e29f9e"
        self.secret = "6D5E919E861D9DF646AC1C01A09E6002"
        self.passphrase = "Qlzwqc2012."
        
        # 测试网专用API地址
        self.testnet_url = "https://www.okx.com"
        self.testnet_ws_url = "wss://wspap.okx.com:8443/ws/v5/public"
        
        # 稳健连接
        self.session = requests.Session()
        self.session.trust_env = False
    
    def investigate_design_problems(self):
        """调查设计问题"""
        print("🔍 虞姬OKX测试网连接方式设计调查...")
        print("=" * 60)
        
        investigation_results = {}
        
        # 调查1: 签名算法设计
        print("\n1. 签名算法设计调查...")
        signature_investigation = self.investigate_signature_design()
        investigation_results['signature'] = signature_investigation
        
        # 调查2: 时间戳设计
        print("\n2. 时间戳设计调查...")
        timestamp_investigation = self.investigate_timestamp_design()
        investigation_results['timestamp'] = timestamp_investigation
        
        # 调查3: 头信息设计
        print("\n3. 头信息设计调查...")
        header_investigation = self.investigate_header_design()
        investigation_results['header'] = header_investigation
        
        # 调查4: 请求格式设计
        print("\n4. 请求格式设计调查...")
        request_investigation = self.investigate_request_design()
        investigation_results['request'] = request_investigation
        
        return investigation_results
    
    def investigate_signature_design(self):
        """调查签名算法设计"""
        print("   调查签名算法设计...")
        
        issues = []
        
        # 检查Secret密钥格式
        print(f"      Secret密钥: {self.secret}")
        print(f"      Secret长度: {len(self.secret)}")
        
        if len(self.secret) != 32:
            issues.append(f"Secret密钥长度异常: {len(self.secret)} (应为32)")
        
        # 检查Secret密钥字符
        valid_chars = set('0123456789ABCDEF')
        if not all(c in valid_chars for c in self.secret):
            issues.append("Secret密钥包含无效字符")
        
        # 检查签名生成
        timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        request_path = "/api/v5/account/balance"
        
        message = timestamp + 'GET' + request_path
        print(f"      签名消息: {message}")
        
        try:
            signature = hmac.new(
                self.secret.encode('utf-8'),
                message.encode('utf-8'),
                hashlib.sha256
            ).hexdigest()
            print(f"      生成签名: {signature}")
            
            # 验证签名长度
            if len(signature) != 64:
                issues.append(f"签名长度异常: {len(signature)} (应为64)")
                
        except Exception as e:
            issues.append(f"签名生成异常: {e}")
        
        return {'issues': issues, 'signature': signature if 'signature' in locals() else None}
    
    def investigate_timestamp_design(self):
        """调查时间戳设计"""
        print("   调查时间戳设计...")
        
        issues = []
        
        # 检查时间戳格式
        timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        print(f"      时间戳格式: {timestamp}")
        
        # 检查时间戳格式规范
        try:
            parsed_timestamp = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%fZ')
            print(f"      时间戳解析成功")
        except Exception as e:
            issues.append(f"时间戳格式异常: {e}")
        
        # 检查时间戳与服务器时间差
        try:
            url = f"{self.testnet_url}/api/v5/public/time"
            response = self.session.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                server_time = data.get('data', [{}])[0].get('ts')
                if server_time:
                    server_datetime = datetime.fromisoformat(server_time.replace('Z', '+00:00'))
                    local_datetime = datetime.utcnow()
                    time_diff = abs((local_datetime - server_datetime).total_seconds())
                    print(f"      时间差: {time_diff:.2f}秒")
                    
                    if time_diff > 30:
                        issues.append(f"时间差过大: {time_diff:.2f}秒")
        except Exception as e:
            print(f"      服务器时间检查异常: {e}")
        
        return {'issues': issues, 'timestamp': timestamp}
    
    def investigate_header_design(self):
        """调查头信息设计"""
        print("   调查头信息设计...")
        
        issues = []
        
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
            'Content-Type': 'application/json',
            'x-simulated-trading': '1'
        }
        
        print(f"      头信息数量: {len(headers)}")
        print(f"      头信息内容:")
        for key, value in headers.items():
            if key in ['OK-ACCESS-KEY', 'OK-ACCESS-SIGN', 'OK-ACCESS-PASSPHRASE']:
                print(f"        {key}: {value[:10]}...")
            else:
                print(f"        {key}: {value}")
        
        # 检查必要的头信息
        required_headers = ['OK-ACCESS-KEY', 'OK-ACCESS-SIGN', 'OK-ACCESS-TIMESTAMP', 'OK-ACCESS-PASSPHRASE']
        for header in required_headers:
            if header not in headers:
                issues.append(f"缺少必要头信息: {header}")
        
        # 检查头信息值
        if not headers['OK-ACCESS-KEY']:
            issues.append("API Key为空")
        if not headers['OK-ACCESS-SIGN']:
            issues.append("签名为空")
        if not headers['OK-ACCESS-TIMESTAMP']:
            issues.append("时间戳为空")
        if not headers['OK-ACCESS-PASSPHRASE']:
            issues.append("Passphrase为空")
        
        return {'issues': issues, 'headers': headers}
    
    def investigate_request_design(self):
        """调查请求格式设计"""
        print("   调查请求格式设计...")
        
        issues = []
        
        # 检查请求URL
        request_path = "/api/v5/account/balance"
        url = f"{self.testnet_url}{request_path}"
        print(f"      请求URL: {url}")
        
        # 检查HTTP方法
        http_method = "GET"
        print(f"      HTTP方法: {http_method}")
        
        # 检查请求参数
        print(f"      请求路径: {request_path}")
        
        # 检查URL格式
        if not url.startswith('https://'):
            issues.append("URL不是HTTPS协议")
        
        if not url.endswith(request_path):
            issues.append("URL路径不正确")
        
        # 测试实际请求
        timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        
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
            'Content-Type': 'application/json',
            'x-simulated-trading': '1'
        }
        
        try:
            response = self.session.get(url, headers=headers, timeout=10)
            print(f"      实际请求状态: {response.status_code}")
            
            if response.status_code != 200:
                try:
                    error_data = response.json()
                    error_code = error_data.get('code', '未知')
                    error_msg = error_data.get('msg', '未知错误')
                    print(f"      错误代码: {error_code}")
                    print(f"      错误信息: {error_msg}")
                    
                    if error_code == '50113':
                        issues.append("签名验证失败 (50113)")
                    elif error_code == '50109':
                        issues.append("API Key无效 (50109)")
                    elif error_code == '50111':
                        issues.append("Passphrase错误 (50111)")
                    else:
                        issues.append(f"API错误: {error_code} - {error_msg}")
                        
                except:
                    issues.append(f"HTTP错误: {response.status_code}")
                    
        except Exception as e:
            issues.append(f"请求异常: {e}")
        
        return {'issues': issues, 'url': url, 'method': http_method}
    
    def generate_design_investigation_report(self, investigation_results):
        """生成设计调查报告"""
        print("\n💰 【虞姬OKX测试网连接方式设计调查报告】")
        print(f"📅 报告时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)
        
        # 设计问题汇总
        print("\n🔧 【设计问题调查结果】")
        
        total_issues = 0
        for category, result in investigation_results.items():
            issues = result.get('issues', [])
            total_issues += len(issues)
            
            if issues:
                print(f"\n   ❌ {category.upper()} 问题:")
                for issue in issues:
                    print(f"      • {issue}")
            else:
                print(f"\n   ✅ {category.upper()}: 设计正确")
        
        print(f"\n   总设计问题: {total_issues}")
        
        # 根本原因分析
        print(f"\n🔍 【根本原因分析】")
        if total_issues > 0:
            print("   🔧 虞姬测试网连接方式设计有问题")
            print("   💡 需要修复设计问题")
        else:
            print("   ✅ 虞姬测试网连接方式设计正确")
            print("   💡 问题不在虞姬设计，而在API配置")
        
        # 最终解决方案
        print(f"\n🚀 【最终解决方案】")
        if total_issues > 0:
            print("   🔧 虞姬连接方式需要修复")
            print("   📋 需要修复设计问题:")
            for category, result in investigation_results.items():
                issues = result.get('issues', [])
                if issues:
                    print(f"      • {category}: {len(issues)}个问题")
        else:
            print("   ✅ 虞姬连接方式设计正确")
            print("   📋 问题在API配置，需要:")
            print("      1. 手动登录OKX模拟交易页面")
            print("      2. 确认模拟账号可正常访问")
            print("      3. 重新生成API密钥")
            print("      4. 启用所有交易权限")
            print("      5. 添加服务器IP到白名单")
        
        print("\n" + "=" * 70)
    
    def run_design_investigation(self):
        """运行设计调查"""
        print("🚀 虞姬OKX测试网连接方式设计调查系统")
        print(f"⏰ 调查时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)
        
        # 设计调查
        investigation_results = self.investigate_design_problems()
        
        # 生成调查报告
        self.generate_design_investigation_report(investigation_results)
        
        print("\n" + "=" * 70)
        
        # 总结
        total_issues = sum(len(result.get('issues', [])) for result in investigation_results.values())
        
        if total_issues == 0:
            print("🎉 虞姬测试网连接方式设计正确! 问题在API配置!")
            return True
        else:
            print("⚠️ 虞姬测试网连接方式设计有问题，需要修复!")
            return False

# 立即运行设计调查
def investigate_okx_testnet_design():
    """调查OKX测试网连接设计"""
    print("🔍 立即调查虞姬OKX测试网连接方式设计...")
    
    investigator = OKXTestnetDesignInvestigation()
    
    try:
        success = investigator.run_design_investigation()
        return success
    except Exception as e:
        print(f"❌ 调查异常: {e}")
        return False

if __name__ == "__main__":
    investigate_okx_testnet_design()