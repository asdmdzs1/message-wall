#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速启动脚本
"""

import subprocess
import sys
import os

def install_requirements():
    """安装依赖包"""
    print("正在安装依赖包...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("依赖包安装完成！")
        return True
    except subprocess.CalledProcessError:
        print("依赖包安装失败，请手动安装：")
        print("pip install -r requirements.txt")
        return False

def run_demo():
    """运行演示"""
    print("运行天干八字量化交易系统演示...")
    try:
        subprocess.run([sys.executable, "demo.py"])
    except Exception as e:
        print(f"运行演示时出错: {e}")

def main():
    """主函数"""
    print("天干八字量化交易系统 - 快速启动")
    print("=" * 50)
    
    # 检查依赖
    try:
        import numpy
        import pandas
        import yfinance
        import matplotlib
        print("所有依赖包已安装")
    except ImportError:
        print("缺少依赖包，正在安装...")
        if not install_requirements():
            return
    
    # 运行演示
    run_demo()
    
    print("\n" + "=" * 50)
    print("要运行完整回测，请执行:")
    print("python bazi_trading_system.py")
    print("=" * 50)

if __name__ == "__main__":
    main()
