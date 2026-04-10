import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="Dairy Manager", layout="wide")

# ===== FILE HANDLING (ONLINE SAFE) =====
file = "data.csv"

if os.path.exists(file):
    df = pd.read_csv(file)
else:
    df = pd.DataFrame(columns=["Date","Shift","Quantity","Fat","Rate","Amount"])
    df.to_csv(file, index=False)

st.title("🐄 Dairy Milk Manager")
st.markdown("### 📥 Daily Entry System")

# ===== INPUT SECTION =====
col1, col2, col3 = st.columns(3)

with col1:
    date = st.date_input("📅 Date")
    shift = st.selectbox("🌅 Shift", ["Morning", "Evening"])

with col2:
    qty = st.number_input("🥛 Milk (Litres)", min_value=0.0)
    fat = st.number_input("🧈 Fat %", min_value=0.0)

with col3:
    rate_100_fat = st.number_input("💰 100 Fat Rate (₹)", value=90.0)

# ===== CALCULATION =====
rate_per_fat = rate_100_fat / 100
rate = fat * rate_per_fat
amount = qty * rate

st.markdown("### 📊 Calculation")
c1, c2, c3 = st.columns(3)

c1.metric("1 Fat Rate", f"₹ {rate_per_fat:.2f}")
c2.metric("Final Rate", f"₹ {rate:.2f}")
c3.metric("Amount", f"₹ {amount:.2f}")

# ===== SAVE =====
if st.button("✅ Save Entry"):
    new_data = pd.DataFrame([[date, shift, qty, fat, rate, amount]],
                            columns=df.columns)
    df = pd.concat([df, new_data], ignore_index=True)
    df.to_csv(file, index=False)
    st.success("Saved Successfully!")

# ===== RECORDS =====
st.markdown("---")
st.markdown("## 📊 Records")

colf1, colf2 = st.columns(2)

with colf1:
    filter_shift = st.selectbox("Filter by Shift", ["All", "Morning", "Evening"])

with colf2:
    if not df.empty:
        df["Date"] = pd.to_datetime(df["Date"])
        start_date = st.date_input("From Date", df["Date"].min())
        end_date = st.date_input("To Date", df["Date"].max())
    else:
        start_date = end_date = datetime.today()

filtered_df = df.copy()

if filter_shift != "All":
    filtered_df = filtered_df[filtered_df["Shift"] == filter_shift]

if not filtered_df.empty:
    filtered_df["Date"] = pd.to_datetime(filtered_df["Date"])
    filtered_df = filtered_df[
        (filtered_df["Date"] >= pd.to_datetime(start_date)) &
        (filtered_df["Date"] <= pd.to_datetime(end_date))
    ]

st.dataframe(filtered_df, use_container_width=True)

# ===== SUMMARY =====
st.markdown("---")
st.markdown("## 💵 Summary")

colt1, colt2 = st.columns(2)

total_amount = filtered_df["Amount"].sum() if not filtered_df.empty else 0
colt1.metric("Total Amount", f"₹ {total_amount:.2f}")

if not df.empty:
    df["Date"] = pd.to_datetime(df["Date"])
    last_10 = df[df["Date"] >= (pd.Timestamp.today() - pd.Timedelta(days=10))]
    last_10_total = last_10["Amount"].sum()
else:
    last_10_total = 0

colt2.metric("Last 10 Days", f"₹ {last_10_total:.2f}")