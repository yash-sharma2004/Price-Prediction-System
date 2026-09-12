import streamlit as st 
import joblib
import pandas as pd


st.title("🚗 Car Price Prediction")
st.write("Enter your car details:")

@st.cache_data
def load_data():
    return pd.read_csv("models/Cleaned_car_data.csv")


@st.cache_resource
def load_model():
    return joblib.load("models/car_pipeline.pkl")


df = load_data()
ml_model = load_model()

# select car brand
brand = st.selectbox("Brand", sorted(df["brand"].unique()))

# select car name based on brand
filtered_cars_df = df[df["brand"] == brand]
car_model = st.selectbox("Car Name", sorted(filtered_cars_df["model"].unique()))

model_df = filtered_cars_df[filtered_cars_df["model"] == car_model]

# car engine — genuine standard engine for the selected model
car_power_options = sorted(model_df["engine"].unique())
car_power = st.selectbox("Engine (cc)", car_power_options)

# car transmission type
available_transmissions = sorted(model_df["transmission"].unique())
transmission = st.selectbox(
    "Transmission Type", 
    available_transmissions if len(available_transmissions) > 0 else ["Manual", "Automatic"]
)

# --- fuel type auto-logic based on engine and model specs ---
available_fuels = sorted(model_df["fuel_type"].unique())
if car_power == 0 or "Electric" in available_fuels:
    fuel_type = st.selectbox("Fuel Type", ["Electric"], disabled=True)
elif len(available_fuels) > 0:
    fuel_type = st.selectbox("Fuel Type", available_fuels)
else:
    fuel_type = st.selectbox("Fuel Type", ["Petrol", "Diesel", "CNG", "LPG"])

# --- seating capacity: accurate seats from clean dataset ---
seat_options = sorted(model_df["Seats"].unique())
Seats = st.selectbox("Seating Capacity", seat_options)

# kms driven
kms_driven = st.number_input("Kms Driven", min_value=100, max_value=200000, value=15000)

# car age
age = st.number_input("Car Age (years)", min_value=1, max_value=30, value=5)

# ownership
ownership = st.selectbox(
    "Ownership",
    ['1st Owner', '2nd Owner', '3rd Owner', '4th Owner', '5th Owner']
)

is_ev = 1 if fuel_type == "Electric" else 0

if st.button("predict price"):
    input_df = pd.DataFrame([{
        "brand": brand,
        "model": car_model,
        "engine": car_power,
        "transmission": transmission,
        "fuel_type": fuel_type,
        "Seats": Seats,
        "kms_driven": kms_driven,
        "age": age,
        "ownership": ownership,
        "is_ev": is_ev
    }])

    prediction = ml_model.predict(input_df)

    st.success(f"Estimated Car Price: ₹{prediction[0]:,.0f}")