import streamlit as st 
import joblib as jlib
import numpy as np
model = jlib.load('titanic_prediction_model.joblib')
st.title("Titanic Survival Prediction")
gender = {
    'Male':1,
    'Female':0
}
col1, col2 = st.columns(2)
with col1:
    p_class = st.slider('Enter P_class', 1,3,1)
    age = st.text_input('Enter Age')
    sex = st.selectbox('Enter Sex', ['Male','Female'])
with col2:
    sibsp = st.slider('Enter Sibsp',1,5,2)
    parch = st.slider('Enter Parch',0,6,3)
    fare = st.text_input('Enter Fare')
predict = st.button("Predict Survival")
if predict:
    p_sex = gender[sex]
    feature_input = np.array([int(p_class),p_sex,float(age),int(sibsp),int(parch),float(fare)])
    predicted = model.predict(feature_input.reshape(1,-1))
    if predicted[0] == 1:
        st.write("Survived")
    else:    
        st.write("Not Survived")