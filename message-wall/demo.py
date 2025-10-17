#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
天干八字量化交易系统演示脚本
简化版本，展示核心功能
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from bazi_trading_system import BaziCalculator, TradingStrategy, DataProcessor
from datetime import datetime, timedelta
import pandas as pd

def demo_bazi_calculation():
    """演示八字计算功能"""
    print("=" * 60)
    print("天干八字计算演示")
    print("=" * 60)
    
    bazi_calc = BaziCalculator()
    
    # 测试不同日期的八字
    test_dates = [
        datetime(2023, 1, 1),
        datetime(2023, 6, 15),
        datetime(2024, 1, 1)
    ]
    
    for date in test_dates:
        bazi = bazi_calc.calculate_bazi(date)
        wuxing = bazi_calc.analyze_wuxing_strength(bazi)
        
        print(f"\n日期: {date.strftime('%Y年%m月%d日')}")
        print(f"八字: {bazi['year']} {bazi['month']} {bazi['day']} {bazi['hour']}")
        print(f"五行强度: {wuxing}")
        
        # 分析最强和最弱的五行
        max_wuxing = max(wuxing, key=wuxing.get)
        min_wuxing = min(wuxing, key=wuxing.get)
        print(f"最强五行: {max_wuxing} ({wuxing[max_wuxing]})")
        print(f"最弱五行: {min_wuxing} ({wuxing[min_wuxing]})")
        
        # 五行关系分析
        relationship = bazi_calc.get_wuxing_relationship(max_wuxing, min_wuxing)
        print(f"最强与最弱五行关系: {relationship}")

def demo_trading_signals():
    """演示交易信号生成"""
    print("\n" + "=" * 60)
    print("交易信号生成演示")
    print("=" * 60)
    
    strategy = TradingStrategy(BaziCalculator())
    
    # 模拟一些价格数据
    dates = pd.date_range('2023-01-01', periods=30, freq='D')
    prices = [100 + i * 0.5 + (i % 3 - 1) * 2 for i in range(30)]
    
    mock_data = pd.DataFrame({
        'Close': prices
    }, index=dates)
    
    # 测试不同日期的交易信号
    test_dates = [datetime(2023, 1, 5), datetime(2023, 1, 15), datetime(2023, 1, 25)]
    
    for date in test_dates:
        signal_info = strategy.get_trading_signal('DEMO', date, mock_data)
        
        print(f"\n日期: {date.strftime('%Y-%m-%d')}")
        print(f"交易信号: {signal_info['signal']}")
        print(f"置信度: {signal_info['confidence']:.3f}")
        print(f"信号强度: {signal_info['strength']}")
        print(f"信号原因: {', '.join(signal_info['reason']) if signal_info['reason'] else '无'}")
        print(f"当前市场五行: {signal_info['current_wuxing']}")
        print(f"品种五行: {signal_info['symbol_wuxing']}")

def demo_wuxing_relationships():
    """演示五行关系"""
    print("\n" + "=" * 60)
    print("五行关系演示")
    print("=" * 60)
    
    bazi_calc = BaziCalculator()
    
    wuxing_list = ['木', '火', '土', '金', '水']
    
    print("五行相生相克关系表:")
    print("-" * 40)
    
    for wuxing in wuxing_list:
        relationships = bazi_calc.wuxing_shengke[wuxing]
        print(f"{wuxing}: 生{wuxing_list[wuxing_list.index(relationships['生'])]}, "
              f"克{wuxing_list[wuxing_list.index(relationships['克'])]}, "
              f"被{wuxing_list[wuxing_list.index(relationships['被生'])]}生, "
              f"被{wuxing_list[wuxing_list.index(relationships['被克'])]}克")
    
    print("\n五行关系判断示例:")
    print("-" * 40)
    
    test_pairs = [('木', '火'), ('火', '土'), ('土', '金'), ('金', '水'), ('水', '木'),
                  ('木', '土'), ('火', '金'), ('土', '水'), ('金', '木'), ('水', '火')]
    
    for w1, w2 in test_pairs:
        relationship = bazi_calc.get_wuxing_relationship(w1, w2)
        print(f"{w1} 对 {w2} 的关系: {relationship}")

def demo_data_processing():
    """演示数据处理功能"""
    print("\n" + "=" * 60)
    print("数据处理演示")
    print("=" * 60)
    
    data_processor = DataProcessor()
    
    # 尝试获取真实数据（如果网络可用）
    try:
        print("尝试获取AAPL股票数据...")
        data = data_processor.get_stock_data('AAPL', '2023-01-01', '2023-02-01')
        
        if not data.empty:
            print(f"成功获取数据，共 {len(data)} 条记录")
            print(f"数据列: {list(data.columns)}")
            print(f"日期范围: {data.index[0].date()} 至 {data.index[-1].date()}")
            
            # 计算技术指标
            data_with_indicators = data_processor.calculate_technical_indicators(data)
            print(f"添加技术指标后的列: {list(data_with_indicators.columns)}")
            
            # 显示最后几行数据
            print("\n最后5行数据:")
            print(data_with_indicators.tail())
            
        else:
            print("未能获取到数据")
            
    except Exception as e:
        print(f"获取数据时出错: {e}")
        print("使用模拟数据进行演示...")
        
        # 创建模拟数据
        dates = pd.date_range('2023-01-01', periods=20, freq='D')
        mock_data = pd.DataFrame({
            'Open': [100 + i for i in range(20)],
            'High': [105 + i for i in range(20)],
            'Low': [95 + i for i in range(20)],
            'Close': [102 + i for i in range(20)],
            'Volume': [1000000 + i * 10000 for i in range(20)]
        }, index=dates)
        
        print(f"模拟数据形状: {mock_data.shape}")
        
        # 计算技术指标
        mock_data_with_indicators = data_processor.calculate_technical_indicators(mock_data)
        print(f"添加技术指标后的列: {list(mock_data_with_indicators.columns)}")
        print("\n最后5行数据:")
        print(mock_data_with_indicators.tail())

def main():
    """主演示函数"""
    print("天干八字量化交易系统演示")
    print("本演示将展示系统的核心功能")
    
    # 运行各个演示
    demo_bazi_calculation()
    demo_wuxing_relationships()
    demo_trading_signals()
    demo_data_processing()
    
    print("\n" + "=" * 60)
    print("演示完成！")
    print("=" * 60)
    print("\n要运行完整的回测系统，请执行:")
    print("python bazi_trading_system.py")
    print("\n更多功能请查看README.md文件")

if __name__ == "__main__":
    main()
