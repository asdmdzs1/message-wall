#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
月度涨跌规律分析模块
分析上证指数、黄金、BTC的月度表现规律
"""

import numpy as np
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns
from bazi_trading_system import BaziCalculator
import warnings
warnings.filterwarnings('ignore')

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

class MonthlyPatternAnalyzer:
    """月度规律分析器"""
    
    def __init__(self):
        self.bazi_calc = BaziCalculator()
        
        # 定义各品种的股票代码
        self.symbols = {
            '上证指数': '000001.SS',  # 上证指数
            '黄金': 'GC=F',          # 黄金期货
            'BTC': 'BTC-USD'         # 比特币
        }
        
        # 月份对应的天干地支和五行
        self.month_bazi = {
            1: {'dizhi': '丑', 'wuxing': '土', 'season': '冬季'},
            2: {'dizhi': '寅', 'wuxing': '木', 'season': '春季'},
            3: {'dizhi': '卯', 'wuxing': '木', 'season': '春季'},
            4: {'dizhi': '辰', 'wuxing': '土', 'season': '春季'},
            5: {'dizhi': '巳', 'wuxing': '火', 'season': '夏季'},
            6: {'dizhi': '午', 'wuxing': '火', 'season': '夏季'},
            7: {'dizhi': '未', 'wuxing': '土', 'season': '夏季'},
            8: {'dizhi': '申', 'wuxing': '金', 'season': '秋季'},
            9: {'dizhi': '酉', 'wuxing': '金', 'season': '秋季'},
            10: {'dizhi': '戌', 'wuxing': '土', 'season': '秋季'},
            11: {'dizhi': '亥', 'wuxing': '水', 'season': '冬季'},
            12: {'dizhi': '子', 'wuxing': '水', 'season': '冬季'}
        }
        
        # 各品种的八字特征（从之前的分析中获得）
        self.asset_bazi_features = {
            '上证指数': {'dominant_wuxing': '木', 'nature': '阳性', 'season': '夏季'},
            '黄金': {'dominant_wuxing': '木', 'nature': '阴性', 'season': '冬季'},
            'BTC': {'dominant_wuxing': '木', 'nature': '阳性', 'season': '冬季'}
        }
    
    def get_historical_data(self, symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
        """获取历史数据"""
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(start=start_date, end=end_date)
            return data
        except Exception as e:
            print(f"获取 {symbol} 数据失败: {e}")
            return pd.DataFrame()
    
    def calculate_monthly_returns(self, data: pd.DataFrame) -> pd.DataFrame:
        """计算月度收益率"""
        if data.empty:
            return pd.DataFrame()
        
        # 重采样为月度数据
        monthly_data = data.resample('M').agg({
            'Open': 'first',
            'High': 'max',
            'Low': 'min',
            'Close': 'last',
            'Volume': 'sum'
        }).dropna()
        
        # 计算月度收益率
        monthly_data['Monthly_Return'] = monthly_data['Close'].pct_change()
        
        # 添加月份信息
        monthly_data['Month'] = monthly_data.index.month
        monthly_data['Year'] = monthly_data.index.year
        
        return monthly_data
    
    def analyze_monthly_patterns(self, asset_name: str, years: int = 10) -> dict:
        """分析月度规律"""
        symbol = self.symbols[asset_name]
        
        # 计算日期范围
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=years*365)).strftime('%Y-%m-%d')
        
        print(f"正在分析 {asset_name} 的 {years} 年历史数据...")
        
        # 获取数据
        raw_data = self.get_historical_data(symbol, start_date, end_date)
        
        if raw_data.empty:
            print(f"无法获取 {asset_name} 的数据")
            return {}
        
        # 计算月度收益率
        monthly_data = self.calculate_monthly_returns(raw_data)
        
        if monthly_data.empty:
            print(f"无法计算 {asset_name} 的月度收益率")
            return {}
        
        # 分析月度表现
        monthly_stats = {}
        
        for month in range(1, 13):
            month_data = monthly_data[monthly_data['Month'] == month]
            
            if len(month_data) == 0:
                continue
            
            returns = month_data['Monthly_Return'].dropna()
            
            monthly_stats[month] = {
                'count': len(returns),
                'mean_return': returns.mean(),
                'median_return': returns.median(),
                'std_return': returns.std(),
                'positive_count': (returns > 0).sum(),
                'negative_count': (returns < 0).sum(),
                'win_rate': (returns > 0).mean(),
                'avg_positive': returns[returns > 0].mean() if (returns > 0).any() else 0,
                'avg_negative': returns[returns < 0].mean() if (returns < 0).any() else 0,
                'max_return': returns.max(),
                'min_return': returns.min()
            }
        
        # 获取品种的八字特征
        bazi_features = self.asset_bazi_features.get(asset_name, {})
        
        return {
            'asset_name': asset_name,
            'symbol': symbol,
            'data_period': f"{start_date} 至 {end_date}",
            'total_months': len(monthly_data),
            'monthly_stats': monthly_stats,
            'bazi_features': bazi_features,
            'raw_monthly_data': monthly_data
        }
    
    def correlate_with_bazi(self, monthly_analysis: dict) -> dict:
        """将月度规律与八字分析关联"""
        asset_name = monthly_analysis['asset_name']
        monthly_stats = monthly_analysis['monthly_stats']
        bazi_features = monthly_analysis['bazi_features']
        
        # 获取品种的主导五行
        dominant_wuxing = bazi_features.get('dominant_wuxing', '')
        
        correlation_analysis = {
            'asset_name': asset_name,
            'dominant_wuxing': dominant_wuxing,
            'monthly_correlations': {},
            'seasonal_patterns': {},
            'bazi_predictions': {}
        }
        
        # 分析每个月的表现与五行关系
        for month, stats in monthly_stats.items():
            month_info = self.month_bazi[month]
            month_wuxing = month_info['wuxing']
            month_season = month_info['season']
            
            # 计算五行关系
            if dominant_wuxing:
                relationship = self.bazi_calc.get_wuxing_relationship(dominant_wuxing, month_wuxing)
            else:
                relationship = '无'
            
            # 预测该月表现
            predicted_performance = self._predict_monthly_performance(
                dominant_wuxing, month_wuxing, relationship, stats
            )
            
            correlation_analysis['monthly_correlations'][month] = {
                'month_name': f"{month}月",
                'month_wuxing': month_wuxing,
                'month_season': month_season,
                'relationship': relationship,
                'actual_stats': stats,
                'predicted_performance': predicted_performance
            }
        
        # 分析季节性规律
        seasonal_analysis = self._analyze_seasonal_patterns(monthly_stats, dominant_wuxing)
        correlation_analysis['seasonal_patterns'] = seasonal_analysis
        
        return correlation_analysis
    
    def _predict_monthly_performance(self, dominant_wuxing: str, month_wuxing: str, 
                                   relationship: str, actual_stats: dict) -> dict:
        """预测月度表现"""
        prediction = {
            'expected_return': '中等',
            'expected_volatility': '中等',
            'expected_win_rate': 0.5,
            'confidence': 0.5,
            'reason': ''
        }
        
        if relationship == '同':
            prediction.update({
                'expected_return': '较好',
                'expected_volatility': '较高',
                'expected_win_rate': 0.6,
                'confidence': 0.7,
                'reason': f'{dominant_wuxing}行与{month_wuxing}行相同，应该表现较好'
            })
        elif relationship == '生':
            prediction.update({
                'expected_return': '很好',
                'expected_volatility': '高',
                'expected_win_rate': 0.7,
                'confidence': 0.8,
                'reason': f'{dominant_wuxing}行生{month_wuxing}行，应该表现很好'
            })
        elif relationship == '被生':
            prediction.update({
                'expected_return': '好',
                'expected_volatility': '中等',
                'expected_win_rate': 0.65,
                'confidence': 0.7,
                'reason': f'{month_wuxing}行生{dominant_wuxing}行，应该表现好'
            })
        elif relationship == '克':
            prediction.update({
                'expected_return': '较差',
                'expected_volatility': '高',
                'expected_win_rate': 0.4,
                'confidence': 0.6,
                'reason': f'{dominant_wuxing}行克{month_wuxing}行，可能表现较差'
            })
        elif relationship == '被克':
            prediction.update({
                'expected_return': '差',
                'expected_volatility': '高',
                'expected_win_rate': 0.3,
                'confidence': 0.7,
                'reason': f'{month_wuxing}行克{dominant_wuxing}行，可能表现差'
            })
        
        # 根据实际统计调整置信度
        actual_win_rate = actual_stats['win_rate']
        predicted_win_rate = prediction['expected_win_rate']
        
        accuracy = 1 - abs(actual_win_rate - predicted_win_rate)
        prediction['accuracy'] = accuracy
        prediction['confidence'] = prediction['confidence'] * accuracy
        
        return prediction
    
    def _analyze_seasonal_patterns(self, monthly_stats: dict, dominant_wuxing: str) -> dict:
        """分析季节性规律"""
        seasonal_stats = {
            '春季': {'months': [2, 3, 4], 'stats': {}},
            '夏季': {'months': [5, 6, 7], 'stats': {}},
            '秋季': {'months': [8, 9, 10], 'stats': {}},
            '冬季': {'months': [11, 12, 1], 'stats': {}}
        }
        
        for season, season_info in seasonal_stats.items():
            season_returns = []
            season_win_rates = []
            
            for month in season_info['months']:
                if month in monthly_stats:
                    stats = monthly_stats[month]
                    # 获取该月所有收益率数据（需要从原始数据计算）
                    season_returns.append(stats['mean_return'])
                    season_win_rates.append(stats['win_rate'])
            
            if season_returns:
                seasonal_stats[season]['stats'] = {
                    'avg_return': np.mean(season_returns),
                    'avg_win_rate': np.mean(season_win_rates),
                    'return_std': np.std(season_returns),
                    'best_month': season_info['months'][np.argmax(season_returns)],
                    'worst_month': season_info['months'][np.argmin(season_returns)]
                }
        
        return seasonal_stats
    
    def plot_monthly_analysis(self, correlation_analysis: dict):
        """绘制月度分析图表"""
        asset_name = correlation_analysis['asset_name']
        monthly_correlations = correlation_analysis['monthly_correlations']
        seasonal_patterns = correlation_analysis['seasonal_patterns']
        
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle(f'{asset_name} 月度规律分析', fontsize=16, fontweight='bold')
        
        # 1. 月度收益率对比
        months = list(range(1, 13))
        actual_returns = []
        predicted_returns = []
        win_rates = []
        
        for month in months:
            if month in monthly_correlations:
                actual_stats = monthly_correlations[month]['actual_stats']
                predicted = monthly_correlations[month]['predicted_performance']
                
                actual_returns.append(actual_stats['mean_return'] * 100)  # 转换为百分比
                
                # 将预测转换为数值
                predicted_map = {'差': -2, '较差': -1, '中等': 0, '好': 1, '很好': 2}
                predicted_returns.append(predicted_map.get(predicted['expected_return'], 0))
                
                win_rates.append(actual_stats['win_rate'] * 100)
            else:
                actual_returns.append(0)
                predicted_returns.append(0)
                win_rates.append(50)
        
        axes[0, 0].plot(months, actual_returns, 'o-', label='实际收益率', linewidth=2)
        axes[0, 0].plot(months, predicted_returns, 's--', label='预测趋势', linewidth=2)
        axes[0, 0].set_title('月度收益率对比')
        axes[0, 0].set_xlabel('月份')
        axes[0, 0].set_ylabel('收益率 (%)')
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)
        
        # 2. 胜率分析
        axes[0, 1].bar(months, win_rates, alpha=0.7, color='skyblue')
        axes[0, 1].axhline(y=50, color='red', linestyle='--', alpha=0.7, label='50%基准线')
        axes[0, 1].set_title('月度胜率')
        axes[0, 1].set_xlabel('月份')
        axes[0, 1].set_ylabel('胜率 (%)')
        axes[0, 1].legend()
        axes[0, 1].grid(True, alpha=0.3)
        
        # 3. 季节性表现
        seasons = list(seasonal_patterns.keys())
        season_returns = []
        season_win_rates = []
        
        for season in seasons:
            if seasonal_patterns[season]['stats']:
                stats = seasonal_patterns[season]['stats']
                season_returns.append(stats['avg_return'] * 100)
                season_win_rates.append(stats['avg_win_rate'] * 100)
            else:
                season_returns.append(0)
                season_win_rates.append(50)
        
        x = np.arange(len(seasons))
        width = 0.35
        
        axes[1, 0].bar(x - width/2, season_returns, width, label='平均收益率', alpha=0.7)
        axes[1, 0].bar(x + width/2, season_win_rates, width, label='平均胜率', alpha=0.7)
        axes[1, 0].set_title('季节性表现')
        axes[1, 0].set_xlabel('季节')
        axes[1, 0].set_ylabel('表现 (%)')
        axes[1, 0].set_xticks(x)
        axes[1, 0].set_xticklabels(seasons)
        axes[1, 0].legend()
        axes[1, 0].grid(True, alpha=0.3)
        
        # 4. 五行关系分析
        relationships = []
        accuracies = []
        
        for month in months:
            if month in monthly_correlations:
                rel = monthly_correlations[month]['relationship']
                acc = monthly_correlations[month]['predicted_performance']['accuracy']
                relationships.append(rel)
                accuracies.append(acc * 100)
        
        # 统计各关系的预测准确度
        rel_stats = {}
        for rel, acc in zip(relationships, accuracies):
            if rel not in rel_stats:
                rel_stats[rel] = []
            rel_stats[rel].append(acc)
        
        if rel_stats:
            rel_names = list(rel_stats.keys())
            rel_accuracies = [np.mean(rel_stats[rel]) for rel in rel_names]
            
            axes[1, 1].bar(rel_names, rel_accuracies, alpha=0.7, color='lightcoral')
            axes[1, 1].set_title('五行关系预测准确度')
            axes[1, 1].set_xlabel('五行关系')
            axes[1, 1].set_ylabel('准确度 (%)')
            axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
    
    def generate_comprehensive_report(self, assets: list) -> dict:
        """生成综合分析报告"""
        print("=" * 80)
        print("📊 月度规律综合分析")
        print("=" * 80)
        
        all_analyses = {}
        
        for asset in assets:
            print(f"\n正在分析 {asset}...")
            
            # 分析月度规律
            monthly_analysis = self.analyze_monthly_patterns(asset)
            
            if not monthly_analysis:
                continue
            
            # 关联八字分析
            correlation_analysis = self.correlate_with_bazi(monthly_analysis)
            
            all_analyses[asset] = {
                'monthly_analysis': monthly_analysis,
                'correlation_analysis': correlation_analysis
            }
        
        # 生成综合对比报告
        self._generate_comparison_report(all_analyses)
        
        return all_analyses
    
    def _generate_comparison_report(self, all_analyses: dict):
        """生成对比报告"""
        print("\n" + "=" * 80)
        print("📈 三品种月度规律对比")
        print("=" * 80)
        
        # 创建对比表格
        comparison_data = []
        
        for asset, analysis in all_analyses.items():
            correlation = analysis['correlation_analysis']
            monthly_stats = correlation['monthly_correlations']
            
            # 计算整体统计
            all_returns = []
            all_win_rates = []
            all_accuracies = []
            
            for month_data in monthly_stats.values():
                actual_stats = month_data['actual_stats']
                predicted = month_data['predicted_performance']
                
                all_returns.append(actual_stats['mean_return'])
                all_win_rates.append(actual_stats['win_rate'])
                all_accuracies.append(predicted['accuracy'])
            
            comparison_data.append({
                '品种': asset,
                '主导五行': correlation['dominant_wuxing'],
                '平均收益率': f"{np.mean(all_returns)*100:.2f}%",
                '平均胜率': f"{np.mean(all_win_rates)*100:.1f}%",
                '预测准确度': f"{np.mean(all_accuracies)*100:.1f}%",
                '最佳月份': self._find_best_month(monthly_stats),
                '最差月份': self._find_worst_month(monthly_stats)
            })
        
        # 显示对比表格
        comparison_df = pd.DataFrame(comparison_data)
        print(comparison_df.to_string(index=False))
        
        # 分析共同规律
        self._analyze_common_patterns(all_analyses)
    
    def _find_best_month(self, monthly_stats: dict) -> str:
        """找到最佳月份"""
        best_month = 1
        best_return = -999
        
        for month, data in monthly_stats.items():
            actual_stats = data['actual_stats']
            if actual_stats['mean_return'] > best_return:
                best_return = actual_stats['mean_return']
                best_month = month
        
        return f"{best_month}月"
    
    def _find_worst_month(self, monthly_stats: dict) -> str:
        """找到最差月份"""
        worst_month = 1
        worst_return = 999
        
        for month, data in monthly_stats.items():
            actual_stats = data['actual_stats']
            if actual_stats['mean_return'] < worst_return:
                worst_return = actual_stats['mean_return']
                worst_month = month
        
        return f"{worst_month}月"
    
    def _analyze_common_patterns(self, all_analyses: dict):
        """分析共同规律"""
        print("\n" + "=" * 80)
        print("🔍 发现的共同规律")
        print("=" * 80)
        
        # 分析各月份的总体表现
        month_performance = {i: {'returns': [], 'win_rates': []} for i in range(1, 13)}
        
        for asset, analysis in all_analyses.items():
            monthly_stats = analysis['correlation_analysis']['monthly_correlations']
            
            for month, data in monthly_stats.items():
                actual_stats = data['actual_stats']
                month_performance[month]['returns'].append(actual_stats['mean_return'])
                month_performance[month]['win_rates'].append(actual_stats['win_rate'])
        
        # 计算各月份的平均表现
        month_avg = {}
        for month in range(1, 13):
            if month_performance[month]['returns']:
                month_avg[month] = {
                    'avg_return': np.mean(month_performance[month]['returns']),
                    'avg_win_rate': np.mean(month_performance[month]['win_rates'])
                }
        
        # 找出最佳和最差月份
        if month_avg:
            best_month = max(month_avg.keys(), key=lambda x: month_avg[x]['avg_return'])
            worst_month = min(month_avg.keys(), key=lambda x: month_avg[x]['avg_return'])
            
            print(f"\n📊 月度表现统计:")
            print(f"最佳月份: {best_month}月 (平均收益率: {month_avg[best_month]['avg_return']*100:.2f}%)")
            print(f"最差月份: {worst_month}月 (平均收益率: {month_avg[worst_month]['avg_return']*100:.2f}%)")
            
            print(f"\n📈 各月份平均收益率:")
            for month in sorted(month_avg.keys()):
                info = self.month_bazi[month]
                print(f"  {month}月 ({info['wuxing']}行, {info['season']}): {month_avg[month]['avg_return']*100:.2f}%")
            
            # 分析五行关系规律
            print(f"\n🔮 五行关系规律:")
            wuxing_performance = {}
            
            for month, performance in month_avg.items():
                month_wuxing = self.month_bazi[month]['wuxing']
                if month_wuxing not in wuxing_performance:
                    wuxing_performance[month_wuxing] = []
                wuxing_performance[month_wuxing].append(performance['avg_return'])
            
            for wuxing, returns in wuxing_performance.items():
                avg_return = np.mean(returns)
                print(f"  {wuxing}行月份平均收益率: {avg_return*100:.2f}%")


def main():
    """主函数"""
    analyzer = MonthlyPatternAnalyzer()
    assets = ['上证指数', '黄金', 'BTC']
    
    # 生成综合分析报告
    all_analyses = analyzer.generate_comprehensive_report(assets)
    
    # 为每个品种生成详细图表
    print("\n" + "=" * 80)
    print("📊 生成详细分析图表")
    print("=" * 80)
    
    for asset in assets:
        if asset in all_analyses:
            print(f"\n正在生成 {asset} 的月度分析图表...")
            correlation_analysis = all_analyses[asset]['correlation_analysis']
            analyzer.plot_monthly_analysis(correlation_analysis)
    
    print("\n✅ 月度规律分析完成！")


if __name__ == "__main__":
    main()
