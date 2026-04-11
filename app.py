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
