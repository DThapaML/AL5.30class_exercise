import streamlit as st
import joblib
target_name = ['setosa', 'versicolor', 'virginica']
st.header("TYPE OF IRIS FLOWER PREDICTION MODEL")
sl = st.text_input('Enter sepal length (cm)')
sw = st.text_input('Enter sepal width (cm)')
pl = st.text_input('Enter petal length (cm)')
pw = st.text_input('Enter petal width (cm)')
model = joblib.load('iris_flower_classification.joblib')
button_preseed = st.button('Predict Flower')
if sl is not None and sw is not None and pl is not None and pw is not None:
    if button_preseed:
        predict = model.predict([[float(sl),float(sw),float(pl),float(pw)]])
        predicted_flower = target_name[predict[0]]
        st.success(f'The flower is {predicted_flower}')