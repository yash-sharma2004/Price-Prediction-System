import streamlit as st
import joblib
import pandas as pd

st.title("🚲 Bike Price Prediction")
st.write("Enter your bike details:")

# Data cache ke saath load karein
@st.cache_data
def load_data():
    return pd.read_csv("models/bike_data.csv")

# Model aur preprocessor cache ke saath load karein (baar baar disk se na padhein)
@st.cache_resource
def load_model_and_preprocessor():
    model = joblib.load("models/bike_model.pkl")
    preprocessor = joblib.load("preprocessor.pkl")
    return model, preprocessor

df = load_data()
model, preprocessor = load_model_and_preprocessor()

# Step A: Brand select
brand = st.selectbox(
    "Brand",
    sorted(df['brand'].unique())
)

# Step B: Us brand ki bikes filter
filtered_bikes_df = df[df['brand'] == brand]
bike_name = st.selectbox(
    "Bike Name",
    sorted(filtered_bikes_df['bike_name'].unique())
)

# Step C: Uss exact bike ka power auto-fetch
bike_power_options = sorted(filtered_bikes_df[filtered_bikes_df['bike_name'] == bike_name]['power'].unique())
power = st.selectbox(
    "Power (cc)",
    bike_power_options
)

age = st.number_input(
    "Bike Age (years)",
    min_value=0,
    max_value=30,
    value=5
)

kms_driven = st.number_input(
    "Kms Driven",
    min_value=0,
    max_value=200000,
    value=15000
)

owner = st.selectbox(
    "Owner",
    ["First Owner", "Second Owner", "Third Owner", "Fourth Owner Or More"]
)

city = st.selectbox(
    "City",
    sorted(df['city'].unique())
)

if st.button("🔮 Predict Price"):
    input_df = pd.DataFrame([{
        "brand": brand,
        "bike_name": bike_name,
        "age": age,
        "kms_driven": kms_driven,
        "power": power,
        "owner": owner,
        "city": city
    }])

    # Step 1: Preprocess (transform)
    input_transformed = preprocessor.transform(input_df)

    # Step 2: Predict
    prediction = model.predict(input_transformed)[0]

    st.success(f"Estimated Bike Price: ₹{prediction:,.0f}")
  