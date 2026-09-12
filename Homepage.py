import streamlit as st

st.set_page_config(
    page_title="Price Predictor",
    page_icon="💰",
    layout="centered",
)

st.title("💰 Price Predictor system")
st.subheader("what would you like to predict")
st.write("select the below and enter its details to predict its estimated price")

col1, col2, col3 = st.columns(3)

with col1:
    st.header("🚗 car")
    st.write("predict the estimate price of car.")
    if  st.button("predict car price",use_container_width=True):
       st.switch_page("pages/2_car.py")
       
with col2:
    st.header("🚲 bike")
    st.write("predict the estimate price of bike.")
    if st.button("predict bike price", use_container_width=True):
        st.switch_page("pages/3_bike.py")

with col3:
    st.header("💻 laptop")
    st.write("predict the estimate price of laptop.")
    if st.button("predict laptop price", use_container_width=True):
        st.switch_page("pages/4_laptop.py")
