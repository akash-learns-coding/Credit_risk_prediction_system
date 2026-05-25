import streamlit as st
import re

st.set_page_config(page_title="Creditworthiness Prediction", page_icon="💳", layout="centered")

# Custom CSS (🔥 MAGIC HERE)
# -------------------------
st.markdown("""
    <style>

    /* Background */
    .stApp {
        background: linear-gradient(135deg, #0f172a, #1e293b);
        color: white;
    }

    /* Card Style */
    .card {
        background-color: #1e293b;
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.3);
        transition: 0.3s;
    }

    .card:hover {
        transform: scale(1.02);
        box-shadow: 0 15px 35px rgba(0,0,0,0.5);
    }

    /* Input Fields */
    .stTextInput input {
        border-radius: 10px;
        border: 2px solid #334155;
        padding: 10px;
        transition: 0.3s;
    }

    .stTextInput input:hover {
        border-color: #38bdf8;
        box-shadow: 0 0 10px rgba(56,189,248,0.4);
    }

    /* Button */
    .stButton button {
        background: linear-gradient(90deg, #38bdf8, #6366f1);
        color: white;
        border-radius: 10px;
        padding: 10px 25px;
        font-weight: bold;
        border: none;
        transition: 0.3s;
    }

    .stButton button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 15px rgba(99,102,241,0.6);
    }

    /* Title Animation */
    h1 {
        text-align: center;
        color: #38bdf8;
        animation: fadeIn 1.2s ease-in-out;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    </style>
""", unsafe_allow_html=True)

# -------------------------
# UI Layout
# -------------------------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.title("💳 Creditworthiness Prediction")
st.write("Welcome to the Creditworthiness Prediction App!")

name = st.text_input("Enter your Name:")
phone = st.text_input("Enter your Phone Number (10 digits):")

def is_valid_phone(phone_number):
    return bool(re.fullmatch(r"[0-9]{10}", phone_number))

if st.button("Log in"):
    if not name.strip():
        st.error("Please enter your name.")
    elif not is_valid_phone(phone):
        st.error("Invalid phone number! Enter exactly 10 digits.")
    else:
        # ✅ SAVE DATA IN SESSION
        st.session_state["logged_in"] = True
        st.session_state["user_name"] = name
        st.session_state["phone"] = phone

        st.success(f"✅ Welcome, {name}! Redirecting...")
        st.balloons()

        # ✅ REDIRECT
        st.switch_page("pages/prediction_page.py")
