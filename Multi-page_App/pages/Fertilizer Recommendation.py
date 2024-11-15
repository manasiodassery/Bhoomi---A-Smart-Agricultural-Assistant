import streamlit as st
import pickle
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from pathlib import Path

# Load data for input ranges with improved path handling
def get_clean_data(filepath=Path("C:/Manasi/NMIMS/Manasi/Capstone Project/Agriculture/Bhoomi/Data/fertilizer_recommendation.csv")):
    try:
        data = pd.read_csv(filepath)
        return data
    except FileNotFoundError:
        st.error(f"Data file not found at {filepath}. Please check the file path.")
        return None

# Load model and label encoder
def load_model_components():
    try:
        model = pickle.load(open(Path("C:/Manasi/NMIMS/Manasi/Capstone Project/Agriculture/Bhoomi/Model/fertilizer_recommendation_model.pkl"), "rb"))
        label_encoder = pickle.load(open(Path("C:/Manasi/NMIMS/Manasi/Capstone Project/Agriculture/Bhoomi/Model/fertilizer_recommendation_encoder.pkl"), "rb"))
        return model, label_encoder
    except FileNotFoundError:
        st.error("Model or label encoder file not found. Please check the file paths.")
        return None, None
    except Exception as e:
        st.error(f"An error occurred while loading the model components: {e}")
        return None, None

# Sidebar for user inputs
def add_sidebar():
    st.sidebar.header("🌱 Fertilizer Recommendation Inputs")
    st.sidebar.markdown("Adjust the field parameters to get a tailored fertilizer recommendation.")
    data = get_clean_data()
    if data is None:
        return None

    slider_labels = [
        ("Nitrogen (N)", "Nitrogen"),
        ("Phosphorus (P)", "Phosphorous"), 
        ("Potassium (K)", "Potassium"),
        ("Temperature (°C)", "Temparature"),
        ("Humidity (%)", "Humidity "),
        ("Moisture Level (%)", "Moisture")
    ]

    input_dict = {}
    for label, key in slider_labels:
        if key in data.columns:
            input_dict[key] = st.sidebar.slider(label, float(data[key].min()), float(data[key].max()), float(data[key].mean()))
        else:
            st.error(f"Column '{key}' not found in the dataset. Please verify column names.")

    if 'Crop Type' in data.columns:
        input_dict['Crop Type'] = st.sidebar.selectbox("Crop Type", data['Crop Type'].unique(), help="Select the crop currently planted")
    else:
        st.error("Column 'Crop Type' not found in the dataset. Please verify column names.")
    
    if 'Soil Type' in data.columns:
        input_dict['Soil Type'] = st.sidebar.selectbox("Soil Type", data['Soil Type'].unique(), help="Select the type of soil in the field")
    else:
        st.error("Column 'Soil Type' not found in the dataset. Please verify column names.")

    return input_dict

# Add a color-coded bar chart to show current input levels
def add_bar_chart(input_data):
    if input_data is None:
        return
    
    parameters = list(input_data.keys())
    values = [input_data[param] for param in parameters if isinstance(input_data[param], (int, float))]
    
    fig = go.Figure(data=[go.Bar(name='Current Conditions', x=parameters[:len(values)], y=values, marker_color='lightgreen')])
    fig.update_layout(
        title="Current Input Levels",
        xaxis_title="Parameters",
        yaxis_title="Value",
        yaxis=dict(range=[0, max(values) * 1.2]),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Prediction function to recommend fertilizer
def add_predictions(input_data):
    model, label_encoder = load_model_components()
    if model is None or label_encoder is None or input_data is None:
        return

    input_df = pd.DataFrame([input_data])
    input_df = pd.get_dummies(input_df, columns=['Crop Type', 'Soil Type'], drop_first=True)

    model_features = model.feature_names_in_
    input_df = input_df.reindex(columns=model_features, fill_value=0)

    try:
        prediction = model.predict(input_df)[0]
        recommended_fertilizer = label_encoder.inverse_transform([prediction])[0]
        st.subheader(" Recommended Fertilizer")
        st.success(f"Based on the input conditions, the recommended fertilizer is **{recommended_fertilizer}**.")
    except Exception as e:
        st.error(f"An error occurred during prediction: {e}")

# Main function to render the app
def main():
    st.set_page_config(
        page_title="Bhoomi: Fertilizer Recommendation",
        layout="wide",
        page_icon="🌱",
        initial_sidebar_state="expanded"
    )
    st.title("Bhoomi: Fertilizer Recommendation System")
    st.markdown("**Optimize your crop growth** by receiving customized fertilizer recommendations based on current field conditions.")

    input_data = add_sidebar()
    if input_data is not None:
        col1, col2 = st.columns([3, 1])
        with col1:
            add_bar_chart(input_data)  
        with col2:
            add_predictions(input_data)

if __name__ == "__main__":
    main()
