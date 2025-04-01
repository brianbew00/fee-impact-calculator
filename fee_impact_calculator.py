import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Streamlit App Title
st.title("📊 Fee Impact Calculator: Active vs. Passive Investing")

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
    # Net returns
    index_net_return = market_return - index_fund_expense
    active_net_return = market_return - active_fund_expense - aum_fee

    # Compound Growth
    index_values.append(index_values[-1] * (1 + index_net_return))
    active_values.append(active_values[-1] * (1 + active_net_return))

# Create DataFrame
df = pd.DataFrame({
    'Year': years_list,
    'Index Fund (Low Fees)': index_values,
    'Active Management (High Fees)': active_values
})

# Display DataFrame
st.subheader("📋 Investment Growth Breakdown")
st.dataframe(df)

# Plot the results
st.subheader("📈 Growth Over Time")

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(df['Year'], df['Index Fund (Low Fees)'], label='Index Fund (Low Fees)', linestyle='-', linewidth=2)
ax.plot(df['Year'], df['Active Management (High Fees)'], label='Active Management (High Fees)', linestyle='--', linewidth=2, color='red')

ax.set_xlabel("Years")
ax.set_ylabel("Portfolio Value ($)")
ax.set_title("Impact of Fees on Investment Growth")
ax.legend()
ax.grid(True)

# Show the plot in Streamlit
st.pyplot(fig)

st.markdown("""
### 💡 Key Takeaways:
- **Low-cost index funds grow significantly more over time due to reduced fees.**
- **Actively managed funds with AUM fees erode long-term wealth.**
- **Even a small difference in fees can lead to hundreds of thousands lost over decades.**
""")

# Footer
st.markdown("**Built with ❤️ using Streamlit**")
