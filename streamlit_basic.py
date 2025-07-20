import streamlit as st
st.header("Welcome to BMI calculator App")
col1,col2 = st.columns(2)
with col1:
    weight = st.text_input("Enter weight in kg")
with col2:
    height = st.text_input("Enter height in feet")
if weight != '' and height != '':
    bmi = float(weight) / ((float(height) * 3.28) ** 2)
    if bmi < 16:
        st.error("You are extremely underweight")
    elif 16 <= bmi < 18.5:
        st.warning("You are underweight")
    elif 18.5 <= bmi < 25:
        st.success("You are healthy")
    elif 25 <= bmi < 30:
        st.info("You are overweight")
    else:
        st.error("You are extermely overweight")
