import streamlit as st
import pandas as pd
from datetime import datetime
import os

# ===== LOGIN SYSTEM =====
USERNAME = "admin"
PASSWORD = "1234"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🔐 Login - Dairy Manager")

    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")

    if st.button("Login"):
        if user == USERNAME and pwd == PASSWORD:
            st.session_state.logged_in = True
            st.success("Login Successful")
        else:
            st.error("Wrong Username or Password")

    st.stop()

# ===== PAGE SETTINGS =====
st.set_page_config(page_title="Dairy Manager", layout="wide")

# ===== FILE =====
file = "data.csv"

if os.path.exists(file):
    df = pd.read_csv(file)
else:
    df = pd.DataFrame(columns=["Date","Shift","Quantity","Fat","Rate","Amount"])
    df.to_csv(file, index=False)

# ===== HEADER =====
st.title("🐄 Dairy Milk Manager")
st.markdown("### 📥 Daily Entry System")

# ===== INPUT =====
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
st.dataframe(df, use_container_width=True)

# ===== SUMMARY =====
st.markdown("---")
st.markdown("## 💵 Summary")

colt1, colt2 = st.columns(2)

total_amount = df["Amount"].sum() if not df.empty else 0
colt1.metric("Total Amount", f"₹ {total_amount:.2f}")

if not df.empty:
    df["Date"] = pd.to_datetime(df["Date"])
    last_10 = df[df["Date"] >= (pd.Timestamp.today() - pd.Timedelta(days=10))]
    last_10_total = last_10["Amount"].sum()
else:
    last_10_total = 0

colt2.metric("Last 10 Days", f"₹ {last_10_total:.2f}")

# ===== SLIP PREVIEW =====
st.markdown("---")
st.markdown("## 🧾 Slip Preview")

st.write(f"Date: {date}")
st.write(f"Shift: {shift}")
st.write(f"Milk: {qty} Ltr")
st.write(f"Fat: {fat}")
st.write(f"Rate: ₹ {rate:.2f}")
st.write(f"Amount: ₹ {amount:.2f}")

# ===== LOGOUT =====
if st.button("🚪 Logout"):
    st.session_state.logged_in = False
    st.experimental_rerun()
