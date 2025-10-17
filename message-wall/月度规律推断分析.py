#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
基于八字分析的月度规律推断
当无法获取实时数据时，基于八字理论推断月度表现规律
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

class BaziBasedMonthlyAnalyzer:
    """基于八字理论的月度分析器"""
    
    def __init__(self):
        # 月份对应的天干地支和五行
        self.month_bazi = {
            1: {'dizhi': '丑', 'wuxing': '土', 'season': '冬季', 'name': '一月'},
            2: {'dizhi': '寅', 'wuxing': '木', 'season': '春季', 'name': '二月'},
            3: {'dizhi': '卯', 'wuxing': '木', 'season': '春季', 'name': '三月'},
            4: {'dizhi': '辰', 'wuxing': '土', 'season': '春季', 'name': '四月'},
            5: {'dizhi': '巳', 'wuxing': '火', 'season': '夏季', 'name': '五月'},
            6: {'dizhi': '午', 'wuxing': '火', 'season': '夏季', 'name': '六月'},
            7: {'dizhi': '未', 'wuxing': '土', 'season': '夏季', 'name': '七月'},
            8: {'dizhi': '申', 'wuxing': '金', 'season': '秋季', 'name': '八月'},
            9: {'dizhi': '酉', 'wuxing': '金', 'season': '秋季', 'name': '九月'},
            10: {'dizhi': '戌', 'wuxing': '土', 'season': '秋季', 'name': '十月'},
            11: {'dizhi': '亥', 'wuxing': '水', 'season': '冬季', 'name': '十一月'},
            12: {'dizhi': '子', 'wuxing': '水', 'season': '冬季', 'name': '十二月'}
        }
        
        # 五行相生相克关系
        self.wuxing_shengke = {
            '木': {'生': '火', '克': '土', '被生': '水', '被克': '金'},
            '火': {'生': '土', '克': '金', '被生': '木', '被克': '水'},
            '土': {'生': '金', '克': '水', '被生': '火', '被克': '木'},
            '金': {'生': '水', '克': '木', '被生': '土', '被克': '火'},
            '水': {'生': '木', '克': '火', '被生': '金', '被克': '土'}
        }
        
        # 各品种的八字特征（从之前的分析中获得）
        self.asset_bazi_features = {
            '上证指数': {
                'dominant_wuxing': '木',
                'nature': '阳性',
                'dominant_season': '夏季',
                'launch_date': '1990-12-19',
                'characteristics': '代表中国经济，具有成长性和进取性'
            },
            '黄金': {
                'dominant_wuxing': '木',
                'nature': '阴性',
                'dominant_season': '冬季',
                'launch_date': '1971-08-15',
                'characteristics': '贵金属，具有保值和收藏特性'
            },
            'BTC': {
                'dominant_wuxing': '木',
                'nature': '阳性',
                'dominant_season': '冬季',
                'launch_date': '2009-01-03',
                'characteristics': '数字货币，具有创新性和变化性'
            }
        }
    
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
    
    def predict_monthly_performance(self, asset_name: str) -> dict:
        """预测各月份的表现在"""
        asset_features = self.asset_bazi_features[asset_name]
        dominant_wuxing = asset_features['dominant_wuxing']
        
        monthly_predictions = {}
        
        for month, month_info in self.month_bazi.items():
            month_wuxing = month_info['wuxing']
            month_season = month_info['season']
            
            # 计算五行关系
            relationship = self.get_wuxing_relationship(dominant_wuxing, month_wuxing)
            
            # 基于五行关系预测表现
            prediction = self._calculate_performance_score(
                dominant_wuxing, month_wuxing, relationship, month_season, asset_features, asset_name
            )
            
            monthly_predictions[month] = {
                'month_name': month_info['name'],
                'month_wuxing': month_wuxing,
                'month_season': month_season,
                'relationship': relationship,
                'prediction': prediction,
                'descriptions': prediction['descriptions']
            }
        
        return monthly_predictions
    
    def _calculate_performance_score(self, dominant_wuxing: str, month_wuxing: str, 
                                   relationship: str, month_season: str, asset_features: dict, asset_name: str = None) -> dict:
        """计算表现评分"""
        
        # 基础评分
        base_scores = {
            '同': {'return': 0.6, 'volatility': 0.7, 'win_rate': 0.6, 'confidence': 0.8},
            '生': {'return': 0.8, 'volatility': 0.8, 'win_rate': 0.7, 'confidence': 0.9},
            '被生': {'return': 0.7, 'volatility': 0.6, 'win_rate': 0.65, 'confidence': 0.8},
            '克': {'return': 0.3, 'volatility': 0.8, 'win_rate': 0.4, 'confidence': 0.7},
            '被克': {'return': 0.2, 'volatility': 0.9, 'win_rate': 0.3, 'confidence': 0.8},
            '无': {'return': 0.5, 'volatility': 0.5, 'win_rate': 0.5, 'confidence': 0.5}
        }
        
        prediction = base_scores.get(relationship, base_scores['无']).copy()
        
        # 根据品种特性调整
        if asset_features['nature'] == '阳性':
            prediction['return'] += 0.1  # 阳性品种更积极
            prediction['volatility'] += 0.1
        else:
            prediction['return'] -= 0.05  # 阴性品种更稳健
            prediction['volatility'] -= 0.05
        
        # 根据主导季节调整
        dominant_season = asset_features['dominant_season']
        if month_season == dominant_season:
            prediction['return'] += 0.15
            prediction['win_rate'] += 0.1
            prediction['confidence'] += 0.1
        
        # 特殊调整（基于品种特性）
        if asset_name == '上证指数':
            # 上证指数在春季（政策利好）和夏季（经济活跃）表现更好
            if month_season in ['春季', '夏季']:
                prediction['return'] += 0.1
                prediction['win_rate'] += 0.05
        elif asset_name == '黄金':
            # 黄金在冬季（避险需求）和秋季（传统旺季）表现更好
            if month_season in ['冬季', '秋季']:
                prediction['return'] += 0.1
                prediction['win_rate'] += 0.05
        elif asset_name == 'BTC':
            # BTC在冬季（诞生季节）和春季（新技术周期）表现更好
            if month_season in ['冬季', '春季']:
                prediction['return'] += 0.15
                prediction['win_rate'] += 0.1
        
        # 确保分数在合理范围内
        for key in ['return', 'volatility', 'win_rate', 'confidence']:
            prediction[key] = max(0.1, min(1.0, prediction[key]))
        
        # 添加文字描述
        return_desc = {
            'return': self._get_return_description(prediction['return']),
            'volatility': self._get_volatility_description(prediction['volatility']),
            'win_rate': self._get_winrate_description(prediction['win_rate']),
            'confidence': self._get_confidence_description(prediction['confidence'])
        }
        
        prediction['descriptions'] = return_desc
        
        return prediction
    
    def _get_return_description(self, score: float) -> str:
        """获取收益率描述"""
        if score >= 0.8:
            return '很好'
        elif score >= 0.6:
            return '好'
        elif score >= 0.4:
            return '一般'
        else:
            return '较差'
    
    def _get_volatility_description(self, score: float) -> str:
        """获取波动性描述"""
        if score >= 0.8:
            return '很高'
        elif score >= 0.6:
            return '高'
        elif score >= 0.4:
            return '中等'
        else:
            return '低'
    
    def _get_winrate_description(self, score: float) -> str:
        """获取胜率描述"""
        if score >= 0.7:
            return '很高'
        elif score >= 0.6:
            return '高'
        elif score >= 0.5:
            return '中等'
        else:
            return '低'
    
    def _get_confidence_description(self, score: float) -> str:
        """获取置信度描述"""
        if score >= 0.8:
            return '很高'
        elif score >= 0.6:
            return '高'
        elif score >= 0.4:
            return '中等'
        else:
            return '低'
    
    def analyze_all_assets(self) -> dict:
        """分析所有品种"""
        print("=" * 80)
        print("🔮 基于八字理论的月度表现预测分析")
        print("=" * 80)
        
        all_predictions = {}
        
        for asset_name in self.asset_bazi_features.keys():
            print(f"\n📊 分析 {asset_name}...")
            
            predictions = self.predict_monthly_performance(asset_name)
            all_predictions[asset_name] = predictions
            
            # 显示分析结果
            asset_features = self.asset_bazi_features[asset_name]
            print(f"品种特征: {asset_features['characteristics']}")
            print(f"主导五行: {asset_features['dominant_wuxing']}")
            print(f"阴阳性质: {asset_features['nature']}")
            print(f"主导季节: {asset_features['dominant_season']}")
            
            print(f"\n月度表现预测:")
            print("-" * 50)
            
            for month in range(1, 13):
                pred = predictions[month]
                desc = pred['descriptions']
                print(f"{pred['month_name']:>4} ({pred['month_wuxing']}行, {pred['month_season']}): "
                      f"收益率{desc['return']:>2} 胜率{desc['win_rate']:>2} "
                      f"波动性{desc['volatility']:>2} 关系:{pred['relationship']}")
        
        return all_predictions
    
    def plot_predictions(self, all_predictions: dict):
        """绘制预测图表"""
        
        # 创建综合对比图
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('基于八字理论的月度表现预测', fontsize=16, fontweight='bold')
        
        # 1. 月度收益率预测对比
        months = list(range(1, 13))
        
        for asset_name, predictions in all_predictions.items():
            returns = [predictions[month]['prediction']['return'] for month in months]
            axes[0, 0].plot(months, returns, 'o-', label=asset_name, linewidth=2, markersize=6)
        
        axes[0, 0].set_title('月度收益率预测对比')
        axes[0, 0].set_xlabel('月份')
        axes[0, 0].set_ylabel('预测收益率')
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)
        axes[0, 0].set_ylim(0, 1)
        
        # 2. 月度胜率预测对比
        for asset_name, predictions in all_predictions.items():
            win_rates = [predictions[month]['prediction']['win_rate'] for month in months]
            axes[0, 1].plot(months, win_rates, 's-', label=asset_name, linewidth=2, markersize=6)
        
        axes[0, 1].axhline(y=0.5, color='red', linestyle='--', alpha=0.7, label='50%基准线')
        axes[0, 1].set_title('月度胜率预测对比')
        axes[0, 1].set_xlabel('月份')
        axes[0, 1].set_ylabel('预测胜率')
        axes[0, 1].legend()
        axes[0, 1].grid(True, alpha=0.3)
        axes[0, 1].set_ylim(0, 1)
        
        # 3. 五行关系影响分析
        wuxing_effects = {}
        for asset_name, predictions in all_predictions.items():
            for month, pred in predictions.items():
                relationship = pred['relationship']
                if relationship not in wuxing_effects:
                    wuxing_effects[relationship] = []
                wuxing_effects[relationship].append(pred['prediction']['return'])
        
        if wuxing_effects:
            relationships = list(wuxing_effects.keys())
            avg_returns = [np.mean(wuxing_effects[rel]) for rel in relationships]
            
            bars = axes[1, 0].bar(relationships, avg_returns, alpha=0.7)
            axes[1, 0].set_title('五行关系对收益率的影响')
            axes[1, 0].set_xlabel('五行关系')
            axes[1, 0].set_ylabel('平均预测收益率')
            axes[1, 0].grid(True, alpha=0.3)
            
            # 添加数值标签
            for bar, avg in zip(bars, avg_returns):
                axes[1, 0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                               f'{avg:.2f}', ha='center', va='bottom')
        
        # 4. 季节性表现预测
        seasonal_performance = {'春季': [], '夏季': [], '秋季': [], '冬季': []}
        
        for asset_name, predictions in all_predictions.items():
            season_returns = {'春季': [], '夏季': [], '秋季': [], '冬季': []}
            
            for month, pred in predictions.items():
                season = pred['month_season']
                season_returns[season].append(pred['prediction']['return'])
            
            for season in seasonal_performance.keys():
                if season_returns[season]:
                    seasonal_performance[season].append(np.mean(season_returns[season]))
        
        seasons = list(seasonal_performance.keys())
        season_avgs = [np.mean(seasonal_performance[season]) for season in seasons]
        
        bars = axes[1, 1].bar(seasons, season_avgs, alpha=0.7, 
                             color=['#90EE90', '#FFB6C1', '#FFD700', '#87CEEB'])
        axes[1, 1].set_title('季节性表现预测')
        axes[1, 1].set_xlabel('季节')
        axes[1, 1].set_ylabel('平均预测收益率')
        axes[1, 1].grid(True, alpha=0.3)
        
        # 添加数值标签
        for bar, avg in zip(bars, season_avgs):
            axes[1, 1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                           f'{avg:.2f}', ha='center', va='bottom')
        
        plt.tight_layout()
        plt.show()
    
    def generate_summary_report(self, all_predictions: dict):
        """生成总结报告"""
        print("\n" + "=" * 80)
        print("📋 月度规律总结报告")
        print("=" * 80)
        
        # 找出各品种的最佳和最差月份
        print("\n🎯 各品种最佳/最差月份:")
        print("-" * 50)
        
        for asset_name, predictions in all_predictions.items():
            best_month = max(predictions.keys(), 
                           key=lambda x: predictions[x]['prediction']['return'])
            worst_month = min(predictions.keys(), 
                            key=lambda x: predictions[x]['prediction']['return'])
            
            best_pred = predictions[best_month]
            worst_pred = predictions[worst_month]
            
            print(f"{asset_name}:")
            print(f"  最佳月份: {best_pred['month_name']} "
                  f"({best_pred['month_wuxing']}行, {best_pred['month_season']}, "
                  f"关系:{best_pred['relationship']}) "
                  f"收益率:{best_pred['descriptions']['return']}")
            
            print(f"  最差月份: {worst_pred['month_name']} "
                  f"({worst_pred['month_wuxing']}行, {worst_pred['month_season']}, "
                  f"关系:{worst_pred['relationship']}) "
                  f"收益率:{worst_pred['descriptions']['return']}")
        
        # 分析共同规律
        print(f"\n🔍 发现的共同规律:")
        print("-" * 50)
        
        # 分析各月份的整体表现
        month_performance = {i: [] for i in range(1, 13)}
        
        for asset_name, predictions in all_predictions.items():
            for month, pred in predictions.items():
                month_performance[month].append(pred['prediction']['return'])
        
        # 计算各月份的平均表现
        month_averages = {}
        for month in range(1, 13):
            if month_performance[month]:
                month_averages[month] = np.mean(month_performance[month])
        
        if month_averages:
            best_overall_month = max(month_averages.keys(), 
                                   key=lambda x: month_averages[x])
            worst_overall_month = min(month_averages.keys(), 
                                    key=lambda x: month_averages[x])
            
            print(f"整体最佳月份: {best_overall_month}月 "
                  f"(平均收益率: {month_averages[best_overall_month]:.3f})")
            print(f"整体最差月份: {worst_overall_month}月 "
                  f"(平均收益率: {month_averages[worst_overall_month]:.3f})")
        
        # 分析五行关系规律
        print(f"\n🔮 五行关系规律:")
        print("-" * 50)
        
        relationship_performance = {}
        for asset_name, predictions in all_predictions.items():
            for month, pred in predictions.items():
                relationship = pred['relationship']
                if relationship not in relationship_performance:
                    relationship_performance[relationship] = []
                relationship_performance[relationship].append(pred['prediction']['return'])
        
        for relationship, returns in relationship_performance.items():
            avg_return = np.mean(returns)
            print(f"{relationship}关系: 平均收益率 {avg_return:.3f} "
                  f"(样本数: {len(returns)})")
        
        # 交易策略建议
        print(f"\n💡 基于八字分析的交易策略建议:")
        print("-" * 50)
        
        print("1. 时机选择策略:")
        print("   - 在木行旺盛的春季(2-4月)增加仓位")
        print("   - 在金克木的秋季(8-10月)谨慎投资")
        print("   - 根据各品种的主导季节调整策略")
        
        print("\n2. 品种轮换策略:")
        print("   - 上证指数: 春季和夏季表现较好")
        print("   - 黄金: 冬季和秋季表现较好")
        print("   - BTC: 冬季和春季表现较好")
        
        print("\n3. 风险控制策略:")
        print("   - 所有品种都表现出高波动性特征")
        print("   - 需要严格的风险管理和仓位控制")
        print("   - 根据五行关系调整风险敞口")


def main():
    """主函数"""
    analyzer = BaziBasedMonthlyAnalyzer()
    
    # 分析所有品种
    all_predictions = analyzer.analyze_all_assets()
    
    # 绘制预测图表
    analyzer.plot_predictions(all_predictions)
    
    # 生成总结报告
    analyzer.generate_summary_report(all_predictions)
    
    print("\n✅ 基于八字理论的月度规律分析完成！")


if __name__ == "__main__":
    main()
