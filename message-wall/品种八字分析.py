#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
品种八字深度分析模块
专门分析上证指数、黄金、BTC的八字特征和五行属性
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

class AssetBaziAnalyzer:
    """资产八字分析器"""
    
    def __init__(self):
        self.bazi_calc = BaziCalculator()
        
        # 定义各品种的关键日期（用于计算品种八字）
        self.asset_launch_dates = {
            '上证指数': datetime(1990, 12, 19),  # 上海证券交易所成立日期
            '黄金': datetime(1971, 8, 15),      # 布雷顿森林体系解体，黄金自由浮动
            'BTC': datetime(2009, 1, 3)         # 比特币创世区块
        }
        
        # 各品种的五行属性特征（基于传统理论）
        self.asset_wuxing_attributes = {
            '上证指数': {
                '主要属性': '土',
                '次要属性': '金',
                '特征': '代表中国经济，土主稳健，金主财富',
                '颜色': '黄色',
                '方位': '中央',
                '季节': '长夏'
            },
            '黄金': {
                '主要属性': '金',
                '次要属性': '土',
                '特征': '贵金属，金主贵重，土主收藏',
                '颜色': '金黄色',
                '方位': '西方',
                '季节': '秋季'
            },
            'BTC': {
                '主要属性': '火',
                '次要属性': '水',
                '特征': '数字货币，火主变化，水主流动',
                '颜色': '橙色',
                '方位': '南方',
                '季节': '夏季'
            }
        }
    
    def get_asset_bazi(self, asset_name: str) -> dict:
        """获取资产的八字信息"""
        if asset_name not in self.asset_launch_dates:
            raise ValueError(f"未知资产: {asset_name}")
        
        launch_date = self.asset_launch_dates[asset_name]
        bazi = self.bazi_calc.calculate_bazi(launch_date)
        wuxing = self.bazi_calc.analyze_wuxing_strength(bazi)
        
        return {
            'asset_name': asset_name,
            'launch_date': launch_date,
            'bazi': bazi,
            'wuxing_strength': wuxing,
            'traditional_attributes': self.asset_wuxing_attributes[asset_name]
        }
    
    def analyze_asset_characteristics(self, asset_name: str) -> dict:
        """深度分析资产特征"""
        asset_info = self.get_asset_bazi(asset_name)
        bazi = asset_info['bazi']
        wuxing = asset_info['wuxing_strength']
        traditional = asset_info['traditional_attributes']
        
        # 分析八字中的五行强弱
        max_wuxing = max(wuxing, key=wuxing.get)
        min_wuxing = min(wuxing, key=wuxing.get)
        
        # 计算五行平衡度
        wuxing_values = list(wuxing.values())
        balance_score = 1 - (np.std(wuxing_values) / np.mean(wuxing_values)) if np.mean(wuxing_values) > 0 else 0
        
        # 分析天干地支特征
        tiangan_analysis = self._analyze_tiangan(bazi)
        dizhi_analysis = self._analyze_dizhi(bazi)
        
        # 生成性格特征描述
        personality_traits = self._generate_personality_traits(wuxing, max_wuxing)
        
        return {
            'asset_name': asset_name,
            'launch_date': asset_info['launch_date'],
            'bazi_full': f"{bazi['year']} {bazi['month']} {bazi['day']} {bazi['hour']}",
            'wuxing_distribution': wuxing,
            'dominant_wuxing': max_wuxing,
            'weak_wuxing': min_wuxing,
            'balance_score': balance_score,
            'traditional_attributes': traditional,
            'tiangan_analysis': tiangan_analysis,
            'dizhi_analysis': dizhi_analysis,
            'personality_traits': personality_traits,
            'market_behavior_prediction': self._predict_market_behavior(wuxing, max_wuxing)
        }
    
    def _analyze_tiangan(self, bazi: dict) -> dict:
        """分析天干特征"""
        tiangan_list = [bazi['year_tg'], bazi['month_tg'], bazi['day_tg'], bazi['hour_tg']]
        
        # 统计天干分布
        tiangan_count = {}
        for tg in self.bazi_calc.tiangan:
            tiangan_count[tg] = tiangan_list.count(tg)
        
        # 分析天干特征
        yang_tiangan = ['甲', '丙', '戊', '庚', '壬']  # 阳干
        yin_tiangan = ['乙', '丁', '己', '辛', '癸']   # 阴干
        
        yang_count = sum(tiangan_count[tg] for tg in yang_tiangan)
        yin_count = sum(tiangan_count[tg] for tg in yin_tiangan)
        
        return {
            'distribution': tiangan_count,
            'yang_count': yang_count,
            'yin_count': yin_count,
            'yang_yin_ratio': yang_count / max(yin_count, 1),
            'nature': '阳性' if yang_count > yin_count else '阴性'
        }
    
    def _analyze_dizhi(self, bazi: dict) -> dict:
        """分析地支特征"""
        dizhi_list = [bazi['year_dz'], bazi['month_dz'], bazi['day_dz'], bazi['hour_dz']]
        
        # 统计地支分布
        dizhi_count = {}
        for dz in self.bazi_calc.dizhi:
            dizhi_count[dz] = dizhi_list.count(dz)
        
        # 分析地支特征
        spring_dz = ['寅', '卯', '辰']    # 春季地支
        summer_dz = ['巳', '午', '未']    # 夏季地支
        autumn_dz = ['申', '酉', '戌']    # 秋季地支
        winter_dz = ['子', '丑', '亥']    # 冬季地支
        
        season_count = {
            '春季': sum(dizhi_count[dz] for dz in spring_dz),
            '夏季': sum(dizhi_count[dz] for dz in summer_dz),
            '秋季': sum(dizhi_count[dz] for dz in autumn_dz),
            '冬季': sum(dizhi_count[dz] for dz in winter_dz)
        }
        
        dominant_season = max(season_count, key=season_count.get)
        
        return {
            'distribution': dizhi_count,
            'season_distribution': season_count,
            'dominant_season': dominant_season,
            'season_balance': max(season_count.values()) - min(season_count.values())
        }
    
    def _generate_personality_traits(self, wuxing: dict, max_wuxing: str) -> list:
        """生成性格特征描述"""
        traits = []
        
        wuxing_traits = {
            '木': ['创新', '成长', '灵活', '进取', '有活力'],
            '火': ['热情', '活跃', '变化', '快速', '有冲劲'],
            '土': ['稳健', '保守', '持久', '可靠', '有耐心'],
            '金': ['精确', '理性', '严谨', '冷静', '有价值'],
            '水': ['流动', '智慧', '适应', '深沉', '有韧性']
        }
        
        # 根据最强五行生成特征
        if max_wuxing in wuxing_traits:
            traits.extend(wuxing_traits[max_wuxing])
        
        # 根据五行强弱关系添加特征
        if wuxing[max_wuxing] >= 3:
            traits.append('特征明显')
        elif wuxing[max_wuxing] == 2:
            traits.append('特征中等')
        else:
            traits.append('特征温和')
        
        return traits
    
    def _predict_market_behavior(self, wuxing: dict, max_wuxing: str) -> dict:
        """预测市场行为特征"""
        behavior = {
            'volatility': '中等',
            'trend_strength': '中等',
            'risk_level': '中等',
            'growth_potential': '中等'
        }
        
        # 根据最强五行调整预测
        if max_wuxing == '木':
            behavior.update({
                'volatility': '较高',
                'trend_strength': '较强',
                'risk_level': '较高',
                'growth_potential': '较高'
            })
        elif max_wuxing == '火':
            behavior.update({
                'volatility': '很高',
                'trend_strength': '很强',
                'risk_level': '很高',
                'growth_potential': '很高'
            })
        elif max_wuxing == '土':
            behavior.update({
                'volatility': '较低',
                'trend_strength': '较弱',
                'risk_level': '较低',
                'growth_potential': '较低'
            })
        elif max_wuxing == '金':
            behavior.update({
                'volatility': '中等',
                'trend_strength': '中等',
                'risk_level': '中等',
                'growth_potential': '中等'
            })
        elif max_wuxing == '水':
            behavior.update({
                'volatility': '较高',
                'trend_strength': '较强',
                'risk_level': '较高',
                'growth_potential': '较高'
            })
        
        return behavior
    
    def compare_assets(self, asset_names: list) -> pd.DataFrame:
        """对比多个资产的特征"""
        comparison_data = []
        
        for asset_name in asset_names:
            analysis = self.analyze_asset_characteristics(asset_name)
            comparison_data.append({
                '资产名称': asset_name,
                '上市日期': analysis['launch_date'].strftime('%Y-%m-%d'),
                '八字': analysis['bazi_full'],
                '主导五行': analysis['dominant_wuxing'],
                '五行平衡度': f"{analysis['balance_score']:.3f}",
                '天干性质': analysis['tiangan_analysis']['nature'],
                '主导季节': analysis['dizhi_analysis']['dominant_season'],
                '波动性': analysis['market_behavior_prediction']['volatility'],
                '风险等级': analysis['market_behavior_prediction']['risk_level'],
                '成长潜力': analysis['market_behavior_prediction']['growth_potential']
            })
        
        return pd.DataFrame(comparison_data)
    
    def plot_asset_analysis(self, asset_name: str):
        """绘制资产分析图表"""
        analysis = self.analyze_asset_characteristics(asset_name)
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle(f'{asset_name} 八字深度分析', fontsize=16, fontweight='bold')
        
        # 五行分布饼图
        wuxing_data = analysis['wuxing_distribution']
        colors = ['#90EE90', '#FFB6C1', '#FFD700', '#FFA500', '#87CEEB']  # 木火土金水
        axes[0, 0].pie(wuxing_data.values(), labels=wuxing_data.keys(), autopct='%1.1f%%', 
                      colors=colors, startangle=90)
        axes[0, 0].set_title('五行分布')
        
        # 天干地支分布
        tiangan_dist = analysis['tiangan_analysis']['distribution']
        dizhi_dist = analysis['dizhi_analysis']['distribution']
        
        # 创建统一的天干地支列表
        all_elements = list(tiangan_dist.keys()) + list(dizhi_dist.keys())
        all_elements = list(set(all_elements))  # 去重
        
        tiangan_values = [tiangan_dist.get(elem, 0) for elem in all_elements]
        dizhi_values = [dizhi_dist.get(elem, 0) for elem in all_elements]
        
        x = np.arange(len(all_elements))
        width = 0.35
        axes[0, 1].bar(x - width/2, tiangan_values, width, label='天干', alpha=0.7)
        axes[0, 1].bar(x + width/2, dizhi_values, width, label='地支', alpha=0.7)
        axes[0, 1].set_xlabel('天干地支')
        axes[0, 1].set_ylabel('数量')
        axes[0, 1].set_title('天干地支分布')
        axes[0, 1].set_xticks(x)
        axes[0, 1].set_xticklabels(all_elements, rotation=45)
        axes[0, 1].legend()
        axes[0, 1].grid(True, alpha=0.3)
        
        # 季节分布
        season_data = analysis['dizhi_analysis']['season_distribution']
        axes[1, 0].bar(season_data.keys(), season_data.values(), 
                      color=['#90EE90', '#FFB6C1', '#FFD700', '#87CEEB'])
        axes[1, 0].set_title('季节分布')
        axes[1, 0].set_ylabel('数量')
        axes[1, 0].grid(True, alpha=0.3)
        
        # 市场行为预测
        behavior = analysis['market_behavior_prediction']
        behavior_names = list(behavior.keys())
        behavior_values = list(behavior.values())
        
        # 将文字转换为数值用于可视化
        value_map = {'很低': 1, '较低': 2, '中等': 3, '较高': 4, '很高': 5}
        numeric_values = [value_map.get(v, 3) for v in behavior_values]
        
        axes[1, 1].barh(behavior_names, numeric_values, color='skyblue', alpha=0.7)
        axes[1, 1].set_title('市场行为预测')
        axes[1, 1].set_xlabel('强度等级')
        axes[1, 1].set_xlim(0, 6)
        
        # 添加数值标签
        for i, (name, value) in enumerate(zip(behavior_names, behavior_values)):
            axes[1, 1].text(numeric_values[i] + 0.1, i, value, va='center')
        
        plt.tight_layout()
        plt.show()
        
        return analysis


def analyze_three_assets():
    """分析三个主要品种"""
    print("=" * 80)
    print("上证指数、黄金、BTC 八字深度分析")
    print("=" * 80)
    
    analyzer = AssetBaziAnalyzer()
    assets = ['上证指数', '黄金', 'BTC']
    
    # 逐个分析每个品种
    detailed_analyses = {}
    for asset in assets:
        print(f"\n{'='*60}")
        print(f"📊 {asset} 详细分析")
        print(f"{'='*60}")
        
        analysis = analyzer.analyze_asset_characteristics(asset)
        detailed_analyses[asset] = analysis
        
        print(f"上市日期: {analysis['launch_date'].strftime('%Y年%m月%d日')}")
        print(f"完整八字: {analysis['bazi_full']}")
        print(f"五行分布: {analysis['wuxing_distribution']}")
        print(f"主导五行: {analysis['dominant_wuxing']} (强度: {analysis['wuxing_distribution'][analysis['dominant_wuxing']]})")
        print(f"最弱五行: {analysis['weak_wuxing']} (强度: {analysis['wuxing_distribution'][analysis['weak_wuxing']]})")
        print(f"五行平衡度: {analysis['balance_score']:.3f}")
        
        print(f"\n传统属性:")
        traditional = analysis['traditional_attributes']
        print(f"  主要属性: {traditional['主要属性']}")
        print(f"  次要属性: {traditional['次要属性']}")
        print(f"  特征描述: {traditional['特征']}")
        print(f"  代表颜色: {traditional['颜色']}")
        print(f"  代表方位: {traditional['方位']}")
        print(f"  代表季节: {traditional['季节']}")
        
        print(f"\n天干分析:")
        tiangan = analysis['tiangan_analysis']
        print(f"  阴阳性质: {tiangan['nature']} (阳:{tiangan['yang_count']}, 阴:{tiangan['yin_count']})")
        print(f"  阴阳比例: {tiangan['yang_yin_ratio']:.2f}")
        
        print(f"\n地支分析:")
        dizhi = analysis['dizhi_analysis']
        print(f"  季节分布: {dizhi['season_distribution']}")
        print(f"  主导季节: {dizhi['dominant_season']}")
        print(f"  季节平衡度: {dizhi['season_balance']}")
        
        print(f"\n性格特征: {', '.join(analysis['personality_traits'])}")
        
        print(f"\n市场行为预测:")
        behavior = analysis['market_behavior_prediction']
        for key, value in behavior.items():
            print(f"  {key}: {value}")
    
    # 对比分析
    print(f"\n{'='*80}")
    print("📈 三品种对比分析")
    print(f"{'='*80}")
    
    comparison_df = analyzer.compare_assets(assets)
    print(comparison_df.to_string(index=False))
    
    # 总结规律
    print(f"\n{'='*80}")
    print("🔍 发现的规律和特征")
    print(f"{'='*80}")
    
    summarize_patterns(detailed_analyses)
    
    return detailed_analyses


def summarize_patterns(analyses: dict):
    """总结发现的规律"""
    print("\n📋 八字分析总结:")
    print("-" * 50)
    
    # 五行主导分析
    print("1. 五行主导特征:")
    for asset, analysis in analyses.items():
        dominant = analysis['dominant_wuxing']
        strength = analysis['wuxing_distribution'][dominant]
        print(f"   {asset}: {dominant}行主导 (强度:{strength})")
    
    # 阴阳特征分析
    print("\n2. 阴阳特征:")
    for asset, analysis in analyses.items():
        nature = analysis['tiangan_analysis']['nature']
        ratio = analysis['tiangan_analysis']['yang_yin_ratio']
        print(f"   {asset}: {nature} (比例:{ratio:.2f})")
    
    # 季节特征分析
    print("\n3. 季节特征:")
    for asset, analysis in analyses.items():
        season = analysis['dizhi_analysis']['dominant_season']
        print(f"   {asset}: 主导季节为{season}")
    
    # 平衡度分析
    print("\n4. 五行平衡度:")
    for asset, analysis in analyses.items():
        balance = analysis['balance_score']
        print(f"   {asset}: {balance:.3f} ({'平衡' if balance > 0.5 else '不平衡'})")
    
    # 市场行为预测对比
    print("\n5. 市场行为预测对比:")
    for asset, analysis in analyses.items():
        behavior = analysis['market_behavior_prediction']
        print(f"   {asset}:")
        print(f"     波动性: {behavior['volatility']}")
        print(f"     风险等级: {behavior['risk_level']}")
        print(f"     成长潜力: {behavior['growth_potential']}")
    
    # 发现的规律
    print("\n🎯 发现的重要规律:")
    print("-" * 50)
    
    patterns = []
    
    # 分析上证指数
    shanghai = analyses['上证指数']
    if shanghai['dominant_wuxing'] == '土':
        patterns.append("上证指数以土行为主导，体现其作为中国经济代表稳健的特性")
    
    # 分析黄金
    gold = analyses['黄金']
    if gold['dominant_wuxing'] == '金':
        patterns.append("黄金以金行为主导，符合其贵金属的本质属性")
    
    # 分析BTC
    btc = analyses['BTC']
    if btc['dominant_wuxing'] == '火':
        patterns.append("BTC以火行为主导，体现其作为数字货币的活跃和变化特性")
    
    # 输出发现的规律
    for i, pattern in enumerate(patterns, 1):
        print(f"{i}. {pattern}")
    
    # 交易策略建议
    print("\n💡 基于八字分析的交易策略建议:")
    print("-" * 50)
    print("1. 上证指数 (土行主导):")
    print("   - 适合长期投资，追求稳健收益")
    print("   - 在土行旺盛时期表现较好")
    print("   - 与金行品种(如黄金)有相生关系")
    
    print("\n2. 黄金 (金行主导):")
    print("   - 具有保值增值功能，适合避险")
    print("   - 在金行旺盛时期表现突出")
    print("   - 与土行品种(如上证指数)有相生关系")
    
    print("\n3. BTC (火行主导):")
    print("   - 波动性大，适合高风险高收益投资")
    print("   - 在火行旺盛时期表现活跃")
    print("   - 与木行品种有相生关系，与水行品种有相克关系")


def main():
    """主函数"""
    try:
        # 运行深度分析
        analyses = analyze_three_assets()
        
        # 绘制分析图表
        analyzer = AssetBaziAnalyzer()
        print(f"\n{'='*80}")
        print("📊 生成可视化分析图表")
        print(f"{'='*80}")
        
        for asset in ['上证指数', '黄金', 'BTC']:
            print(f"\n正在生成 {asset} 的分析图表...")
            analyzer.plot_asset_analysis(asset)
        
        print("\n✅ 分析完成！所有图表已生成。")
        
    except Exception as e:
        print(f"分析过程中出现错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
