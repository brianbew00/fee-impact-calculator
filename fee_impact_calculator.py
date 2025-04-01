import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

# Sidebar title
st.sidebar.markdown("<h2 style='font-size: 20px;'>📊 Fee Impact Calculator:<br>Active vs. Passive Investing</h2>", unsafe_allow_html=True)

# Sidebar inputs
st.sidebar.header("Customize Your Scenario")
initial_investment = st.sidebar.number_input("Initial Investment ($)", min_value=1000, value=100000, step=1000)
market_return = st.sidebar.slider("Expected Market Return (%)", 0.0, 15.0, 8.0, 0.1) / 100
index_fund_expense = st.sidebar.slider("Index Fund Expense Ratio (%)", 0.0, 1.0, 0.03, 0.01) / 100
active_fund_expense = st.sidebar.slider("Active Fund Expense Ratio (%)", 0.0, 2.0, 0.5, 0.1) / 100
aum_fee = st.sidebar.slider("Advisor AUM Fee (%)", 0.0, 2.0, 1.5, 0.1) / 100
years = st.sidebar.slider("Investment Duration (Years)", 1, 50, 30)

# Initialize values
years_list = np.arange(0, years + 1)
index_values = [initial_investment]
active_values = [initial_investment]
index_fees_paid = [0]
active_fees_paid = [0]

# Compound calculation with fee tracking
for _ in range(1, years + 1):
    # Fees based on beginning-of-year balance
    index_fee_amt = index_values[-1] * index_fund_expense
    active_fee_amt = active_values[-1] * (active_fund_expense + aum_fee)

    # Accumulate fees
    index_fees_paid.append(index_fees_paid[-1] + index_fee_amt)
    active_fees_paid.append(active_fees_paid[-1] + active_fee_amt)

    # Apply growth after subtracting fee
    new_index = index_values[-1] * (1 + market_return - index_fund_expense)
    new_active = active_values[-1] * (1 + market_return - active_fund_expense - aum_fee)

    index_values.append(new_index)
    active_values.append(new_active)

# Final values
final_index = index_values[-1]
final_active = active_values[-1]
total_index_fees = index_fees_paid[-1]
total_active_fees = active_fees_paid[-1]
dollar_difference = final_index - final_active
percent_difference = (dollar_difference / final_index) * 100

# Fee Impact Summary Table
summary_data = {
    "Metric": ["Final Portfolio Value", "Total Fees Paid"],
    "Passive (Index)": [f"${final_index:,.2f}", f"${total_index_fees:,.2f}"],
    "Active": [f"${final_active:,.2f}", f"${total_active_fees:,.2f}"],
    "Difference": [f"${dollar_difference:,.2f}", f"${(total_active_fees - total_index_fees):,.2f}"]
}
summary_df = pd.DataFrame(summary_data)

# Display Fee Impact Summary Table
st.markdown("### 💰 Fee Impact Summary")
st.table(summary_df.set_index("Metric"))

# Display Highlighted % Reduction
st.markdown(f"""
<div style='font-size: 20px; margin-top: 10px;'>
<strong>Reduction in Portfolio Due to Fees:</strong>
<span style='color: red; font-weight: bold;'>{percent_difference:.2f}%</span>
</div>
""", unsafe_allow_html=True)

# Plot: Growth Over Time
st.subheader("📈 Growth Over Time")

fig = go.Figure()
fig.add_trace(go.Scatter(x=years_list, y=index_values,
                         mode='lines', name='Index Fund (Low Fees)',
                         line=dict(width=3)))
fig.add_trace(go.Scatter(x=years_list, y=active_values,
                         mode='lines', name='Active Management (High Fees)',
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
  <li><strong>Most of the underperformance is due to fees, not strategy or market conditions.</strong></li>
</ul>
</div>
""", unsafe_allow_html=True)

# Data Table
df = pd.DataFrame({
    'Year': years_list,
    'Index Fund (Low Fees)': index_values,
    'Index Fees Paid': index_fees_paid,
    'Active Management (High Fees)': active_values,
    'Active Fees Paid': active_fees_paid
})

# Format as currency
for col in df.columns[1:]:
    df[col] = df[col].map('${:,.2f}'.format)

# Display Table
st.subheader("📋 Investment Growth Breakdown")
st.dataframe(df, use_container_width=True)
