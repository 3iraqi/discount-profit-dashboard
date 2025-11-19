# dashboard.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ---- Load your dataset ----
# Replace with your CSV or dataset path
df = pd.read_csv("./mart_sales_data_cleaned.csv", parse_dates=['Order Date', 'Ship Date'])
# Convert decimal discount to percentage string



# ---- Preprocessing ----
# Create is_loss column
df = df.assign(is_loss=lambda x: x['Profit'] < 0)

# Aggregate metrics by Discount
agg_df = df[df['Discount'] != 0].groupby('Discount').agg(
    Total_Profit=('Profit', 'sum'),
    Order_Count=('Profit', 'count'),
    Avg_Profit_Per_Order=('Profit', 'mean'),
    Loss_Count=('is_loss', 'sum')
).reset_index()
agg_df['Discount_Label'] = (agg_df['Discount'] * 100).astype(int).astype(str) + '%'

# Example:
# print(agg_df[['Discount', 'Discount_Label']])
# Calculate loss ratio
agg_df['Loss_Ratio'] = agg_df['Loss_Count'] / agg_df['Order_Count']

# ---- Streamlit App ----
st.title("Profit Analysis Dashboard by Discount")
st.write("Interactive dashboard to analyze profit, orders, and loss ratio by discount levels.")

# --- Total Profit by Discount ---
st.subheader("Total Profit by Discount")
fig_profit = px.bar(
    agg_df, x='Discount_Label', y='Total_Profit', 
    labels={'Discount': 'Discount', 'Total_Profit': 'Total Profit'},
    text='Total_Profit'
)
st.plotly_chart(fig_profit)

# --- Average Profit per Order ---
st.subheader("Average Profit per Order by Discount")
fig_avg = px.bar(
    agg_df, x='Discount_Label', y='Avg_Profit_Per_Order',
    labels={'Discount': 'Discount_Label', 'Avg_Profit_Per_Order': 'Average Profit per Order'},
    text='Avg_Profit_Per_Order'
)
st.plotly_chart(fig_avg)

# --- Order Count by Discount ---
st.subheader("Order Count by Discount")
fig_count = px.bar(
    agg_df, x='Discount', y='Order_Count',
    labels={'Discount': 'Discount', 'Order_Count': 'Number of Orders'},
    text='Order_Count'
)
st.plotly_chart(fig_count)

# --- Loss Ratio by Discount ---
st.subheader("Loss Ratio by Discount")
fig_loss = px.bar(
    agg_df, x='Discount', y='Loss_Ratio',
    labels={'Discount': 'Discount', 'Loss_Ratio': 'Loss Ratio'},
    text='Loss_Ratio'
)
st.plotly_chart(fig_loss)

# --- Profitability Heatmap ---
st.subheader("Profitability Heatmap")
st.subheader("Is Loss vs. Discount Heatmap")
heatmap_data = df[df['Discount'] != 0].pivot_table(
    index='Discount', 
    columns='is_loss', 
    values='Profit', 
    aggfunc='sum', 
    fill_value=0
)
fig_heat = px.imshow(
    heatmap_data,
    labels=dict(x="Loss Status (False=Profit, True=Loss)", y="Discount", color="Profit"),
    text_auto=True
)
st.plotly_chart(fig_heat)
# ---- Business Insight Message ----
st.markdown("""
### $\\to$ Business Insight:
- The **50% discount** leads to a **massive loss** (-86,458) despite a high order count (982 orders).  
- Discounts **10%-15%** are profitable and should be prioritized.  
- Higher discounts (>30%) are generally **not profitable** and should be used cautiously.  
- Consider **optimizing discount strategy** to balance sales volume and profitability.
""")
