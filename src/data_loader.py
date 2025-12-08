"""
Data loading and preprocessing module
"""
import pandas as pd
import numpy as np
from pathlib import Path

class DataLoader:
    """Load and preprocess EV market data"""
    
    def __init__(self, data_dir='data'):
        self.data_dir = Path(data_dir)
    
    def load_cities_data(self):
        """Load city-level EV data"""
        csv_path = self.data_dir / 'india_ev_cities.csv'
        
        if not csv_path.exists():
            raise FileNotFoundError(f"Data file not found: {csv_path}")
        
        df = pd.read_csv(csv_path)
        print(f"✓ Loaded {len(df)} cities data")
        return df
    
    def calculate_market_size(self, df):
        """Calculate 3-year revenue potential"""
        
        # Market sizing assumptions
        daily_km = 50  # Average daily kilometers
        charge_frequency = 1.5  # Charges per day
        avg_kwh_per_charge = 20
        tariff_per_kwh = 15  # INR
        market_capture_rate = 0.30  # 30% market share assumption
        annual_growth_rate = 1.12  # 12% CAGR
        
        # Calculate annual revenue
        df['annual_revenue_potential_cr'] = (
            (df['ev_registrations_2025_projected'] * 
             daily_km * 
             charge_frequency * 
             avg_kwh_per_charge * 
             tariff_per_kwh * 
             market_capture_rate) / 10000000  # Convert to Crores
        )
        
        # Calculate 3-year revenue with growth
        df['three_year_revenue_cr'] = (
            df['annual_revenue_potential_cr'] * 
            (1 + annual_growth_rate**0 + annual_growth_rate**1 + annual_growth_rate**2)
        )
        
        # Station requirement calculation
        df['recommended_stations'] = (
            df['three_year_revenue_cr'] * 1000000 / 500000  # INR 5L per station
        ).astype(int)
        
        return df
    
    def prepare_analysis_data(self):
        """Full pipeline: load → calculate → prepare"""
        df = self.load_cities_data()
        df = self.calculate_market_size(df)
        df = df.sort_values('three_year_revenue_cr', ascending=False).reset_index(drop=True)
        df['rank'] = range(1, len(df) + 1)
        
        print(f"✓ Market analysis complete")
        print(f"✓ Total TAM (3-year): ₹{df['three_year_revenue_cr'].sum():.1f} Crores")
        
        return df


if __name__ == '__main__':
    loader = DataLoader()
    market_data = loader.prepare_analysis_data()
    print(market_data[['rank', 'city', 'three_year_revenue_cr', 'recommended_stations']].head(10))
