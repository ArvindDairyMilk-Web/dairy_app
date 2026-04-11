import streamlit as st
import pandas as pd
from datetime import datetime
import os

# ===== PAGE =====
st.set_page_config(page_title="Arvind Dairy", layout="wide")

# ===== FILE =====
file = "data.csv"

if os.path.exists(file):
    df = pd.read_csv(file)
else:
    df = pd.DataFrame(columns=["Date","Shift","Quantity","Fat","Rate","Amount"])
    df.to_csv(file, index=False)

if not df.empty:
    df["Date"] = pd.to_datetime(df["Date"])

# ===== LOGIN =====
USERNAME = "admin"
PASSWORD = "1234"

if "login" not in st.session_state:
    st.session_state.login = False

if not st.session_state.login:
    st.title("🔐 Arvind Dairy Login")

    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")

    if st.button("Login"):
        if user == USERNAME and pwd == PASSWORD:
            st.session_state.login = True
            st.rerun()
        else:
            st.error("Wrong Username or Password")

    st.stop()

# ===== HEADER =====
st.title("🐄 Arvind Dairy Milk Management")

# ===== TABS =====
tab1, tab2, tab3, tab4 = st.tabs(["Entry", "Records", "Reports", "Dashboard"])

# ===== ENTRY =====
with tab1:

    col1, col2, col3 = st.columns(3)

    with col1:
        date = st.date_input("Date")
        shift = st.selectbox("Shift", ["Morning", "Evening"])

    with col2:
        qty = st.number_input("Milk", min_value=0.0)
        fat = st.number_input("Fat", min_value=0.0)

    with col3:
        rate_100 = st.number_input("100 Fat Rate", value=90.0)

    rate = (rate_100 / 100) * fat
    amount = qty * rate

    st.metric("Amount ₹", f"{amount:.2f}")

    if st.button("Save Entry"):
        new = pd.DataFrame([[date, shift, qty, fat, rate, amount]],
                           columns=["Date","Shift","Quantity","Fat","Rate","Amount"])
        df = pd.concat([df, new], ignore_index=True)
        df.to_csv(file, index=False)
        st.success("Saved!")

# ===== RECORDS =====
with tab2:
    st.subheader("Records")

    if not df.empty:
        st.dataframe(df, use_container_width=True)

# ===== REPORTS =====
with tab3:
    st.subheader("Reports")

    if not df.empty:

        daily = df.groupby("Date")["Amount"].sum()
        st.line_chart(daily)

        df["Month"] = df["Date"].dt.to_period("M")
        monthly = df.groupby("Month")["Amount"].sum()
        st.bar_chart(monthly)

# ===== DASHBOARD =====
with tab4:
    st.subheader("Dashboard")

    if not df.empty:

        total = df["Amount"].sum()

        last10 = df[df["Date"] >= (pd.Timestamp.today() - pd.Timedelta(days=10))]
        last10_total = last10["Amount"].sum()

        current_month = df[df["Date"].dt.month == datetime.today().month]
        monthly_total = current_month["Amount"].sum()

        col1, col2, col3 = st.columns(3)

        col1.metric("Total ₹", f"{total:.2f}")
        col2.metric("Last 10 Days ₹", f"{last10_total:.2f}")
        col3.metric("This Month ₹", f"{monthly_total:.2f}")

# ===== LOGOUT =====
if st.sidebar.button("Logout"):
    st.session_state.login = False
    st.rerun()
