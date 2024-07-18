import streamlit as st
import pickle
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier

# Load the RandomForestClassifier model
with open('random_forest_model.pkl', 'rb') as model_file:
    loaded_model = pickle.load(model_file)

# Define treatment mapping
treatment_mapping = {'Medicine': 1, 'Surgery': 0}

# Streamlit app
st.title('Prediction model for Recurrence of Cardiovascular Disease')

# User inputs
st.subheader('Enter Patient Information:')
gender = st.radio("Gender", ('Female', 'Male'))
age = st.number_input("Age", step=1)
current_smoking = st.radio("Are you currently smoking?", ('No', 'Yes'))
diabetes = st.radio("Do you have diabetes?", ('No', 'Yes'))
bmi = st.number_input("BMI", step=1)
systolic = st.number_input("Systolic Blood Pressure", step=1)
diastolic = st.number_input("Diastolic Blood Pressure", step=1)
cholesterol = st.number_input("Cholesterol level", step=1)
atrial_fibrillation = st.radio("Do you have Atrial Fibrillation?", ('No', 'Yes'))
vascular_beds = st.number_input("Number of Vascular Beds", min_value=0, step=1)
cardio_event_past_year = st.radio("Did you have a Cardiovascular Event in the Past Year?", ('No', 'Yes'))

# Select treatment type
cardio_treatment_type = st.selectbox("Select Type of Cardiovascular Treatment:", list(treatment_mapping.keys()))

# Predict button
if st.button('Predict'):
    # Convert inputs to numeric values
    gender = 1 if gender == 'Male' else 0
    current_smoking = 1 if current_smoking == 'Yes' else 0
    diabetes = 1 if diabetes == 'Yes' else 0
    atrial_fibrillation = 1 if atrial_fibrillation == 'Yes' else 0
    cardio_event_past_year = 1 if cardio_event_past_year == 'Yes' else 0
    cardio_treatment_type = treatment_mapping[cardio_treatment_type]
    
    # Ensure numerical inputs are not empty and convert them to appropriate types
    age = int(age) if age else 0
    bmi = float(bmi) if bmi else 0
    systolic = float(systolic) if systolic else 0
    diastolic = float(diastolic) if diastolic else 0
    cholesterol = float(cholesterol) if cholesterol else 0
    vascular_beds = int(vascular_beds) if vascular_beds else 0
    
    # Prepare sample data for prediction
    sample_data = np.array([[gender, age, current_smoking, diabetes, bmi, systolic, diastolic, cholesterol,
                             atrial_fibrillation, vascular_beds, cardio_event_past_year,
                             cardio_treatment_type]])
    
    # Make predictions
    prediction = loaded_model.predict(sample_data)
    
    # Display prediction result
    st.write("Prediction (0=No recurrence, 1=recurrence): ", int(prediction[0]))
