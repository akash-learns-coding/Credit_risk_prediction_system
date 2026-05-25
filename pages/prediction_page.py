import streamlit as st
import pandas as pd
import joblib 

st.set_page_config(page_title="Prediction Page", page_icon="📊", layout="centered")


st.markdown("""
<style>

/* Background */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0f172a, #1e293b);
}

/* Main container */
[data-testid="stVerticalBlock"] {
    background: rgba(30, 41, 59, 0.75);
    padding: 25px;
    border-radius: 15px;
    backdrop-filter: blur(8px);
    box-shadow: 0 10px 25px rgba(0,0,0,0.4);
}

/* Buttons */
.stButton > button {
    background: linear-gradient(90deg, #38bdf8, #6366f1);
    color: white;
    border-radius: 10px;
    font-weight: bold;
    border: none;
    transition: all 0.3s ease;
}

/* Button Hover ✅ WORKS */
.stButton > button:hover {
    transform: scale(1.05);
    box-shadow: 0 0 20px rgba(99,102,241,0.7);
}

/* Input Boxes */
[data-testid="stNumberInput"] input {
    border-radius: 10px;
    border: 2px solid #334155;
    transition: 0.3s;
}

/* Input Hover ✅ WORKS */
[data-testid="stNumberInput"] input:focus {
    border-color: #38bdf8;
    box-shadow: 0 0 10px rgba(56,189,248,0.5);
}

/* Slider */
[data-testid="stSlider"] {
    padding-top: 10px;
}

/* Title */
h1 {
    color: #38bdf8;
    text-align: center;
}

</style>
""", unsafe_allow_html=True)


# 🔒 BLOCK DIRECT ACCESS
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.error("🚨 Please log in first from the Login Page.")
    st.stop()

st.title("📊 Creditworthiness Prediction")

#  READ DATA FROM SESSION
st.write(f"Hello, **{st.session_state['user_name']}** 👋")
st.write(f"Your phone number: {st.session_state['phone']}")

age = st.number_input("Enter your Age", min_value=18, max_value=100, step=1)
#credit_amount = st.number_input("Enter Credit Amount ($)", min_value=1000, max_value=100000, step=100)
credit_amount = st.number_input("Enter Credit Amount ($)", min_value=0)

#duration = st.slider("Loan Duration (months)", min_value=5, max_value=72, step=6)
duration = st.slider("Loan Duration (months)", 1, 120)

sex = st.radio("Select your Sex:", ["Male", "Female"])
housing = st.radio("Select Housing Type:", ["Own", "Rent", "Free"])
purpose = st.selectbox(
    "Select Loan Purpose:",
    ["Radio/TV", "Education", "Car", "Business", "Furniture/Equipment"]
)
saving_account = st.selectbox(
    "Saving Account Status:",
    ["little", "moderate", "rich", "unknown"]
)

checking_account = st.selectbox(
    "Checking Account Status:",
    ["little", "moderate", "rich", "unknown"]
)

#if st.button("Predict Creditworthiness"):
   # if credit_amount < 4000 and duration <= 24:
 #       result = "✅ Eligible (Good Credit)"
  #  else:
   #     result = "❌ Not Eligible (Bad Credit)"

    #st.subheader("Prediction Result")
    #st.write(result)

#    st.write("### Entered Details")
 #   st.write(f"- Age: {age}")
  #  st.write(f"- Credit Amount: ${credit_amount}")
   # st.write(f"- Duration: {duration} months")
    #st.write(f"- Sex: {sex}")
    #st.write(f"- Housing: {housing}")
    #st.write(f"- Purpose: {purpose}")

if st.button("Predict Creditworthiness"):

    input_data = pd.DataFrame([{
        "Age": age,
        "Sex": sex,
        "Housing": housing,
        "Saving accounts": saving_account,
        "Checking account": checking_account,
        "Credit amount": credit_amount,
        "Duration": duration,
        "Purpose": purpose
    }])
    def load_model():
     return joblib.load("credit_risk_model.pkl")

    model = load_model()
    prediction = model.predict(input_data)[0]

    if prediction == 1:
        result = "✅ Eligible (Good Credit)"
    else:
        result = "❌ Not Eligible (Bad Credit)"

    st.subheader("Prediction Result")
    st.success(result)


if st.button("Logout"):
    st.session_state.clear()
    st.switch_page("welcome.py")
