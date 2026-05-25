# app.py
import streamlit as st
import joblib  as jb
import numpy as np
import pandas as pd

# -----------------------------
# Load the trained pipeline
# -----------------------------
@st.cache_resource
def load_model():
    return jb.load("credit_model.pkl")  # this should be your saved pipeline

model = load_model()

# -----------------------------
# Streamlit App UI
# -----------------------------
st.set_page_config(page_title="Creditworthiness Prediction", page_icon="💳", layout="centered")

st.title("💳 Creditworthiness Prediction App")
st.markdown("Enter user details to check creditworthiness (Trust Score).")

# -----------------------------
# Sidebar for threshold control
# -----------------------------
st.sidebar.header("⚙️ Settings")
threshold = st.sidebar.slider("Decision Threshold", 0.0, 1.0, 0.5, 0.01)
st.sidebar.write(f"If probability > {threshold:.2f}, credit is APPROVED")

# -----------------------------
# Collect user inputs
# -----------------------------
st.header("📝 User Information")

col1, col2 = st.columns(2)

with col1:
    age = st.number_input("Age", min_value=18, max_value=100, value=30)
    duration = st.number_input("Duration (months)", min_value=4, max_value=72, value=24)
    credit_amount = st.number_input("Credit Amount", min_value=100, max_value=20000, value=2000)

with col2:
    sex = st.selectbox("Sex", ["male", "female"])
    housing = st.selectbox("Housing", ["own", "rent", "free"])
    saving_accounts = st.selectbox("Saving accounts", ["little", "moderate", "quite rich", "rich", "missing"])
    checking_account = st.selectbox("Checking account", ["little", "moderate", "rich", "missing"])
    purpose = st.selectbox("Purpose", ["car", "furniture/equipment", "radio/TV", "education", "business", "domestic appliances", "repairs", "vacation/others"])

# -----------------------------
# Prepare input dataframe
# -----------------------------
input_data = pd.DataFrame({
    "Age": [age],
    "Duration": [duration],
    "Credit amount": [credit_amount],
    "Sex": [sex],
    "Housing": [housing],
    "Saving accounts": [saving_accounts],
    "Checking account": [checking_account],
    "Purpose": [purpose]
})

# -----------------------------
# Prediction
# -----------------------------
if st.button("🔮 Predict Creditworthiness"):
    proba = model.predict_proba(input_data)[:, 1][0]  # probability of BAD credit risk
    trust_score = 1 - proba  # invert: higher = more trustworthy

    st.subheader("📊 Results")
    st.metric(label="Trust Score", value=f"{trust_score*100:.2f}%")

    if trust_score > threshold:
        st.success("✅ Credit Approved")
    else:
        st.error("❌ Credit Denied")

    # Extra: Show raw probability
    with st.expander("See model details"):
        st.write(f"Bad Credit Probability: {proba:.3f}")
        st.write(f"Threshold used: {threshold:.2f}")
