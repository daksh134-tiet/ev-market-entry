import streamlit as st
import pandas as pd
import plotly.express as px

st.title("EV Market Entry – Plotly Test")

df = pd.DataFrame({
    "city": ["Delhi", "Mumbai", "Bangalore"],
    "revenue_cr": [42.5, 38.2, 35.8],
})

st.dataframe(df)
fig = px.bar(df, x="city", y="revenue_cr", title="Revenue by city (₹ Cr)")
st.plotly_chart(fig, use_container_width=True)
