import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("IFA.csv")
    df = df.drop("Unnamed: 0", axis=1)
    df["Date"] = pd.to_datetime(df["Date"])
    return df

df = load_data()

# UI Layout
st.title("📈 Interactive Stock Data Explorer")

# Sidebar Controls
st.sidebar.header("Filter Options")

symbols = df["Symbol"].unique()
selected_symbols = st.sidebar.multiselect("Select stock symbol(s):", symbols, default=[symbols[0]])

# Filter by date
min_date = df["Date"].min()
max_date = df["Date"].max()
date_range = st.sidebar.date_input("Select date range:", [min_date, max_date], min_value=min_date, max_value=max_date)

# Show volume toggle
show_volume = st.sidebar.checkbox("Show Volume Chart", value=False)

# Filter data
filtered_df = df[(df["Symbol"].isin(selected_symbols)) & 
                 (df["Date"] >= pd.to_datetime(date_range[0])) & 
                 (df["Date"] <= pd.to_datetime(date_range[1]))]

# Plotting
if not filtered_df.empty:
    st.subheader("📊 Closing Price Over Time")
    fig = px.line(filtered_df, x="Date", y="Close", color="Symbol", markers=True,
                  title="Stock Closing Prices", labels={"Close": "Closing Price"})
    fig.update_layout(xaxis_title="Date", yaxis_title="Closing Price (¥)")
    st.plotly_chart(fig, use_container_width=True)

    if show_volume:
        st.subheader("📦 Volume Over Time")
        vol_fig = px.bar(filtered_df, x="Date", y="Volume", color="Symbol", title="Stock Volume Traded")
        st.plotly_chart(vol_fig, use_container_width=True)
else:
    st.warning("No data available for the selected options.")
