#!/usr/bin/env python3
"""安装交易依赖包"""

import subprocess
import sys

def install_package(package):
    """安装Python包"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✓ 已安装: {package}")
        return True
    except subprocess.CalledProcessError:
        print(f"✗ 安装失败: {package}")
        return False

def main():
    packages = [
        'ccxt',
        'pandas',
        'numpy',
        'requests',
        'websocket-client'
    ]
    
    print("开始安装交易依赖包...")
    
    success_count = 0
    for package in packages:
        if install_package(package):
            success_count += 1
    
    print(f"\n安装完成: {success_count}/{len(packages)} 个包安装成功")
    
    if success_count == len(packages):
        print("✓ 所有依赖包安装成功，可以开始交易了！")
    else:
        print("⚠ 部分依赖包安装失败，请手动安装")

if __name__ == "__main__":
    main()