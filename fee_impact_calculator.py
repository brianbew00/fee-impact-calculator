import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

# Move the main title to the sidebar
st.sidebar.markdown("<h2 style='font-size: 20px;'>📊 Fee Impact Calculator:<br>Active vs. Passive Investing</h2>", unsafe_allow_html=True)

# Sidebar Inputs
st.sidebar.header("Customize Your Scenario")
initial_investment = st.sidebar.number_input("Initial Investment ($)", min_value=1000, value=100000, step=1000)
market_return = st.sidebar.slider("Expected Market Return (%)", 0.0, 15.0, 8.0, 0.1) / 100
index_fund_expense = st.sidebar.slider("Index Fund Expense Ratio (%)", 0.0, 1.0, 0.03, 0.01) / 100
active_fund_expense = st.sidebar.slider("Active Fund Expense Ratio (%)", 0.0, 2.0, 0.5, 0.1) / 100
aum_fee = st.sidebar.slider("Advisor AUM Fee (%)", 0.0, 2.0, 1.5, 0.1) / 100
years = st.sidebar.slider("Investment Duration (Years)", 1, 50, 30)

# Initialize lists
years_list = np.arange(0, years + 1)
index_values = [initial_investment]
active_values = [initial_investment]
index_fees_paid = [0]
active_fees_paid = [0]

# Compound growth and fee tracking
for i in range(1, years + 1):
    # Net return
    index_net_return = market_return - index_fund_expense
    active_net_return = market_return - active_fund_expense - aum_fee

    # Prior values
    prev_index = index_values[-1]
    prev_active = active_values[-1]

    # Grow portfolio
    new_index = prev_index * (1 + index_net_return)
    new_active = prev_active * (1 + active_net_return)

    # Fee calculations
    index_fee_amt = prev_index * index_fund_expense
    active_fee_amt = prev_active * (active_fund_expense + aum_fee)

    # Append results
    index_values.append(new_index)
    active_values.append(new_active)
    index_fees_paid.append(index_fees_paid[-1] + index_fee_amt)
    active_fees_paid.append(active_fees_paid[-1] + active_fee_amt)

# Create DataFrame
df = pd.DataFrame({
    'Year': years_list,
    'Index Fund (Low Fees)': index_values,
    'Active Management (High Fees)': active_values,
    'Index Fees Paid': index_fees_paid,
    'Active Fees Paid': active_fees_paid
})

# Fee Impact Summary
final_index = index_values[-1]
final_active = active_values[-1]
total_index_fees = index_fees_paid[-1]
total_active_fees = active_fees_paid[-1]
dollar_difference = final_index - final_active
percent_difference = (dollar_difference / final_index) * 100

st.markdown("### 💰 Fee Impact Summary")
st.markdown(f"""
- **Final Value with Index Fund:** `${final_index:,.2f}`  
- **Final Value with Active Management:** `${final_active:,.2f}`  
- **Cumulative Dollar Difference:** `${dollar_difference:,.2f}`  
- **Percentage Reduction in Future Value Due to Fees:** `{percent_difference:.2f}%`  
- **Total Fees Paid – Index Fund:** `${total_index_fees:,.2f}`  
- **Total Fees Paid – Active Management:** `${total_active_fees:,.2f}`  
- **Extra Paid in Fees with Active Management:** `${(total_active_fees - total_index_fees):,.2f}`
""")

# Chart Section
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

# Key Takeaways
st.markdown("""
<div style='margin-top: 30px;'>
<h4>💡 Key Takeaways:</h4>
<ul>
  <li><strong>Low-cost index funds</strong> grow significantly more over time due to reduced fees.</li>
  <li><strong>Actively managed funds</strong> with AUM fees erode long-term wealth.</li>
  <li><strong>Most of the underperformance is due to fees, not skill or strategy.</strong></li>
</ul>
</div>
""", unsafe_allow_html=True)

# Format columns
df_display = df.copy()
df_display['Index Fund (Low Fees)'] = df_display['Index Fund (Low Fees)'].map('${:,.2f}'.format)
df_display['Active Management (High Fees)'] = df_display['Active Management (High Fees)'].map('${:,.2f}'.format)
df_display['Index Fees Paid'] = df_display['Index Fees Paid'].map('${:,.2f}'.format)
df_display['Active Fees Paid'] = df_display['Active Fees Paid'].map('${:,.2f}'.format)

# Table
st.subheader("📋 Investment Growth Breakdown")
st.dataframe(df_display, use_container_width=True)

