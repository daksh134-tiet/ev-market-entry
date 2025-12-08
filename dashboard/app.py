import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.title("EV Market Entry – Test")

df = pd.DataFrame({
    "city": ["Delhi", "Mumbai", "Bangalore"],
    "revenue_cr": [42.5, 38.2, 35.8]
})

st.write("Top 3 cities by projected 3‑year revenue (₹ Cr):")
st.dataframe(df)

fig = px.bar(df, x="city", y="revenue_cr", title="Revenue by city (₹ Cr)")
st.plotly_chart(fig, use_container_width=True)
