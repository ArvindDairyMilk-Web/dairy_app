import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="Arvind Dairy App", layout="wide")

# ===== STYLE =====
st.markdown("""
<style>
.card {
    padding: 15px;
    border-radius: 12px;
    background: #f8f9fa;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
    margin-bottom: 15px;
}
</style>
""", unsafe_allow_html=True)

# ===== FILE =====
DATA_FILE = "data.csv"
EXP_FILE = "expense.csv"

def load(file, cols):
    if os.path.exists(file):
        try:
            df = pd.read_csv(file)
        except:
            df = pd.DataFrame(columns=cols)
    else:
        df = pd.DataFrame(columns=cols)
        df.to_csv(file, index=False)
    return df

df = load(DATA_FILE, ["Date","Customer","Shift","Qty","Fat","Rate","Amount"])
exp = load(EXP_FILE, ["Date","Amount","Note"])

if not df.empty:
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

def save():
    df.to_csv(DATA_FILE, index=False)
    exp.to_csv(EXP_FILE, index=False)

# ===== LOGIN =====
if "login" not in st.session_state:
    st.session_state.login = False

if not st.session_state.login:
    st.title("🔐 Login")

    u = st.text_input("Username")
    p = st.text_input("Password", type="password")

    if st.button("Login"):
        if u == "admin" and p == "1234":
            st.session_state.login = True
            st.rerun()
        else:
            st.error("Wrong login")

    st.stop()

# ===== SIDEBAR =====
st.sidebar.title("Arvind Dairy App")
menu = st.sidebar.radio("Menu",
["Dashboard","Entry","Records","Reports","Expense","Bill"])

st.title("🐄 Arvind Dairy App")

# ================= DASHBOARD =================
if menu == "Dashboard":

    if not df.empty:

        total = df["Amount"].sum()
        avg = df["Amount"].mean()

        best_day = df.groupby("Date")["Amount"].sum().idxmax()

        st.metric("Total ₹", total)
        st.metric("Average ₹", avg)

        st.info(f"Best Day: {best_day}")

        st.line_chart(df.groupby("Date")["Amount"].sum())

# ================= ENTRY =================
elif menu == "Entry":

    c1,c2,c3 = st.columns(3)

    with c1:
        date = st.date_input("Date")
        customer = st.text_input("Customer")

    with c2:
        shift = st.selectbox("Shift",["Morning","Evening"])
        qty = st.number_input("Milk",0.0)

    with c3:
        fat = st.number_input("Fat",0.0)
        rate100 = st.number_input("100 Fat Rate",90.0)

    rate = (rate100/100)*fat
    amount = qty * rate

    st.metric("Amount ₹", f"{amount:.2f}")

    if st.button("Save Entry"):
        df.loc[len(df)] = [date,customer,shift,qty,fat,rate,amount]
        save()
        st.success("Entry Saved ✅")

# ================= RECORD =================
elif menu == "Records":

    st.subheader("📊 Records")

    if not df.empty:

        # DATE FILTER
        start = st.date_input("From Date")
        end = st.date_input("To Date")

        filtered = df[
            (df["Date"] >= pd.to_datetime(start)) &
            (df["Date"] <= pd.to_datetime(end))
        ]

        st.dataframe(filtered)

# ================= REPORT =================
elif menu == "Reports":

    if not df.empty:
        df["Month"] = df["Date"].dt.strftime("%Y-%m")

        st.bar_chart(df.groupby("Month")["Amount"].sum())

# ================= EXPENSE =================
elif menu == "Expense":

    d = st.date_input("Date")
    a = st.number_input("Amount",0.0)
    n = st.text_input("Note")

    if st.button("Add Expense"):
        exp.loc[len(exp)] = [d,a,n]
        save()
        st.success("Expense Added")

    st.dataframe(exp)

# ================= BILL =================
elif menu == "Bill":

    st.subheader("🧾 Dairy Bill")

    date = st.date_input("Bill Date")
    name = st.text_input("Customer Name")
    qty = st.number_input("Milk",0.0)
    fat = st.number_input("Fat",0.0)
    rate100 = st.number_input("100 Fat Rate",90.0)

    rate = (rate100/100)*fat
    amount = qty * rate

    st.markdown(f"""
    ### 🐄 Arvind Dairy
    Date: {date}  
    Customer: {name}  

    Milk: {qty} L  
    Fat: {fat}  
    Rate: ₹ {rate:.2f}  

    ### Total: ₹ {amount:.2f}
    """)

# ===== LOGOUT =====
if st.sidebar.button("Logout"):
    st.session_state.login = False
    st.rerun()
