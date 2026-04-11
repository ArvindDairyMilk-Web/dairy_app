import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="Arvind Dairy Super App", layout="wide")

# ===== CSS (GLASS UI) =====
st.markdown("""
<style>

body {
    background: linear-gradient(to right, #e0ecff, #ffffff);
}

.card {
    padding: 15px;
    border-radius: 15px;
    background: rgba(255,255,255,0.7);
    backdrop-filter: blur(10px);
    box-shadow: 0px 4px 15px rgba(0,0,0,0.1);
    margin-bottom: 15px;
}

.big {
    font-size: 22px;
    font-weight: bold;
    color: #2c3e50;
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
    st.title("🔐 Login - Arvind Dairy")

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
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/1998/1998610.png", width=100)
menu = st.sidebar.radio("Menu",
["Dashboard","Entry","Records","Reports","Expense","Bill"])

st.title("🐄 Arvind Dairy Super App")

# ================= DASHBOARD =================
if menu == "Dashboard":

    if not df.empty:

        total = df["Amount"].sum()
        month = df[df["Date"].dt.month == datetime.today().month]
        month_total = month["Amount"].sum()

        exp_total = exp["Amount"].sum() if not exp.empty else 0
        profit = month_total - exp_total

        c1,c2,c3 = st.columns(3)

        c1.markdown(f'<div class="card big">Total ₹ {total:.2f}</div>', unsafe_allow_html=True)
        c2.markdown(f'<div class="card big">Monthly ₹ {month_total:.2f}</div>', unsafe_allow_html=True)
        c3.markdown(f'<div class="card big">Profit ₹ {profit:.2f}</div>', unsafe_allow_html=True)

        # PIE CHART
        st.subheader("📊 Income vs Expense")
        chart = pd.DataFrame({
            "Type":["Income","Expense"],
            "Value":[month_total,exp_total]
        })
        st.bar_chart(chart.set_index("Type"))

# ================= ENTRY =================
elif menu == "Entry":

    st.markdown('<div class="card">', unsafe_allow_html=True)

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
        st.success("Saved")

    st.markdown('</div>', unsafe_allow_html=True)

# ================= RECORD =================
elif menu == "Records":
    st.dataframe(df)

# ================= REPORT =================
elif menu == "Reports":

    if not df.empty:
        df["Month"] = df["Date"].dt.strftime("%Y-%m")

        st.line_chart(df.groupby("Date")["Amount"].sum())
        st.bar_chart(df.groupby("Month")["Amount"].sum())

# ================= EXPENSE =================
elif menu == "Expense":

    d = st.date_input("Date")
    a = st.number_input("Amount",0.0)
    n = st.text_input("Note")

    if st.button("Add Expense"):
        exp.loc[len(exp)] = [d,a,n]
        save()
        st.success("Added")

    st.dataframe(exp)

# ================= BILL =================
elif menu == "Bill":

    st.subheader("🧾 Generate Bill")

    date = st.date_input("Bill Date")
    name = st.text_input("Customer Name")
    qty = st.number_input("Milk",0.0)
    fat = st.number_input("Fat",0.0)
    rate100 = st.number_input("100 Fat Rate",90.0)

    rate = (rate100/100)*fat
    amount = qty * rate

    bill = f"""
    ARVIND DAIRY
    Date: {date}
    Customer: {name}

    Milk: {qty} L
    Fat: {fat}
    Rate: ₹ {rate:.2f}

    Total: ₹ {amount:.2f}
    """

    st.code(bill)

    st.download_button("Download Bill", bill, "bill.txt")

# ===== LOGOUT =====
if st.sidebar.button("Logout"):
    st.session_state.login = False
    st.rerun()
