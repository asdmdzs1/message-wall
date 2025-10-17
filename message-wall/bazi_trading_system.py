#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
天干八字量化交易系统
基于传统命理学的量化交易策略
"""

import numpy as np
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

class BaziCalculator:
    """天干八字计算器"""
    
    def __init__(self):
        # 天干地支定义
        self.tiangan = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
        self.dizhi = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
        
        # 五行对应关系
        self.wuxing_tiangan = {
            '甲': '木', '乙': '木',
            '丙': '火', '丁': '火', 
            '戊': '土', '己': '土',
            '庚': '金', '辛': '金',
            '壬': '水', '癸': '水'
        }
        
        self.wuxing_dizhi = {
            '子': '水', '丑': '土', '寅': '木', '卯': '木',
            '辰': '土', '巳': '火', '午': '火', '未': '土',
            '申': '金', '酉': '金', '戌': '土', '亥': '水'
        }
        
        # 五行相生相克关系
        self.wuxing_shengke = {
            '木': {'生': '火', '克': '土', '被生': '水', '被克': '金'},
            '火': {'生': '土', '克': '金', '被生': '木', '被克': '水'},
            '土': {'生': '金', '克': '水', '被生': '火', '被克': '木'},
            '金': {'生': '水', '克': '木', '被生': '土', '被克': '火'},
            '水': {'生': '木', '克': '火', '被生': '金', '被克': '土'}
        }
    
    def get_tiangan_dizhi(self, year: int) -> Tuple[str, str]:
        """根据年份获取天干地支"""
        # 以1900年为甲子年作为基准
        base_year = 1900
        offset = (year - base_year) % 60
        
        tiangan_index = offset % 10
        dizhi_index = offset % 12
        
        return self.tiangan[tiangan_index], self.dizhi[dizhi_index]
    
    def calculate_bazi(self, date: datetime) -> Dict[str, str]:
        """计算指定日期的八字"""
        year_tg, year_dz = self.get_tiangan_dizhi(date.year)
        
        # 简化计算，实际八字需要更复杂的历法转换
        month_tg = self.tiangan[(date.month - 1) % 10]
        month_dz = self.dizhi[(date.month - 1) % 12]
        
        day_tg = self.tiangan[(date.day - 1) % 10]
        day_dz = self.dizhi[(date.day - 1) % 12]
        
        hour_tg = self.tiangan[(date.hour // 2) % 10]
        hour_dz = self.dizhi[(date.hour // 2) % 12]
        
        return {
            'year': f"{year_tg}{year_dz}",
            'month': f"{month_tg}{month_dz}",
            'day': f"{day_tg}{day_dz}",
            'hour': f"{hour_tg}{hour_dz}",
            'year_tg': year_tg, 'year_dz': year_dz,
            'month_tg': month_tg, 'month_dz': month_dz,
            'day_tg': day_tg, 'day_dz': day_dz,
            'hour_tg': hour_tg, 'hour_dz': hour_dz
        }
    
    def analyze_wuxing_strength(self, bazi: Dict[str, str]) -> Dict[str, int]:
        """分析五行强弱"""
        wuxing_count = {'木': 0, '火': 0, '土': 0, '金': 0, '水': 0}
        
        # 统计天干五行
        for key in ['year_tg', 'month_tg', 'day_tg', 'hour_tg']:
            if key in bazi:
                wuxing = self.wuxing_tiangan.get(bazi[key], '')
                if wuxing:
                    wuxing_count[wuxing] += 1
        
        # 统计地支五行
        for key in ['year_dz', 'month_dz', 'day_dz', 'hour_dz']:
            if key in bazi:
                wuxing = self.wuxing_dizhi.get(bazi[key], '')
                if wuxing:
                    wuxing_count[wuxing] += 1
        
        return wuxing_count
    
    def get_wuxing_relationship(self, wuxing1: str, wuxing2: str) -> str:
        """获取五行关系"""
        if wuxing1 == wuxing2:
            return '同'
        elif self.wuxing_shengke[wuxing1]['生'] == wuxing2:
            return '生'
        elif self.wuxing_shengke[wuxing1]['克'] == wuxing2:
            return '克'
        elif self.wuxing_shengke[wuxing1]['被生'] == wuxing2:
            return '被生'
        elif self.wuxing_shengke[wuxing1]['被克'] == wuxing2:
            return '被克'
        else:
            return '无'


class TradingStrategy:
    """基于天干八字的交易策略"""
    
    def __init__(self, bazi_calculator: BaziCalculator):
        self.bazi_calc = bazi_calculator
        
    def get_trading_signal(self, symbol: str, date: datetime, price_data: pd.DataFrame) -> Dict[str, any]:
        """根据八字分析获取交易信号"""
        
        # 计算当前日期的八字
        current_bazi = self.bazi_calc.calculate_bazi(date)
        current_wuxing = self.bazi_calc.analyze_wuxing_strength(current_bazi)
        
        # 获取品种的"八字"（基于上市日期或重要日期）
        # 这里简化为使用最近的一个交易日
        symbol_bazi = self.bazi_calc.calculate_bazi(date - timedelta(days=1))
        symbol_wuxing = self.bazi_calc.analyze_wuxing_strength(symbol_bazi)
        
        # 分析五行关系
        signal_strength = 0
        signal_reason = []
        
        # 根据五行相生相克关系判断
        for wuxing in ['木', '火', '土', '金', '水']:
            current_strength = current_wuxing.get(wuxing, 0)
            symbol_strength = symbol_wuxing.get(wuxing, 0)
            
            # 如果当前市场五行强于品种五行，且五行相生，则看涨
            if current_strength > symbol_strength:
                for target_wuxing in ['木', '火', '土', '金', '水']:
                    if wuxing != target_wuxing:
                        relationship = self.bazi_calc.get_wuxing_relationship(wuxing, target_wuxing)
                        if relationship == '生' and symbol_wuxing.get(target_wuxing, 0) > 0:
                            signal_strength += 1
                            signal_reason.append(f"{wuxing}生{target_wuxing}")
        
        # 生成交易信号
        if signal_strength >= 3:
            signal = 'BUY'
            confidence = min(signal_strength / 5.0, 1.0)
        elif signal_strength <= -3:
            signal = 'SELL'
            confidence = min(abs(signal_strength) / 5.0, 1.0)
        else:
            signal = 'HOLD'
            confidence = 0.5
        
        return {
            'signal': signal,
            'confidence': confidence,
            'strength': signal_strength,
            'reason': signal_reason,
            'current_bazi': current_bazi,
            'current_wuxing': current_wuxing,
            'symbol_wuxing': symbol_wuxing
        }


class DataProcessor:
    """数据处理模块"""
    
    def __init__(self):
        self.bazi_calc = BaziCalculator()
    
    def get_stock_data(self, symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
        """获取股票数据"""
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(start=start_date, end=end_date)
            return data
        except Exception as e:
            print(f"获取 {symbol} 数据失败: {e}")
            return pd.DataFrame()
    
    def get_multiple_symbols_data(self, symbols: List[str], start_date: str, end_date: str) -> Dict[str, pd.DataFrame]:
        """获取多个品种的数据"""
        data_dict = {}
        for symbol in symbols:
            data = self.get_stock_data(symbol, start_date, end_date)
            if not data.empty:
                data_dict[symbol] = data
        return data_dict
    
    def calculate_technical_indicators(self, data: pd.DataFrame) -> pd.DataFrame:
        """计算技术指标"""
        df = data.copy()
        
        # 移动平均线
        df['MA5'] = df['Close'].rolling(window=5).mean()
        df['MA20'] = df['Close'].rolling(window=20).mean()
        df['MA50'] = df['Close'].rolling(window=50).mean()
        
        # RSI
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))
        
        # 布林带
        df['BB_middle'] = df['Close'].rolling(window=20).mean()
        bb_std = df['Close'].rolling(window=20).std()
        df['BB_upper'] = df['BB_middle'] + (bb_std * 2)
        df['BB_lower'] = df['BB_middle'] - (bb_std * 2)
        
        return df


class BacktestingEngine:
    """回测引擎"""
    
    def __init__(self, initial_capital: float = 100000):
        self.initial_capital = initial_capital
        self.strategy = TradingStrategy(BaziCalculator())
        self.data_processor = DataProcessor()
    
    def run_backtest(self, symbols: List[str], start_date: str, end_date: str) -> Dict[str, any]:
        """运行回测"""
        
        # 获取数据
        data_dict = self.data_processor.get_multiple_symbols_data(symbols, start_date, end_date)
        
        if not data_dict:
            return {'error': '无法获取数据'}
        
        # 初始化回测结果
        results = {
            'portfolio_value': [self.initial_capital],
            'returns': [0],
            'positions': {},
            'trades': [],
            'daily_returns': [],
            'dates': []
        }
        
        current_capital = self.initial_capital
        positions = {}
        
        # 按日期遍历数据
        all_dates = set()
        for symbol, data in data_dict.items():
            all_dates.update(data.index.date)
        
        all_dates = sorted(list(all_dates))
        
        for date in all_dates:
            daily_returns = 0
            date_obj = datetime.combine(date, datetime.min.time())
            
            # 为每个品种生成交易信号
            for symbol in symbols:
                if symbol not in data_dict:
                    continue
                    
                data = data_dict[symbol]
                if date not in data.index.date:
                    continue
                
                current_price = data.loc[data.index.date == date, 'Close'].iloc[0]
                
                # 获取交易信号
                signal_info = self.strategy.get_trading_signal(symbol, date_obj, data)
                
                # 执行交易逻辑
                if signal_info['signal'] == 'BUY' and symbol not in positions:
                    # 买入
                    shares = int(current_capital * signal_info['confidence'] * 0.1 / current_price)
                    if shares > 0:
                        cost = shares * current_price
                        positions[symbol] = {
                            'shares': shares,
                            'entry_price': current_price,
                            'entry_date': date
                        }
                        current_capital -= cost
                        results['trades'].append({
                            'date': date,
                            'symbol': symbol,
                            'action': 'BUY',
                            'shares': shares,
                            'price': current_price,
                            'confidence': signal_info['confidence']
                        })
                
                elif signal_info['signal'] == 'SELL' and symbol in positions:
                    # 卖出
                    position = positions[symbol]
                    proceeds = position['shares'] * current_price
                    current_capital += proceeds
                    daily_returns += (current_price - position['entry_price']) / position['entry_price']
                    
                    results['trades'].append({
                        'date': date,
                        'symbol': symbol,
                        'action': 'SELL',
                        'shares': position['shares'],
                        'price': current_price,
                        'confidence': signal_info['confidence']
                    })
                    
                    del positions[symbol]
                
                # 更新持仓市值
                if symbol in positions:
                    position = positions[symbol]
                    position_value = position['shares'] * current_price
                    daily_returns += (current_price - position['entry_price']) / position['entry_price']
            
            # 计算组合总价值
            total_position_value = sum(pos['shares'] * data_dict[sym].loc[data_dict[sym].index.date == date, 'Close'].iloc[0] 
                                     for sym, pos in positions.items() 
                                     if date in data_dict[sym].index.date)
            
            portfolio_value = current_capital + total_position_value
            results['portfolio_value'].append(portfolio_value)
            results['returns'].append((portfolio_value - results['portfolio_value'][-2]) / results['portfolio_value'][-2] if len(results['portfolio_value']) > 1 else 0)
            results['daily_returns'].append(daily_returns)
            results['dates'].append(date)
        
        results['positions'] = positions
        return results
    
    def calculate_metrics(self, results: Dict[str, any]) -> Dict[str, float]:
        """计算回测指标"""
        if not results.get('portfolio_value'):
            return {}
        
        portfolio_values = np.array(results['portfolio_value'])
        returns = np.array(results['returns'][1:])  # 排除第一个0
        
        # 基本指标
        total_return = (portfolio_values[-1] - portfolio_values[0]) / portfolio_values[0]
        
        # 年化收益率
        days = len(portfolio_values)
        annual_return = (1 + total_return) ** (365 / days) - 1
        
        # 波动率
        volatility = np.std(returns) * np.sqrt(252)
        
        # 夏普比率（假设无风险利率为3%）
        risk_free_rate = 0.03
        sharpe_ratio = (annual_return - risk_free_rate) / volatility if volatility > 0 else 0
        
        # 最大回撤
        peak = np.maximum.accumulate(portfolio_values)
        drawdown = (portfolio_values - peak) / peak
        max_drawdown = np.min(drawdown)
        
        # 胜率
        winning_trades = len([r for r in returns if r > 0])
        win_rate = winning_trades / len(returns) if returns.size > 0 else 0
        
        return {
            '总收益率': total_return,
            '年化收益率': annual_return,
            '波动率': volatility,
            '夏普比率': sharpe_ratio,
            '最大回撤': max_drawdown,
            '胜率': win_rate,
            '交易次数': len(results.get('trades', []))
        }


class Visualization:
    """可视化模块"""
    
    @staticmethod
    def plot_portfolio_performance(results: Dict[str, any], metrics: Dict[str, float]):
        """绘制组合表现图表"""
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('天干八字量化交易系统回测结果', fontsize=16)
        
        # 组合价值曲线
        # 确保数据长度一致
        min_len = min(len(results['dates']), len(results['portfolio_value']))
        dates = results['dates'][:min_len]
        values = results['portfolio_value'][:min_len]
        
        if dates and values:
            axes[0, 0].plot(dates, values)
            axes[0, 0].set_title('组合价值变化')
            axes[0, 0].set_ylabel('组合价值')
            axes[0, 0].grid(True)
        else:
            axes[0, 0].text(0.5, 0.5, '无数据', ha='center', va='center', transform=axes[0, 0].transAxes)
            axes[0, 0].set_title('组合价值变化')
        
        # 收益率分布
        returns = np.array(results['returns'][1:]) if len(results['returns']) > 1 else np.array([0])
        if len(returns) > 0 and np.any(returns != 0):
            axes[0, 1].hist(returns, bins=min(30, len(returns)), alpha=0.7)
            axes[0, 1].set_title('收益率分布')
            axes[0, 1].set_xlabel('日收益率')
            axes[0, 1].set_ylabel('频次')
            axes[0, 1].grid(True)
        else:
            axes[0, 1].text(0.5, 0.5, '无收益率数据', ha='center', va='center', transform=axes[0, 1].transAxes)
            axes[0, 1].set_title('收益率分布')
        
        # 回撤分析
        if len(values) > 0:
            portfolio_values = np.array(values)
            peak = np.maximum.accumulate(portfolio_values)
            drawdown = (portfolio_values - peak) / peak
            
            axes[1, 0].fill_between(dates, drawdown, 0, alpha=0.3, color='red')
            axes[1, 0].set_title('回撤分析')
            axes[1, 0].set_ylabel('回撤比例')
            axes[1, 0].grid(True)
        else:
            axes[1, 0].text(0.5, 0.5, '无数据', ha='center', va='center', transform=axes[1, 0].transAxes)
            axes[1, 0].set_title('回撤分析')
        
        # 关键指标
        metrics_text = '\n'.join([f'{k}: {v:.4f}' for k, v in metrics.items()])
        axes[1, 1].text(0.1, 0.5, metrics_text, transform=axes[1, 1].transAxes, 
                        fontsize=12, verticalalignment='center')
        axes[1, 1].set_title('关键指标')
        axes[1, 1].axis('off')
        
        plt.tight_layout()
        plt.show()
    
    @staticmethod
    def plot_bazi_analysis(symbol: str, date: datetime, signal_info: Dict[str, any]):
        """绘制八字分析图"""
        
        fig, axes = plt.subplots(1, 2, figsize=(12, 5))
        
        # 五行强度
        current_wuxing = signal_info['current_wuxing']
        symbol_wuxing = signal_info['symbol_wuxing']
        
        wuxing_names = list(current_wuxing.keys())
        current_values = list(current_wuxing.values())
        symbol_values = list(symbol_wuxing.values())
        
        x = np.arange(len(wuxing_names))
        width = 0.35
        
        axes[0].bar(x - width/2, current_values, width, label='当前市场', alpha=0.7)
        axes[0].bar(x + width/2, symbol_values, width, label='品种', alpha=0.7)
        axes[0].set_xlabel('五行')
        axes[0].set_ylabel('强度')
        axes[0].set_title(f'{symbol} 五行强度对比')
        axes[0].set_xticks(x)
        axes[0].set_xticklabels(wuxing_names)
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)
        
        # 交易信号
        signal = signal_info['signal']
        confidence = signal_info['confidence']
        strength = signal_info['strength']
        
        signal_colors = {'BUY': 'green', 'SELL': 'red', 'HOLD': 'gray'}
        axes[1].bar(['交易信号'], [confidence], color=signal_colors.get(signal, 'gray'), alpha=0.7)
        axes[1].set_title(f'交易信号: {signal} (强度: {strength})')
        axes[1].set_ylabel('置信度')
        axes[1].set_ylim(0, 1)
        
        plt.tight_layout()
        plt.show()


def main():
    """主函数"""
    print("天干八字量化交易系统")
    print("=" * 50)
    
    # 初始化系统组件
    bazi_calc = BaziCalculator()
    strategy = TradingStrategy(bazi_calc)
    backtester = BacktestingEngine()
    
    # 测试品种
    symbols = ['AAPL', 'MSFT', 'GOOGL', 'TSLA', 'NVDA']
    start_date = '2023-01-01'
    end_date = '2024-01-01'
    
    print(f"回测品种: {symbols}")
    print(f"回测期间: {start_date} 至 {end_date}")
    print("开始回测...")
    
    # 运行回测
    results = backtester.run_backtest(symbols, start_date, end_date)
    
    if 'error' in results:
        print(f"回测失败: {results['error']}")
        return
    
    # 计算指标
    metrics = backtester.calculate_metrics(results)
    
    # 显示结果
    print("\n回测结果:")
    print("-" * 30)
    for key, value in metrics.items():
        if isinstance(value, float):
            print(f"{key}: {value:.4f}")
        else:
            print(f"{key}: {value}")
    
    # 显示交易记录
    trades = results.get('trades', [])
    if trades:
        print(f"\n交易记录 (共 {len(trades)} 笔):")
        print("-" * 50)
        for trade in trades[-10:]:  # 显示最近10笔交易
            print(f"{trade['date']} {trade['action']} {trade['symbol']} "
                  f"{trade['shares']}股 @ ${trade['price']:.2f} "
                  f"(置信度: {trade['confidence']:.3f})")
    
    # 绘制图表
    viz = Visualization()
    viz.plot_portfolio_performance(results, metrics)
    
    # 示例八字分析
    test_date = datetime(2023, 6, 15)
    test_symbol = 'AAPL'
    print(f"\n{test_symbol} 在 {test_date.strftime('%Y-%m-%d')} 的八字分析:")
    print("-" * 40)
    
    # 获取测试数据
    data_processor = DataProcessor()
    test_data = data_processor.get_stock_data(test_symbol, '2023-01-01', '2023-12-31')
    
    if not test_data.empty:
        signal_info = strategy.get_trading_signal(test_symbol, test_date, test_data)
        
        print(f"八字: {signal_info['current_bazi']['year']} {signal_info['current_bazi']['month']} "
              f"{signal_info['current_bazi']['day']} {signal_info['current_bazi']['hour']}")
        print(f"当前市场五行: {signal_info['current_wuxing']}")
        print(f"品种五行: {signal_info['symbol_wuxing']}")
        print(f"交易信号: {signal_info['signal']}")
        print(f"置信度: {signal_info['confidence']:.3f}")
        print(f"信号强度: {signal_info['strength']}")
        print(f"信号原因: {', '.join(signal_info['reason'])}")
        
        # 绘制八字分析图
        viz.plot_bazi_analysis(test_symbol, test_date, signal_info)


if __name__ == "__main__":
    main()
