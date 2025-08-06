import streamlit as st
import joblib
import numpy as np
model = joblib.load('breast_detection.joblib')
scalar = joblib.load('scalar_breast_detection.joblib')
encoder = joblib.load('label_encoder.joblib')
st.title("Breast Prediction Application")
input = ['radius_mean', 'texture_mean', 'perimeter_mean', 'area_mean',
       'smoothness_mean', 'compactness_mean', 'concavity_mean',
       'concave points_mean', 'symmetry_mean', 'fractal_dimension_mean',
       'radius_se', 'texture_se', 'perimeter_se', 'area_se', 'smoothness_se',
       'compactness_se', 'concavity_se', 'concave points_se', 'symmetry_se',
       'fractal_dimension_se', 'radius_worst', 'texture_worst',
       'perimeter_worst', 'area_worst', 'smoothness_worst',
       'compactness_worst', 'concavity_worst', 'concave points_worst',
       'symmetry_worst', 'fractal_dimension_worst']
data = dict()
col = st.columns(4)
for num,i in enumerate(input):
    with col[num % 4]:
        value = st.text_input(f'Enter {i}')
        data[i] = value
button = st.button("Predict Breast Cancer")
if button:
    fetch_input = np.array([float(v) for v in data.values()])
    fetch_input = fetch_input.reshape(1,-1)
    scaled_input = scalar.transform(fetch_input)
    predicted = model.predict(scaled_input)
    encoded_output = encoder.inverse_transform(predicted)
    if encoded_output[0] == 'M':
        st.write("94% its Diagnosis: M - Malignant")
    else:
        st.write("94% its Diagnosis: B - Benign")


