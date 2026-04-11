import streamlit as st
import pandas as pd
from datetime import datetime
import os

# ===== PAGE =====
st.set_page_config(page_title="Arvind Dairy", layout="wide")

# ===== FILE =====
file = "data.csv"

def load_data():
    if os.path.exists(file):
        df = pd.read_csv(file)
    else:
        df = pd.DataFrame(columns=["Date","Shift","Quantity","Fat","Rate","Amount"])
        df.to_csv(file, index=False)
    return df

def save_data(df):
    df.to_csv(file, index=False)

df = load_data()

# ===== DATE FIX =====
if not df.empty:
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

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
            st.error("Wrong Username")

    st.stop()

# ===== HEADER =====
st.title("🐄 Arvind Dairy Milk Management")

# ===== TABS =====
tab1, tab2, tab3, tab4 = st.tabs(["📥 Entry", "📊 Records", "📈 Reports", "💰 Dashboard"])

# ===== ENTRY =====
with tab1:

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
                           columns=df.columns)
        df = pd.concat([df, new], ignore_index=True)
        save_data(df)
        st.success("Saved Successfully!")

# ===== RECORDS (EDIT + DELETE) =====
with tab2:
    st.subheader("📊 Records")

    if not df.empty:

        selected_index = st.number_input("Select Row Index to Edit/Delete", min_value=0, max_value=len(df)-1, step=1)

        row = df.loc[selected_index]

        st.write("### ✏️ Edit Entry")

        col1, col2 = st.columns(2)

        with col1:
            new_qty = st.number_input("Quantity", value=float(row["Quantity"]))
            new_fat = st.number_input("Fat", value=float(row["Fat"]))

        with col2:
            new_shift = st.selectbox("Shift", ["Morning", "Evening"], index=0 if row["Shift"]=="Morning" else 1)
            new_rate100 = st.number_input("100 Fat Rate", value=float(row["Rate"]*100/row["Fat"]) if row["Fat"]!=0 else 90.0)

        new_rate = (new_rate100/100)*new_fat
        new_amount = new_qty * new_rate

        if st.button("Update Entry"):
            df.at[selected_index, "Quantity"] = new_qty
            df.at[selected_index, "Fat"] = new_fat
            df.at[selected_index, "Shift"] = new_shift
            df.at[selected_index, "Rate"] = new_rate
            df.at[selected_index, "Amount"] = new_amount
            save_data(df)
            st.success("Updated!")

        if st.button("Delete Entry"):
            df = df.drop(index=selected_index).reset_index(drop=True)
            save_data(df)
            st.warning("Deleted!")

        st.write("### 📋 Full Data")
        st.dataframe(df, use_container_width=True)

# ===== REPORTS =====
with tab3:
    st.subheader("📈 Reports")

    if not df.empty:

        daily = df.groupby("Date")["Amount"].sum()
        st.line_chart(daily)

        df["Month"] = df["Date"].dt.to_period("M").astype(str)
        monthly = df.groupby("Month")["Amount"].sum()
        st.bar_chart(monthly)

        shift_data = df.groupby("Shift")["Amount"].sum()
        st.bar_chart(shift_data)

# ===== DASHBOARD =====
with tab4:
    st.subheader("💰 Dashboard")

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
