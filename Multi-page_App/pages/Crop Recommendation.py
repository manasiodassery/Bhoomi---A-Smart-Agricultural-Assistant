import streamlit as st
import pickle
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Function to load and clean data
def get_clean_data(filepath="C:/Manasi/NMIMS/Manasi/Capstone Project/Agriculture/Bhoomi/Data/crop_recommendation.csv"):
    return pd.read_csv(filepath)

# Function to add sidebar inputs with sliders and tooltips
def add_sidebar():
    st.sidebar.header("🌱 Crop Recommendation Inputs")
    st.sidebar.markdown("Adjust the parameters below to reflect your field's soil and weather conditions.")
    data = get_clean_data()
    
    # Slider labels and keys
    slider_labels = [
        ("Nitrogen (N)", "N", "Essential nutrient for plant growth."),
        ("Phosphorus (P)", "P", "Vital for root development."),
        ("Potassium (K)", "K", "Improves overall plant health."),
        ("Temperature (°C)", "temperature", "Optimal temperature for crop growth."),
        ("Humidity (%)", "humidity", "Ideal moisture level in the air."),
        ("pH Level", "ph", "Indicates soil acidity or alkalinity."),
        ("Rainfall (mm)", "rainfall", "Amount of rainfall received.")
    ]
    
    input_dict = {}
    for label, key, description in slider_labels:
        st.sidebar.markdown(f"**{label}**")
        input_dict[key] = st.sidebar.slider(
            label, float(data[key].min()), float(data[key].max()), float(data[key].mean()), help=description
        )
    return input_dict

# Function to scale input values
def get_scaled_values(input_dict):
    data = get_clean_data()
    X = data[list(input_dict.keys())]
    return {key: (value - X[key].min()) / (X[key].max() - X[key].min()) for key, value in input_dict.items()}

# Function to display a bar chart of input values without color coding
def get_bar_chart(input_data):
    scaled_input = get_scaled_values(input_data)
    categories = list(scaled_input.keys())
    input_values = list(scaled_input.values())

    fig = go.Figure(data=[go.Bar(x=categories, y=input_values)])
    fig.update_layout(
        title="Current Input Conditions",
        xaxis_title="Metrics",
        yaxis_title="Scaled Values (0-1)",
        yaxis=dict(range=[0, 1]),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)"
    )
    return fig

# Function to load model, predict, and display recommended crop
def add_predictions(input_data):
    try:
        model = pickle.load(open("C:/Manasi/NMIMS/Manasi/Capstone Project/Agriculture/Bhoomi/Model/crop_recommendation_model.pkl", "rb"))
        scaler = pickle.load(open("C:/Manasi/NMIMS/Manasi/Capstone Project/Agriculture/Bhoomi/Model/crop_recommendation_scaler.pkl", "rb"))
        label_encoder = pickle.load(open("C:/Manasi/NMIMS/Manasi/Capstone Project/Agriculture/Bhoomi/Model/crop_recommendation_encoder.pkl", "rb"))

        input_df = pd.DataFrame([input_data], columns=input_data.keys())
        input_array_scaled = scaler.transform(input_df)
        prediction = model.predict(input_array_scaled)
        predicted_crop = label_encoder.inverse_transform(prediction)[0]

        # Display crop recommendation with styled HTML
        st.subheader("Recommended Crop")
        st.write("Based on the input conditions, the recommended crop is:")
        st.markdown(
            f"""
            <div style="background-color:#4CAF50; padding:15px; border-radius:10px;">
                <h3 style="color:white; text-align:center; margin:0;">{predicted_crop}</h3>
            </div>
            """,
            unsafe_allow_html=True
        )
    except Exception as e:
        st.error(f"An error occurred during prediction: {e}")

# Main function to organize layout and display elements
def main():
    st.set_page_config(page_title="Bhoomi: Crop Recommendation", layout="wide", page_icon="🌾", initial_sidebar_state="expanded")

    st.title("🌾 Bhoomi: Crop Recommendation System")
    st.write("Adjust the sliders to reflect the soil and weather conditions of your field to receive a recommended crop.")

    input_data = add_sidebar()

    col1, col2 = st.columns([3, 1])
    with col1:
        bar_chart = get_bar_chart(input_data)
        st.plotly_chart(bar_chart, use_container_width=True)
    with col2:
        add_predictions(input_data)

if __name__ == "__main__":
    main()
