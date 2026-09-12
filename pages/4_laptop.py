import pandas as pd
import numpy as np

import streamlit as st 
import joblib

st.title("💻 Laptop Price Prediction")
st.write("Enter your laptop details:")

@st.cache_data
def  load_data():
    return joblib.load("models/laptop_cleaned_data.pkl")

def load_model():
    model = joblib.load("models/laptop_model.pkl")
    return model

df = load_data()
ml_model = load_model()

# brand
company = st.selectbox(
    "brand",
    sorted(df['Company'].unique())
)

# type of laptop
filtered_laptops_df = df[df['Company'] == company]
type = st.selectbox('Type',filtered_laptops_df['TypeName'].unique())

# Ram
ram = st.selectbox('RAM(in GB)', df['Ram'].unique())

# weight
laptop_weight_options = sorted(filtered_laptops_df['Weight'].unique())
weight = st.number_input('Weight of the Laptop', min_value=min(laptop_weight_options), max_value=max(laptop_weight_options))

# Touchscreen
touchscreen = st.selectbox('Touchscreen',['No','Yes'])

# IPS
ips = st.selectbox('IPS',['No','Yes'])

# screen 

screen_size = st.select_slider(
    "Screen Size",
    options=[11.6, 12.5, 13.3, 14.0, 15.6, 16.0, 17.3, 18.0],
    value=15.6
)

# resolution
resolution = st.selectbox('Screen Resolution',['1920x1080','1366x768','1600x900','3840x2160','3200x1800','2880x1800','2560x1600','2560x1440','2304x1440'])

#cpu

cpu = st.selectbox('CPU',df['Cpu_Name'].unique())

hdd = st.selectbox('HDD(in GB)',[0,128,256,512,1024,2048])

ssd = st.selectbox('SSD(in GB)',[0,8,128,256,512,1024])

gpu_brand = st.selectbox(
    'GPU Brand',
    ['None', 'Intel', 'AMD', 'Nvidia']
)

laptop_os_options = sorted(filtered_laptops_df['OS'].unique())
os = st.selectbox('OS',laptop_os_options)

laptop_hybrid_options = sorted(filtered_laptops_df['Hybrid'].unique())
hybrid = st.selectbox('Hybrid',laptop_hybrid_options)

flash_Storage_options = sorted(filtered_laptops_df['Flash_Storage'].unique())
flash_storage = st.selectbox('Flash Storage', flash_Storage_options)

if st.button('Predict Price'):
    # query
    ppi = None
    if touchscreen == 'Yes':
        touchscreen = 1
    else:
        touchscreen = 0

    if ips == 'Yes':
        ips = 1
    else:
        ips = 0

    # if gpu_brand == "No GPU":
    #     gpu_brand = "Intel"   # integrated graphics
    # else:
    #     gpu_brand = gpu

    X_res = int(resolution.split('x')[0])
    Y_res = int(resolution.split('x')[1])
    ppi = ((X_res**2) + (Y_res**2))**0.5/screen_size
    input_df = pd.DataFrame([{
        "Company": company,
        "TypeName": type,
        "Ram": ram,
        "Weight": weight,
        "TouchScreen": touchscreen,
        "IPS_Panel": ips,
        "ppi": ppi,
        "Cpu_Name": cpu,
        "HDD": hdd,
        "SSD": ssd,
        "Hybrid": hybrid,
        "Flash_Storage": flash_storage,
        "GPU brand": gpu_brand,
        "OS": os
    }])

    st.title("The predicted price of this configuration is   " + str(int(np.exp(ml_model.predict(input_df)[0]))))
         