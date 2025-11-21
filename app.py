# -*- coding: utf-8 -*-
"""
Created on Sat Nov 15 19:39:25 2025

@author: tarse
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import openai
from datetime import datetime

# ==========================
# PAGE CONFIG (FIRST)
# ==========================
st.set_page_config(
    page_title="Hisaab Kitab",
    layout="wide"
)

# ==========================
# GLOBAL STATE (for edit flow)
# ==========================
if "edit_row" not in st.session_state:
    st.session_state.edit_row = None
    


# ==========================
# CUSTOM UI (Background + Font + Colors)
# ==========================
def apply_styles(bg_url: str):
    st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("{bg_url}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    /* General font */
    @import url('https://fonts.googleapis.com/css2?family=Bodoni+Moda:wght@400;600;700;900&display=swap');
    html, body, div, span, label, input, textarea, select, button, p, h1, h2, h3, h4, h5, h6 {{
        font-family: "Bodoni Moda", serif !important;
    }}

    /* Headings black */
    h1{{color: #5F9EA0}}
    h2, h3, h4, h5, h6, label {{
        color: #000 !important;
        font-weight: 700 !important;
    }}

    /* Input boxes: black bg, white text */
    input, textarea, select {{
        background-color: #000 !important;
        color: #fff !important;
        border-radius: 8px !important;
        border: 1px solid #333 !important;
        padding: 6px !important;
    }}

    /* Quick Edit section text black */
    [data-testid="stHorizontalBlock"] {{
        color: #000000 !important;
    }}

    /* Metric text black */
    [data-testid="stMetricValue"], [data-testid="stMetricDelta"], [data-testid="stMetricLabel"] {{
        color: #000 ;
    }}
/* Only Header Glass Card */
.header-glass {{
    width: 100% !important;
    background: rgba(120, 0, 0, 0.45);
    padding: 3px;
    border-radius: 22px;
    margin-top: 20px;
    margin-bottom: 25px;
    backdrop-filter: blur(14px);
    border: 1px solid rgba(200, 0, 0, 0.55);
    box-shadow: 0 6px 20px rgba(70, 0, 0, 0.35);
}}
/* Sub Header Glass Card */
.subheader-glass {{
    width: 100% !important;
    background: rgba(120, 0, 0, 0.45);   /* Same dark red */
    padding: 3px;
    border-radius: 22px;
    margin-top: 20px;
    margin-bottom: 25px;
    backdrop-filter: blur(14px);
    border: 1px solid rgba(200, 0, 0, 0.55);
    box-shadow: 0 6px 20px rgba(70, 0, 0, 0.35);
}}

    /* Glass cards */
    .glass-card {{
        background: rgba(0, 0, 0, 0.75);
        border-radius: 18px;
        padding: 1px;
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.25);
        margin-bottom: 16px;
    }}
/* PURE WHITE FOOTER CARD */
.white-footer-card {{
    background: rgba(255, 255, 255, 1);   /* Full pure white */
    border-radius: 18px;
    padding: 25px;
    border: 1px solid rgba(0, 0, 0, 0.15); /* soft grey border */
    backdrop-filter: blur(0px);           /* no blur (pure solid) */
    margin-top: 25px;
    text-align: center;
}}
    /* Footer */
    .white-footer-card {{
        color: #000 !important;
        text-align: center;
        font-weight: 700 !important;
    }}




    /* ✅ Force Streamlit button text to white */
    div.stButton > button:first-child {{
        color: #fff !important;
        font-weight: 700 !important;
        background-color: #000 !important;  /* optional, keeps dark style */
        border: 1px solid #333 !important;
    }}
    div.stButton > button:first-child:hover {{
        color: #fff !important;
        background-color: #222 !important;
        
    }}
    
/* Summary text box */
.premium-summary-box {{
    background: rgba(255,255,255,0.15);
    padding: 20px;
    border-radius: 15px;
    color: black !important;
    font-size: 18px;
    line-height: 1.7;
    font-weight: 500;
    border-left: 4px solid gold;
}}
div[role=radiogroup] > label {{
    background-color: #111;
    border-radius: 8px;
    padding: 10px 14px;
    margin-bottom: 6px;
    border: 1px solid #333;
    display: flex;
    align-items: center;
    color: white !important;
    cursor: pointer;
}}

div[role=radiogroup] input {{
    display: none !important;
}}

div[role=radiogroup] > label:hover {{
    background-color: #222;
}}

div[role=radiogroup] > label:active {{
    background-color: #333;
}}
/* Make ALL form labels dark black */
.stApp label, .stApp p {{
    color: black !important;
    font-weight: 700 !important;
}}
/* Restore default text color for buttons */
.stApp button, .stApp button * {{
    color: white !important;
}}


[data-testid="stRadio"] label {{
    background: none !important;
    border: none !important;
    padding: 0 !important;
    margin-right: 20px !important;
    box-shadow: none !important;
}}

[data-testid="stRadio"] label p {{
    color: black !important;     /* ⭐ text now BLACK */
    font-weight: 700 !important;
    margin: 0 !important;
}}

[data-testid="stRadio"] label:hover {{
    background: none !important;
}}

[data-testid="stRadio"] svg {{
    fill: black !important;     /* ⭐ radio circle black */
    stroke: black !important;
}}
/* Bring radio inline with title */
[data-testid="stRadio"] {{
    margin-top: -8px !important;
    padding-top: 0 !important;
}}

/* Remove space inside options */
[data-testid="stRadio"] label {{
    margin-right: 20px !important;
    padding: 0 !important;
}}

/* Radio text spacing fix */
[data-testid="stRadio"] label p {{
    margin: 0 0 0 4px !important;
    padding: 0 !important;
}}
/* Reduce space above radio buttons */
.stRadio > div {{
    margin-top: -21px !important;
}}

/* Align Cash & UPI row properly */
.stRadio label p {{
    color: black !important;
    font-weight: 600 !important;
}}

/* Remove extra gap below radios */
.stRadio {{
    margin-bottom: -1000px !important;
}}
{{ /* Pull entire Cash + UPI row LEFT */ }}
.stRadio > div {{
    margin-left: -140px !important;
}}


/* Make Metrics Bigger & Bolder */
[data-testid="stMetricValue"] {{
    font-size: 32px !important;     /* Value size (₹, numbers) */
    font-weight: 900 !important;
    color: slateblue !important;
}}

[data-testid="stMetricLabel"] {{
    font-size: 120px !important;     /* Label size (Cash, UPI, etc.) */
    font-weight: 1000 !important;
    color: black !important;
}}

[data-testid="stMetricDelta"] {{
    font-size: 18px !important;  
}}
/* Disable typing but DO NOT hide input */
.stSelectbox div[data-baseweb="select"] input {{
    pointer-events: none !important;     /* No typing */
    caret-color: transparent !important;  /* No cursor */
    color: transparent !important;        /* No text visible */
    background: transparent !important;
    border: none !important;
    outline: none !important;
}}

/* Remove placeholder text completely */
.stSelectbox div[data-baseweb="select"] input::placeholder {{
    color: transparent !important;
}}

/* Hide search box inside dropdown menu */
div[data-baseweb="popover"] input {{
    display: none !important;
}}







    </style>
    """, unsafe_allow_html=True)


apply_styles("https://i.pinimg.com/736x/e0/57/5b/e0575bac3b38b3c19d35118649c3a64e.jpg")

from supabase import create_client, Client

SUPABASE_URL = "https://skfubcpggfsepzlvpjym.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNrZnViY3BnZ2ZzZXB6bHZwanltIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjM2MjY1NjcsImV4cCI6MjA3OTIwMjU2N30.JX4qdt7OR_mH6BUcqzfd5RrGoksjRUJyQ0b_Uu-Y0Bc"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
def login_ui():
    st.markdown("""
    <style>
    .login-container {
        display: flex;
        flex-direction: column;
        height: 1vh;    /* Center vertically */
        text-align: center;
        margin-top: 10px;
        margin-left: 1200px;
    }
    /* General font */
    @import url('https://fonts.googleapis.com/css2?family=Bodoni+Moda:wght@400;600;700;900&display=swap');
    html, body, div, span, label, input, textarea, select, button, p, h1, h2, h3, h4, h5, h6 {{
        font-family: "Bodoni Moda", serif !important;
    }}


        
/* FONT SIZE ONLY for Email / Password input text */
.stTextInput > div > div > input {
    font-size: 27px !important;
    font-weight: 700 !important;
}

/* FONT SIZE of Label (📧 Email & 🔑 Password) */
.stTextInput label {
    font-size: 20px !important;
    font-weight: 900 !important;
}

   

    .login-title {
        font-size: 45px;
        font-weight: 900;
        margin-top: -131px;
        margin-left: 469px;
        color: #5F9EA0 ;
    }
    .tagline {
    font-size: 41px !important;
    font-weight: 700 !important;
    color: #444 !important;
    text-align: center;
    margin-bottom: 25px;
}


  
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='login-container'>", unsafe_allow_html=True)
    col1, col2 = st.columns([2, 6])  # 4 = empty space, 1 = logo area
    with col2:
        st.image("hisaab_logo.png", width=110)

    st.markdown("<div class='login-title'>Hisaab Kitab ( Shop Login )</div>", unsafe_allow_html=True)
    st.markdown(
    "<p class='tagline'>Welcome ! Enter your login email and password👇</p>",
    unsafe_allow_html=True
)
    

    st.markdown("<div class='login-box'>", unsafe_allow_html=True)

    email = st.text_input("📧  Email", key="login_email", placeholder="Enter your email")
    password = st.text_input("🔑 Password", type="password", key="login_pass", placeholder="Enter password")

    if st.button("Login Now", use_container_width=False):
        try:
            res = supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            if res.user:
                st.session_state.user = res.user
                st.success("Login successful!")
                st.experimental_rerun()
            else:
                st.error("Wrong email or password")
        except Exception:
            st.error("Login failed — contact admin")

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


# Stop entire app until user logs in
if "user" not in st.session_state:
    login_ui()
    st.stop()


# ⬇️ YAHAN Step-1 paste karna hai
st.markdown("""
<style>
.ai-summary-text {
    color: black !important;
    font-size: 18px;
    line-height: 1.6;
    font-weight: 500;
}
</style>
""", unsafe_allow_html=True)

# ==========================
# OPENAI KEY (keep in secrets for production)
# ==========================
openai.api_key = "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"  # replace or use st.secrets["OPENAI_API_KEY"]

# ==========================
# GOOGLE SHEETS SETUP
# ==========================


# ==========================
# HEADER
# ==========================
# HEADER with background color
# ==========================

st.markdown("<div class='header-glass'>", unsafe_allow_html=True)


col1, col2, col3 = st.columns([1, 6, 1])

with col2:
    inner_col1, inner_col2 = st.columns([1, 4])

    with inner_col1:
        st.image("hisaab_logo.png", width=100)

    with inner_col2:
        st.markdown(
            """
            <h1 style="
                margin: 0;
                font-weight:900;
                font-size:50px;
                transform: translateX(-80px);
                color: 1E90FF !important;
            ">
                Hisaab Kitab  ( Sales Manager )
            </h1>
            """, 
            unsafe_allow_html=True
        )

# closing div
st.markdown("</div>", unsafe_allow_html=True)



# ==========================
# ADD SALE ENTRY
# ==========================
st.markdown("<div class='subheader-glass'>", unsafe_allow_html=True)
st.subheader("➕ Add Sale Entry")

with st.form("entry_form", clear_on_submit=True):


    # --- Row 1 ---
    colA, colB = st.columns([2, 2])
    with colA:
        p = st.text_input("Product Name", placeholder="Type product name")
    with colB:
        q = st.number_input("Quantity", min_value=1)

    # --- Row 2 ---
    colC, colD = st.columns([2, 2])
    with colC:
        price = st.number_input("Price per Item (₹)", min_value=1.0, step=0.5)
    with colD:
        status = st.selectbox("Status", ["Sold", "Defected"], index=0)

    # --- Mode of Payment (Working + Clean) ---
    # --- MODE OF PAYMENT (Perfect Alignment) ---
    col1, col2 = st.columns([1, 4])
    with col1:
        st.write("Mode of Payment")
    with col2:
        mode = st.radio(
        label="",
        options=["Cash", "UPI"],
        horizontal=True,
        key="mode_payment"
    )

        

    # --- SUBMIT BUTTON (IMPORTANT: form ke last line par hi ho) ---
    submit = st.form_submit_button("Add Sale")

# FORM ke BAHAAR ye chalega
if submit:
    with st.spinner("⏳ Adding entry..."):
        today = datetime.now().strftime("%Y-%m-%d")
        

    supabase.table("sales").insert({
        "date": today,
        "product": p,
        "quantity": q,
        "price": price,
        "status": status,
        "mode": mode,
        "shop_id": st.session_state.user.id  # UNIQUE PER SHOP!
    }).execute()

    st.success(f"Added: {p} ({status})")



st.markdown("</div>", unsafe_allow_html=True)


# ==========================
# LOAD DATA
# ==========================
response = supabase.table("sales").select("id, date, product, quantity, price, status, mode, shop_id").execute()
data = pd.DataFrame(response.data)


# Column Name Fix
#data.rename(columns={
    

# OR (better)
data.columns = data.columns.str.lower()   # sab lowercase ho jayenge
  # saare first letter capital


if data.empty:
    st.info("📄 No data available yet.")
else:
    # Make sure types are numeric for math/graphs
    if "quantity" in data.columns:
        data["quantity"] = pd.to_numeric(data["quantity"], errors="coerce").fillna(0)
    if "Price" in data.columns:
        data["price"] = pd.to_numeric(data["price"], errors="coerce").fillna(0)
    data["revenue"] = data["quantity"] * data["price"]

    today_str = datetime.now().strftime("%Y-%m-%d")
    today_df = data[data["date"] == today_str].copy()

    # ---- TODAY TABLE (with edit buttons) ----
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader(f"📅 Today's Sales ({today_str})")

    if today_df.empty:
        st.info("👋 No sales recorded today.")
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        # Show a clean table (read-only view)
        st.dataframe(today_df, use_container_width=True)

        st.markdown("</div>", unsafe_allow_html=True)
        # ---- INLINE 'EDIT' BUTTONS PER ROW (opens edit form) ----
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("✏️ Quick Edit (Today's Entries)")

        # We'll use original index (row in 'data') to compute sheet row numbers
        # sheet row = data_index + 2 (because header occupies row 1)
        edit_target = None
        for i, (idx, row) in enumerate(today_df.iterrows()):
            c1, c2, c3, c4, c5, c6,c7 = st.columns([2, 3, 2, 2, 2, 2 ,1])
            c1.write(f"📌 {row['date']}")
            c2.write(f"🧾 {row['product']}")
            c3.write(f"Qty: {int(row['quantity'])}")
            c4.write(f"₹ {float(row['price']):,.2f}")
            c5.write(f"Status: {row['status']}")
            c6.write(f"Mode: {row['mode']}")
            if c7.button("✏️", key=f"edit_btn_{idx}"):
                st.session_state.edit_row = int(idx)  # store original 'data' index

        st.markdown("</div>", unsafe_allow_html=True)

        # ---- EDIT FORM (when a row is selected) ----
if st.session_state.edit_row is not None:
    edit_idx = st.session_state.edit_row
    row_data = data.loc[edit_idx]

    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader("✏️ Edit Entry")

    new_product = st.text_input("Product Name", value=str(row_data["product"]))
    new_qty = st.number_input("Quantity", min_value=1, value=int(row_data["quantity"]))
    new_price = st.number_input("Price per Item (₹)", min_value=1.0, value=float(row_data["price"]))
    new_status = st.selectbox("Status", ["Sold", "Defected"],
                              index=(0 if row_data["status"] == "Sold" else 1))

    # --- MODE OF PAYMENT (EXACT SAME AS ADD ENTRY) ---
    colE1, colE2 = st.columns([1, 4])

    with colE1:
        st.write("Mode of Payment")

    with colE2:
        new_mode = st.radio(
            label="",
            options=["Cash", "UPI"],
            horizontal=True,
            index=(0 if row_data["mode"] == "Cash" else 1),
            key=f"edit_mode_{edit_idx}"
        )

    # --- SAVE / CANCEL BUTTONS ---
    save_col, cancel_col = st.columns([1, 1])

    if save_col.button("💾 Save Changes"):
        sheet_row = int(edit_idx) + 2

        # Updating ALL 6 columns including Mode
        supabase.table("sales").update({
    "product": new_product,
    "quantity": new_qty,
    "price": new_price,
    "status": new_status,
    "mode": new_mode
}).eq("id", row_data["id"]).execute()




        st.success("✅ Updated successfully!")
        st.session_state.edit_row = None
        st.experimental_rerun()

    if cancel_col.button("✖ Cancel"):
        st.session_state.edit_row = None
        st.experimental_rerun()



        # ==========================
#      👇 NEW METRICS
# ==========================
st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
st.subheader("📈 Status Overview")

# ---- CALCULATIONS ----

# Total Cash Revenue
total_cash = today_df[today_df["mode"] == "Cash"]["revenue"].sum()

# Total UPI Revenue
total_upi = today_df[today_df["mode"] == "UPI"]["revenue"].sum()

# Total Revenue (Cash + UPI)
total_revenue = total_cash + total_upi

# Items Sold
total_items = int(today_df["quantity"].sum())

# Defected Items
total_defected = int((today_df["status"] == "Defected").sum())

# ---- 5 Columns Layout ----
colA, colB, colC, colD, colE = st.columns(5)

colA.metric("💵 Total Cash", f"₹{int(total_cash):,}")
colB.metric("📱 Total UPI", f"₹{int(total_upi):,}")
colD.metric("📦 Items Sold", f"{int(total_items):,}")
colE.metric("❌ Defected", f"{int(total_defected):,}")
colC.metric("💰 Total Revenue", f"₹{int(total_revenue):,}")


st.markdown("</div>", unsafe_allow_html=True)


        # ---- BLUE BAR CHART ----
        # ---- MODERN MULTI-COLOR BAR CHART ----
st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
st.subheader("📊 Top Selling Products Today")

top_products = today_df.groupby("product")["revenue"].sum().sort_values(ascending=False)

if not top_products.empty:
    import numpy as np

    colors = plt.cm.tab20(np.linspace(0, 1, len(top_products)))

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.bar(top_products.index, top_products.values, color=colors, 
           edgecolor="black", linewidth=1.5)

    ax.set_title("Top Selling Products", fontsize=18, fontweight="bold")
    ax.set_ylabel("revenue (₹)", fontsize=14)

    plt.xticks(rotation=10, fontsize=12)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='y', linestyle='--', alpha=0.3)

    plt.tight_layout()
    st.pyplot(fig)

st.markdown("</div>", unsafe_allow_html=True)


        

   # ---- AI SUMMARY (PREMIUM UI) ----
st.markdown("""
<div class="premium-card">
    <h2 class="premium-title">🧠 AI Summary</h2>
""", unsafe_allow_html=True)


if st.button("✨ Generate Summary"):
    from openai import OpenAI

    prompt = f"""
    Summarize today's sales ONLY in Indian Rupees (₹). 
    Do NOT use the dollar symbol ($). 
    Use ₹ for every money figure. 
    Here is the data:
    {today_df.to_string(index=False)}
    """

    try:
        ai = OpenAI(api_key=openai.api_key)
        res = ai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        raw_text = res.choices[0].message.content
        safe_html = raw_text.replace("\n", "<br>")

        st.markdown(
            f"""
            <div class="premium-summary-box">
                {safe_html}
            </div>
            """,
            unsafe_allow_html=True
        )

    except Exception as e:
        st.error(f"AI Error: {e}")


st.markdown("</div>", unsafe_allow_html=True)





# ==========================
# FOOTER
# ==========================
st.markdown("""
<div style="text-align:center; color:black; font-weight:600; margin-top:40px;">
    Developed with ❤️ by <b>Taksh and Dhruv</b><br>
    Contact no.- 8445432597 (Taksh) , 9045010252 (Dhruv)<br>
    © Hisaab Kitab
</div>
""", unsafe_allow_html=True)


