"""
Streamlit Dashboard for EV Market Entry Analysis
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.data_loader import DataLoader
from src.market_analyzer import MarketAnalyzer

# Page config
st.set_page_config(
    page_title="EV Market Entry Strategy",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load data (cached)
@st.cache_data
def load_data():
    loader = DataLoader(data_dir='data')
    return loader.prepare_analysis_data()

# Title & Header
st.title("🚗 EV Charging Network - Market Entry Strategy")
st.markdown("**Data-driven analysis for optimal market entry and station placement**")
st.divider()

# Load data
market_data = load_data()
analyzer = MarketAnalyzer(market_data)

# Sidebar
st.sidebar.title("📊 Navigation")
page = st.sidebar.radio(
    "Select View:",
    ["📈 Market Overview", "🏙️ City Rankings", "🎯 Strategy & Recommendations", "⚠️ Risk Analysis"]
)

# Page 1: Market Overview
if page == "📈 Market Overview":
    col1, col2, col3, col4 = st.columns(4)
    
    metrics = analyzer.calculate_portfolio_metrics()
    
    with col1:
        st.metric("Total TAM (3-Year)", f"₹{metrics['total_tam_cr']:.0f} Cr")
    with col2:
        st.metric("Priority Cities", f"{metrics['total_cities']}")
    with col3:
        st.metric("Recommended Stations", f"{metrics['total_stations_recommended']}")
    with col4:
        st.metric("Avg ROI Multiple", f"{metrics['avg_roi']}x")
    
    st.divider()
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        top10 = analyzer.get_top_cities(10)
        fig = px.bar(
            top10,
            x='city',
            y='three_year_revenue_cr',
            title="Top 10 Cities by 3-Year Revenue Potential",
            labels={'three_year_revenue_cr': 'Revenue (₹ Crore)'},
            color='three_year_revenue_cr',
            color_continuous_scale='Viridis'
        )
        fig.update_layout(xaxis_tickangle=-45, height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.pie(
            top10,
            values='three_year_revenue_cr',
            names='city',
            title="Revenue Distribution - Top 10 Cities"
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

# Page 2: City Rankings
elif page == "🏙️ City Rankings":
    st.header("Detailed City Ranking Analysis")
    
    # City selector
    top_n = st.slider("Show Top N Cities:", 5, 30, 10)
    
    top_cities = analyzer.get_top_cities(top_n)
    st.dataframe(
        top_cities,
        use_container_width=True,
        hide_index=True
    )
    
    # Download button
    csv = top_cities.to_csv(index=False)
    st.download_button(
        label="📥 Download as CSV",
        data=csv,
        file_name="ev_cities_ranking.csv",
        mime="text/csv"
    )

# Page 3: Strategy & Recommendations
elif page == "🎯 Strategy & Recommendations":
    st.header("Strategic Rollout Plan")
    
    phase1 = analyzer.get_phase1_strategy()
    phase2 = analyzer.get_phase2_strategy()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Phase 1: Rapid Growth (0-18 months)")
        st.metric("Cities", f"{len(phase1['cities'])}")
        st.metric("Stations", f"{phase1['total_stations']}")
        st.metric("Investment", f"₹{phase1['total_investment_cr']:.0f} Cr")
        st.metric("Projected Revenue", f"₹{phase1['projected_revenue_cr']:.0f} Cr")
        
        st.write("**Cities:**")
        for city in phase1['cities']:
            st.write(f"• {city}")
    
    with col2:
        st.subheader("Phase 2: Market Consolidation (18-36 months)")
        st.metric("Cities", f"{len(phase2['cities'])}")
        st.metric("Stations", f"{phase2['total_stations']}")
        st.metric("Investment", f"₹{phase2['total_investment_cr']:.0f} Cr")
        st.metric("Projected Revenue", f"₹{phase2['projected_revenue_cr']:.0f} Cr")
        
        st.write("**Cities:**")
        for city in phase2['cities']:
            st.write(f"• {city}")
    
    st.divider()
    st.subheader("📊 Investment & Revenue Timeline")
    
    timeline_data = pd.DataFrame({
        'Phase': ['Phase 1', 'Phase 2'],
        'Duration': ['0-18 months', '18-36 months'],
        'Investment (₹Cr)': [phase1['total_investment_cr'], phase2['total_investment_cr']],
        'Projected Revenue (₹Cr)': [phase1['projected_revenue_cr'], phase2['projected_revenue_cr']]
    })
    
    fig = px.bar(
        timeline_data,
        x='Phase',
        y=['Investment (₹Cr)', 'Projected Revenue (₹Cr)'],
        barmode='group',
        title="Investment vs. Revenue by Phase"
    )
    st.plotly_chart(fig, use_container_width=True)

# Page 4: Risk Analysis
elif page == "⚠️ Risk Analysis":
    st.header("Risk Assessment & Mitigation")
    
    risks = analyzer.risk_assessment()
    
    for risk_name, risk_details in risks.items():
        col1, col2 = st.columns([1, 3])
        
        with col1:
            severity = risk_details['severity']
            color = {'HIGH': '🔴', 'MEDIUM': '🟡', 'LOW': '🟢'}[severity]
            st.markdown(f"### {color} {severity}")
        
        with col2:
            st.markdown(f"**{risk_name.replace('_', ' ').title()}**")
            st.write(f"*Mitigation:* {risk_details['mitigation']}")
        
        st.divider()

st.sidebar.divider()
st.sidebar.info(
    "📧 **Questions?**\n\n"
    "Contact: dsingh10_be22@thapar.edu\n\n"
    "LinkedIn: linkedin.com/in/dakshveer-singh-210d"
)
