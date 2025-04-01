import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Custom Title with Smaller Font
st.markdown("<h2 style='font-size: 28px;'>📊 Fee Impact Calculator: Active vs. Passive Investing</h2>", unsafe_allow_html=True)

# Key Takeaways Positioned Right After Title
st.markdown("""
<div style='margin-bottom: 30px;'>
<h4>💡 Key Takeaways:</h4>
<ul>
  <li><strong>Low-cost index funds</strong> grow significantly more over time due to reduced fees.</li>
  <li><strong>Actively managed funds</strong> with AUM fees erode long-term wealth.</li>
  <li><strong>Even a small difference in fees</strong> can lead to hundreds of thousands lost over decades.</li>
</ul>
</div>
""", unsafe_allow_html=True)

# Sidebar Inputs
st.sidebar.header("Investment Inputs")

initial_investment = st.sidebar.number_input("Initial Investment ($)", min_value=1000, value=100000, step=1000)
market_return = st.sidebar.slider("Expected Market Return (%)", 0.0, 15.0, 8.0, 0.1) / 100
index_fund_expense = st.sidebar.slider("Index Fund Expense Ratio (%)", 0.0, 1.0, 0.03, 0.01) / 100
active_fund_expense = st.sidebar.slider("Active Fund Expense Ratio (%)", 0.0, 2.0, 0.5, 0.1) / 100
aum_fee = st.sidebar.slider("Advisor AUM Fee (%)", 0.0, 2.0, 1.5, 0.1) / 100
years = st.sidebar.slider("Investment Duration (Years)", 1, 50, 30)

# Calculation Logic
years_list = np.arange(0, years + 1)
index_values = [initial_investment]
active_values = [initial_investment]

for i in range(1, years + 1):
    index_net_return = market_return - index_fund_expense
    active_net_return = market_return - active_fund_expense - aum_fee

    index_values.append(index_values[-1] * (1 + index_net_return))
    active_values.append(active_values[-1] * (1 + active_net_return))

# Create DataFrame
df = pd.DataFrame({
    'Year': years_list,
    'Index Fund (Low Fees)': index_values,
    'Active Management (High Fees)': active_values
})

# Format currency columns
df_display = df.copy()
df_display['Index Fund (Low Fees)'] = df_display['Index Fund (Low Fees)'].map('${:,.2f}'.format)
df_display['Active Management (High Fees)'] = df_display['Active Management (High Fees)'].map('${:,.2f}'.format)

# Chart: Investment Growth
st.subheader("📈 Growth Over Time")

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(df['Year'], df['Index Fund (Low Fees)'], label='Index Fund (Low Fees)', linestyle='-', linewidth=2)
ax.plot(df['Year'], df['Active Management (High Fees)'], label='Active Management (High Fees)', linestyle='--', linewidth=2, color='red')

ax.set_xlabel("Years")
ax.set_ylabel("Portfolio Value ($)")
ax.set_title("Impact of Fees on Investment Growth")
ax.legend()
ax.grid(True)

st.pyplot(fig)

# Table: Investment Growth Breakdown
st.subheader("📋 Investment Growth Breakdown")
st.dataframe(df_display, use_container_width=True)
