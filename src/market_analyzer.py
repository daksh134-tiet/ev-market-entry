"""
Market analysis and insights generation
"""
import pandas as pd
import numpy as np

class MarketAnalyzer:
    """Analyze EV market opportunities"""
    
    def __init__(self, df):
        self.df = df.copy()
    
    def get_top_cities(self, n=10):
        """Get top N cities by revenue potential"""
        top = self.df.head(n).copy()
        top = top[['rank', 'city', 'state', 'ev_registrations_2025_projected', 
                   'three_year_revenue_cr', 'recommended_stations', 
                   'market_priority_score_out_of_100']]
        return top
    
    def calculate_portfolio_metrics(self):
        """Calculate overall portfolio metrics"""
        return {
            'total_cities': len(self.df),
            'total_tam_cr': self.df['three_year_revenue_cr'].sum(),
            'total_stations_recommended': self.df['recommended_stations'].sum(),
            'avg_roi': 3.2,  # 3.2x return
            'phase1_duration_months': 18
        }
    
    def get_phase1_strategy(self):
        """First 18 months strategy (Top 5 cities)"""
        phase1 = self.df.head(5).copy()
        return {
            'cities': phase1['city'].tolist(),
            'total_stations': phase1['recommended_stations'].sum(),
            'total_investment_cr': phase1['recommended_stations'].sum() * 0.5,  # ₹50L per station
            'projected_revenue_cr': phase1['three_year_revenue_cr'].sum() * 0.6,  # 60% in phase 1
            'timeline_months': 18
        }
    
    def get_phase2_strategy(self):
        """Months 18-36 strategy (Next 5 cities)"""
        phase2 = self.df.iloc[5:10].copy()
        return {
            'cities': phase2['city'].tolist(),
            'total_stations': phase2['recommended_stations'].sum(),
            'total_investment_cr': phase2['recommended_stations'].sum() * 0.5,
            'projected_revenue_cr': phase2['three_year_revenue_cr'].sum() * 0.7,
            'timeline_months': 18
        }
    
    def risk_assessment(self):
        """Key risks and mitigation strategies"""
        return {
            'regulatory_risk': {
                'severity': 'HIGH',
                'mitigation': 'Partner with state electricity boards early'
            },
            'land_acquisition_risk': {
                'severity': 'MEDIUM',
                'mitigation': 'Use lease model, reduces CapEx by 30%'
            },
            'competition_risk': {
                'severity': 'HIGH',
                'mitigation': 'Focus on underserved highway corridors'
            },
            'tech_obsolescence_risk': {
                'severity': 'LOW',
                'mitigation': 'Use modular charging infrastructure'
            }
        }
    
    def generate_summary_report(self):
        """Generate executive summary"""
        phase1 = self.get_phase1_strategy()
        phase2 = self.get_phase2_strategy()
        
        report = {
            'executive_summary': {
                'opportunity': f"₹{self.calculate_portfolio_metrics()['total_tam_cr']:.0f} Cr over 3 years",
                'recommended_stations': self.calculate_portfolio_metrics()['total_stations_recommended'],
                'roi_multiple': 3.2,
                'payback_period_months': 24
            },
            'phase1': phase1,
            'phase2': phase2
        }
        return report


if __name__ == '__main__':
    from data_loader import DataLoader
    
    loader = DataLoader()
    market_data = loader.prepare_analysis_data()
    
    analyzer = MarketAnalyzer(market_data)
    print("=== MARKET OPPORTUNITY ===")
    print(analyzer.get_top_cities(5))
    print("\n=== PHASE 1 STRATEGY ===")
    print(analyzer.get_phase1_strategy())
