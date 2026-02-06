from datetime import datetime

# -----------------------------
# ব্যালেন্স আপডেট ফাংশন
# -----------------------------
def add_transaction(user, type_, amount):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO transactions (user, type, amount, date) VALUES (?,?,?,?)",
              (user, type_, amount, now))
    # ব্যালেন্স আপডেট
    c.execute("SELECT balance FROM users WHERE username=?", (user,))
    current_balance = c.fetchone()[0]
    if type_ == "Deposit":
        new_balance = current_balance + amount
    else:
        new_balance = current_balance - amount
    c.execute("UPDATE users SET balance=? WHERE username=?", (new_balance, user))
    conn.commit()
    return new_balance

# -----------------------------
# হোম / Welcome পেজ
# -----------------------------
st.markdown("---")
st.markdown('<h2 style="color:#00d4ff;text-align:center;">🏠 হোম পেজ</h2>', unsafe_allow_html=True)

# ইউজারের ইনফো ডাইনামিক
if st.session_state.get('logged_in', False):
    user = st.session_state.user
    c.execute("SELECT full_name, balance, status, rank FROM users WHERE username=?", (user,))
    data = c.fetchone()
    full_name, balance, status, rank = data
else:
    full_name, balance, status, rank = "Guest", 0.0, "Pending", "Member"

# -----------------------------
# ব্যালেন্স / স্ট্যাটাস / র‍্যাঙ্ক কার্ড
# -----------------------------
col1, col2, col3 = st.columns(3)
col1.markdown(f"""
<div style="background:#0d1117;padding:15px;border-radius:15px;border:1px solid #30363d;text-align:center;">
<h4 style="color:#00d4ff;">ব্যালেন্স</h4>
<h2 style="color:white;">৳{balance}</h2>
</div>
""", unsafe_allow_html=True)

col2.markdown(f"""
<div style="background:#0d1117;padding:15px;border-radius:15px;border:1px solid #30363d;text-align:center;">
<h4 style="color:#00d4ff;">স্ট্যাটাস</h4>
<h2 style="color:white;">{status}</h2>
</div>
""", unsafe_allow_html=True)

col3.markdown(f"""
<div style="background:#0d1117;padding:15px;border-radius:15px;border:1px solid #30363d;text-align:center;">
<h4 style="color:#00d4ff;">র‍্যাঙ্ক</h4>
<h2 style="color:white;">{rank}</h2>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# ডিপোজিট / উইথড্র সেকশন
# -----------------------------
st.markdown("<h3 style='color:#00d4ff;'>💰 ব্যালেন্স আপডেট</h3>", unsafe_allow_html=True)
trx_type = st.selectbox("টাইপ", ["Deposit", "Withdraw"])
amount = st.number_input("পরিমাণ", min_value=0.0, step=100.0)
if st.button("আপডেট করুন"):
    if not st.session_state.get('logged_in', False):
        st.warning("দয়া করে প্রথমে লগইন করুন।")
    elif amount <= 0:
        st.warning("পরিমাণ অবশ্যই 0 এর বেশি হতে হবে।")
    else:
        new_balance = add_transaction(user, trx_type, amount)
        st.success(f"সফল! নতুন ব্যালেন্স: ৳{new_balance}")

# -----------------------------
# প্ল্যান লিস্ট
# -----------------------------
st.markdown("<h3 style='color:#00d4ff;'>📦 প্ল্যানসমূহ</h3>", unsafe_allow_html=True)

plans = [
    {"name": "Starter Plan", "amount": 500, "roi": "5% per month", "duration": "1 Month"},
    {"name": "Silver Plan", "amount": 2000, "roi": "7% per month", "duration": "3 Months"},
    {"name": "Gold Plan", "amount": 5000, "roi": "10% per month", "duration": "6 Months"},
    {"name": "Platinum Plan", "amount": 10000, "roi": "15% per month", "duration": "12 Months"},
]

for plan in plans:
    st.markdown(f"""
    <div style="background:#161b22;padding:15px;margin-bottom:10px;border-radius:15px;border:1px solid #30363d;">
    <h4 style="color:#00d4ff;">{plan['name']}</h4>
    <p style="color:white;">💵 Amount: ৳{plan['amount']}</p>
    <p style="color:white;">📈 ROI: {plan['roi']}</p>
    <p style="color:white;">⏳ Duration: {plan['duration']}</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<br><p style="text-align:center;color:#888;">© 2026 Global Power Metric</p>', unsafe_allow_html=True)
