import streamlit as st
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt

# Load and preprocess data
df = pd.read_csv("IFA.csv")
df = df.drop("Unnamed: 0", axis=1)
df["Date"] = pd.to_datetime(df["Date"])

# Streamlit UI
st.title("Stock Closing Price Viewer")

# Stock selection
symbols = df["Symbol"].unique()
selected_symbol = st.selectbox("Select a stock symbol:", symbols)

# Filter data
stk = df[df["Symbol"] == selected_symbol]

# Plotting
st.subheader(f"Closing Price of {selected_symbol}")
fig, ax = plt.subplots(figsize=(10, 5))
sb.lineplot(x=stk["Date"], y=stk["Close"], ax=ax)
plt.xticks(rotation=90)
st.pyplot(fig)
