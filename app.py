import streamlit as st
import pandas as pd
from datetime import datetime
import os

# ===== PAGE =====
st.set_page_config(page_title="Arvind Dairy", layout="wide")

# ===== SAFE FILE SYSTEM (ERROR FIX) =====
file = "data.csv"

def load_data():
    if os.path.exists(file):
        return pd.read_csv(file)
    else:
        df = pd.DataFrame(columns=["Date","Shift","Quantity","Fat","Rate","Amount"])
        df.to_csv(file, index=False)
        return df

def save_data(df):
    df.to_csv(file, index=False)

df = load_data()

if not df.empty:
    df["Date"] = pd.to_datetime(df["Date"])

# ===== DESIGN =====
st.markdown("""
<style>

.header {
    background: linear-gradient(90deg, #0f2027, #203a43, #2c5364);
    padding: 20px;
    border-radius: 12px;
    color: white;
    text-align: center;
    font-size: 28px;
    font-weight: bold;
}

.card {
    background: #ffffff;
    padding: 15px;
    border-radius: 12px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
    margin-bottom: 15px;
}

.stButton>button {
    background: linear-gradient(90deg, #0f2027, #2c5364);
    color: white;
    border-radius: 8px;
    height: 45px;
    width: 100%;
}

</style>
""", unsafe_allow_html=True)

# ===== LOGIN =====
USERNAME = "admin"
PASSWORD = "1234"

if "login" not in st.session_state:
    st.session_state.login = False

if not st.session_state.login:
    st.markdown('<div class="header">🔐 Arvind Dairy Login</div>', unsafe_allow_html=True)

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
st.markdown('<div class="header">🐄 Arvind Dairy Milk Management</div>', unsafe_allow_html=True)

# ===== TABS =====
tab1, tab2, tab3, tab4 = st.tabs(["📥 Entry", "📊 Records", "📈 Reports", "💰 Dashboard"])

# ===== ENTRY =====
with tab1:
    st.markdown('<div class="card">', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        date = st.date_input("Date")
        shift = st.selectbox("Shift", ["Morning", "Evening"])

    with col2:
        qty = st.number_input("Milk (Ltr)", min_value=0.0)
        fat = st.number_input("Fat %", min_value=0.0)

    with col3:
        rate_100 = st.number_input("100 Fat Rate", value=90.0)

    rate = (rate_100 / 100) * fat
    amount = qty * rate

    st.metric("Amount ₹", f"{amount:.2f}")

    if st.button("Save Entry"):
        new = pd.DataFrame([[date, shift, qty, fat, rate, amount]],
                           columns=["Date","Shift","Quantity","Fat","Rate","Amount"])
        df = pd.concat([df, new], ignore_index=True)
        save_data(df)
        st.success("Saved Successfully!")

    st.markdown('</div>', unsafe_allow_html=True)

# ===== RECORDS =====
with tab2:
    st.markdown('<div class="card">',
