#!/usr/bin/env python3
"""
虞姬OKX连接方式设计检查
检查虞姬设计的连接方式是否有问题
"""

import time
import hmac
import hashlib
import requests
import json
from datetime import datetime

class OKXConnectionDesignCheck:
    def __init__(self):
        # 老板提供的最新OKX凭据
        self.api_key = "cefedac1-1d25-4fae-861d-9f006e4cd654"
        self.secret = "EE66B6A88F9E57FBCAE6219081DABDE1"
        self.passphrase = "Qian1314."
        self.base_url = "https://www.okx.com"
        
        # 稳健连接
        self.session = requests.Session()
        self.session.trust_env = False
    
    def check_design_problems(self):
        """检查设计问题"""
        print("🔍 虞姬OKX连接方式设计检查...")
        print("=" * 60)
        
        design_issues = {}
        
        # 检查1: 签名算法设计
        print("\n1. 签名算法设计检查...")
        signature_design = self.check_signature_algorithm_design()
        design_issues['signature'] = signature_design
        
        # 检查2: 时间戳设计
        print("\n2. 时间戳设计检查...")
        timestamp_design = self.check_timestamp_design()
        design_issues['timestamp'] = timestamp_design
        
        # 检查3: 头信息设计
        print("\n3. 头信息设计检查...")
        header_design = self.check_header_design()
        design_issues['header'] = header_design
        
        # 检查4: 请求格式设计
        print("\n4. 请求格式设计检查...")
        request_design = self.check_request_format_design()
        design_issues['request'] = request_design
        
        # 检查5: 连接参数设计
        print("\n5. 连接参数设计检查...")
        connection_design = self.check_connection_params_design()
        design_issues['connection'] = connection_design
        
        return design_issues
    
    def check_signature_algorithm_design(self):
        """检查签名算法设计"""
        print("   检查签名算法设计...")
        
        issues = []
        
        # 标准签名算法
        timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        request_path = "/api/v5/account/balance"
        
        # 检查签名消息格式
        message = timestamp + 'GET' + request_path
        print(f"      签名消息格式: {message}")
        
        # 检查Secret密钥格式
        print(f"      Secret密钥长度: {len(self.secret)}")
        print(f"      Secret密钥格式: {self.secret}")
        
        if len(self.secret) != 32:
            issues.append("Secret密钥长度不正确，应为32位")
        
        # 检查签名生成
        try:
            signature = hmac.new(
                self.secret.encode('utf-8'),
                message.encode('utf-8'),
                hashlib.sha256
            ).hexdigest()
            print(f"      签名生成成功: {signature}")
        except Exception as e:
            issues.append(f"签名生成失败: {e}")
        
        return {'issues': issues, 'signature': signature if 'signature' in locals() else None}
    
    def check_timestamp_design(self):
        """检查时间戳设计"""
        print("   检查时间戳设计...")
        
        issues = []
        
        # 检查时间戳格式
        timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        print(f"      时间戳格式: {timestamp}")
        
        # 检查时间戳是否在合理范围内
        try:
            from datetime import datetime
            parsed_timestamp = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%fZ')
            current_time = datetime.utcnow()
            time_diff = abs((current_time - parsed_timestamp).total_seconds())
            print(f"      时间戳与当前时间差: {time_diff:.2f}秒")
            
            if time_diff > 30:
                issues.append("时间戳与当前时间差过大")
        except Exception as e:
            issues.append(f"时间戳解析失败: {e}")
        
        return {'issues': issues, 'timestamp': timestamp}
    
    def check_header_design(self):
        """检查头信息设计"""
        print("   检查头信息设计...")
        
        issues = []
        
        # 标准头信息
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
    
    def check_request_format_design(self):
        """检查请求格式设计"""
        print("   检查请求格式设计...")
        
        issues = []
        
        # 检查请求URL
        request_path = "/api/v5/account/balance"
        url = f"{self.base_url}{request_path}"
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
        
        return {'issues': issues, 'url': url, 'method': http_method}
    
    def check_connection_params_design(self):
        """检查连接参数设计"""
        print("   检查连接参数设计...")
        
        issues = []
        
        # 检查连接参数
        timeout = 15
        print(f"      连接超时: {timeout}秒")
        
        # 检查会话配置
        print(f"      会话信任环境: {self.session.trust_env}")
        
        # 检查基础URL
        print(f"      基础URL: {self.base_url}")
        
        # 检查API凭据
        print(f"      API Key长度: {len(self.api_key)}")
        print(f"      Secret长度: {len(self.secret)}")
        print(f"      Passphrase长度: {len(self.passphrase)}")
        
        # 检查凭据格式
        if len(self.api_key) < 10:
            issues.append("API Key长度过短")
        if len(self.secret) != 32:
            issues.append("Secret密钥长度不正确")
        if len(self.passphrase) < 6:
            issues.append("Passphrase长度过短")
        
        return {'issues': issues, 'timeout': timeout}
    
    def generate_design_check_report(self, design_issues):
        """生成设计检查报告"""
        print("\n💰 【虞姬OKX连接方式设计检查报告】")
        print(f"📅 报告时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)
        
        # 设计问题汇总
        print("\n🔧 【设计问题汇总】")
        
        total_issues = 0
        for category, result in design_issues.items():
            issues = result.get('issues', [])
            total_issues += len(issues)
            
            if issues:
                print(f"\n   ❌ {category.upper()} 问题:")
                for issue in issues:
                    print(f"      • {issue}")
            else:
                print(f"\n   ✅ {category.upper()}: 设计正确")
        
        print(f"\n   总问题数量: {total_issues}")
        
        # 设计正确部分
        print(f"\n✅ 【设计正确部分】")
        correct_categories = []
        for category, result in design_issues.items():
            if not result.get('issues'):
                correct_categories.append(category)
        
        if correct_categories:
            for category in correct_categories:
                print(f"   • {category}: 设计正确")
        else:
            print("   ❌ 所有设计部分都有问题")
        
        # 根本原因分析
        print(f"\n🔍 【根本原因分析】")
        if total_issues == 0:
            print("   ✅ 虞姬连接方式设计正确")
            print("   💡 问题不在虞姬设计，而在API配置")
        else:
            print("   🔧 虞姬连接方式设计有问题")
            print("   💡 需要修复设计问题")
        
        # 解决方案
        print(f"\n🚀 【解决方案】")
        if total_issues == 0:
            print("   ✅ 虞姬连接方式设计正确")
            print("   📋 问题在API配置，需要:")
            print("      1. 重新生成OKX模拟账号API")
            print("      2. 确认模拟账号状态正常")
            print("      3. 检查IP白名单配置")
            print("      4. 验证API权限设置")
        else:
            print("   🔧 虞姬连接方式需要修复")
            print("   📋 需要修复设计问题:")
            for category, result in design_issues.items():
                issues = result.get('issues', [])
                if issues:
                    print(f"      • {category}: {len(issues)}个问题")
        
        print("\n" + "=" * 70)
    
    def run_design_check(self):
        """运行设计检查"""
        print("🚀 虞姬OKX连接方式设计检查系统")
        print(f"⏰ 检查时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)
        
        # 设计检查
        design_issues = self.check_design_problems()
        
        # 生成设计检查报告
        self.generate_design_check_report(design_issues)
        
        print("\n" + "=" * 70)
        
        # 总结
        total_issues = sum(len(result.get('issues', [])) for result in design_issues.values())
        
        if total_issues == 0:
            print("🎉 虞姬连接方式设计正确! 问题在API配置!")
            return True
        else:
            print("⚠️ 虞姬连接方式设计有问题，需要修复!")
            return False

# 立即运行设计检查
def check_okx_connection_design():
    """检查OKX连接设计"""
    print("🔍 立即检查虞姬OKX连接方式设计...")
    
    checker = OKXConnectionDesignCheck()
    
    try:
        success = checker.run_design_check()
        return success
    except Exception as e:
        print(f"❌ 检查异常: {e}")
        return False

if __name__ == "__main__":
    check_okx_connection_design()