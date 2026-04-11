import streamlit as st
import pandas as pd
from datetime import datetime
import os

# ===== PAGE CONFIG =====
st.set_page_config(page_title="Arvind Dairy", layout="wide")

# ===== CUSTOM CSS =====
st.markdown("""
<style>

body {
    background: linear-gradient(to right, #eef2f3, #ffffff);
}

.header {
    background: linear-gradient(90deg, #1e3c72, #2a5298);
    padding: 18px;
    border-radius: 12px;
    color: white;
    text-align: center;
    font-size: 30px;
    font-weight: bold;
}

.card {
    background: white;
    padding: 15px;
    border-radius: 12px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
    margin-bottom: 15px;
}

.stButton>button {
    background: linear-gradient(90deg, #1e3c72, #2a5298);
    color: white;
    border-radius: 8px;
    height: 45px;
    width: 100%;
    font-size: 16px;
}

</style>
""", unsafe_allow_html=True)

# ===== LOGIN =====
USERNAME = "admin"
PASSWORD = "1234"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.markdown('<div class="header">🔐 Arvind Dairy Login</div>', unsafe_allow_html=True)

    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")

    if st.button("Login"):
        if user == USERNAME and pwd == PASSWORD:
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Wrong Username or Password")

    st.stop()

# ===== FILE =====
file = "data.csv"

if os.path.exists(file):
    df = pd.read_csv(file)
else:
    df = pd.DataFrame(columns=["Date","Shift","Quantity","Fat","Rate","Amount"])
    df.to_csv(file, index=False)

# ===== SIDEBAR =====
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/1998/1998610.png", width=100)
st.sidebar.title("Arvind Dairy")

menu = st.sidebar.radio("Menu", ["Entry", "Records", "Analytics"])

# ===== HEADER =====
st.markdown('<div class="header">🐄 Arvind Dairy Milk Management</div>', unsafe_allow_html=True)

# ===== ENTRY =====
if menu == "Entry":

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📥 Daily Entry")

    col1, col2, col3 = st.columns(3)

    with col1:
        date = st.date_input("Date")
        shift = st.selectbox("Shift", ["Morning", "Evening"])

    with col2:
        qty = st.number_input("Milk (Ltr)", min_value=0.0)
        fat = st.number_input("Fat %", min_value=0.0)

    with col3:
        rate_100 = st.number_input("100 Fat Rate", value=90.0)

    st.markdown('</div>', unsafe_allow_html=True)

    rate = (rate_100 / 100) * fat
    amount = qty * rate

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📊 Calculation")

    c1, c2, c3 = st.columns(3)
    c1.metric("1 Fat Rate", f"₹ {rate_100/100:.2f}")
    c2.metric("Final Rate", f"₹ {rate:.2f}")
    c3.metric("Amount", f"₹ {amount:.2f}")

    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("✅ Save Entry"):
        new = pd.DataFrame([[date, shift, qty, fat, rate, amount]],
                           columns=df.columns)
        df = pd.concat([df, new], ignore_index=True)
        df.to_csv(file, index=False)
        st.success("Saved Successfully!")

# ===== RECORDS =====
elif menu == "Records":

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📊 Records")
    st.dataframe(df, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ===== ANALYTICS =====
elif menu == "Analytics":

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📈 Income Chart")

    if not df.empty:
        df["Date"] = pd.to_datetime(df["Date"])
        chart_data = df.groupby("Date")["Amount"].sum()
        st.line_chart(chart_data)

    total = df["Amount"].sum() if not df.empty else 0
    st.metric("Total Income", f"₹ {total:.2f}")

    st.markdown('</div>', unsafe_allow_html=True)

# ===== LOGOUT =====
if st.sidebar.button("🚪 Logout"):
    st.session_state.logged_in = False
    st.rerun()
