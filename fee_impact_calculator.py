import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

# Custom Title with Smaller Font
st.markdown("<h2 style='font-size: 28px;'>📊 Fee Impact Calculator: Active vs. Passive Investing</h2>", unsafe_allow_html=True)

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

# Plotly Interactive Chart
st.subheader("📈 Growth Over Time")

fig = go.Figure()
fig.add_trace(go.Scatter(x=df['Year'], y=df['Index Fund (Low Fees)'],
                         mode='lines',
                         name='Index Fund (Low Fees)',
                         line=dict(width=3)))
fig.add_trace(go.Scatter(x=df['Year'], y=df['Active Management (High Fees)'],
                         mode='lines',
                         name='Active Management (High Fees)',
                         line=dict(width=3, dash='dash', color='red')))

fig.update_layout(
    xaxis_title="Years",
    yaxis_title="Portfolio Value ($)",
    hovermode='x unified',
    template='plotly_white',
    legend=dict(x=0.01, y=0.99),
    margin=dict(l=40, r=20, t=40, b=40)
)

st.plotly_chart(fig, use_container_width=True)

# Fee Impact Summary (moved up)
final_index = index_values[-1]
final_active = active_values[-1]
dollar_difference = final_index - final_active
percent_difference = (dollar_difference / final_index) * 100

st.markdown("### 💰 Fee Impact Summary")
st.markdown(f"""
- **Final Value with Index Fund:** `${final_index:,.2f}`  
- **Final Value with Active Management:** `${final_active:,.2f}`  
- **Cumulative Dollar Difference:** `${dollar_difference:,.2f}`  
- **Percentage Reduction in Future Value Due to Fees:** `{percent_difference:.2f}%`
""")

# Key Takeaways (moved down)
st.markdown("""
<div style='margin-top: 30px;'>
<h4>💡 Key Takeaways:</h4>
<ul>
  <li><strong>Low-cost index funds</strong> grow significantly more over time due to reduced fees.</li>
  <li><strong>Actively managed funds</strong> with AUM fees erode long-term wealth.</li>
  <li><strong>Even a small difference in fees</strong> can lead to hundreds of thousands lost over decades.</li>
</ul>
</div>
""", unsafe_allow_html=True)

# Format currency columns for table display
df_display = df.copy()
df_display['Index Fund (Low Fees)'] = df_display['Index Fund (Low Fees)'].map('${:,.2f}'.format)
df_display['Active Management (High Fees)'] = df_display['Active Management (High Fees)'].map('${:,.2f}'.format)

# Table: Investment Growth Breakdown
st.subheader("📋 Investment Growth Breakdown")
st.dataframe(df_display, use_container_width=True)
