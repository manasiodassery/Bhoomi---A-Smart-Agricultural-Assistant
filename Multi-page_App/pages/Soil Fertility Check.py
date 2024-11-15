import streamlit as st
import pickle
import pandas as pd
import numpy as np
import plotly.graph_objects as go

def get_clean_data(filepath="C:/Manasi/NMIMS/Manasi/Capstone Project/Agriculture/Bhoomi/Data/soil_fertility.csv"):
    return pd.read_csv(filepath)

def add_sidebar():
    st.sidebar.header("Soil Composition and Properties")
    st.sidebar.write("Adjust each slider to input soil composition values. Each element plays a role in soil fertility.")

    data = get_clean_data()
    slider_labels = [
        ("Nitrogen (N)", "N"), ("Phosphorus (P)", "P"), ("Potassium (K)", "K"),
        ("pH Level", "pH"), ("Electrical Conductivity (EC)", "EC"),
        ("Organic Carbon (OC)", "OC"), ("Sulfur (S)", "S"), 
        ("Zinc (Zn)", "Zn"), ("Iron (Fe)", "Fe"),
        ("Copper (Cu)", "Cu"), ("Manganese (Mn)", "Mn"), ("Boron (B)", "B")
    ]

    input_dict = {}
    for label, key in slider_labels:
        if key not in st.session_state:
            st.session_state[key] = float(data[key].mean())
        
        input_dict[key] = st.sidebar.slider(label, float(data[key].min()), float(data[key].max()), st.session_state[key], help=f"Set the value for {label}")

    if st.sidebar.button("Reset Values"):
        for label, key in slider_labels:
            st.session_state[key] = float(data[key].mean())
    
    return input_dict

def get_scaled_values(input_dict):
    data = get_clean_data()
    X = data[list(input_dict.keys())]
    
    scaled_dict = {key: (value - X[key].min()) / (X[key].max() - X[key].min()) for key, value in input_dict.items()}
    return scaled_dict

def get_radar_chart(input_data):
    input_data = get_scaled_values(input_data)
    categories = list(input_data.keys())

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=list(input_data.values()),
        theta=categories,
        fill='toself',
        name='Current Soil Composition',
        fillcolor='rgba(0,128,0,0.5)',
        line=dict(color='green')
    ))

    optimal_values = [0.7, 0.6, 0.8, 0.5, 0.3, 0.7, 0.6, 0.4, 0.5, 0.2, 0.6, 0.3]
    fig.add_trace(go.Scatterpolar(
        r=optimal_values,
        theta=categories,
        fill='toself',
        name='Optimal Soil Composition',
        fillcolor='rgba(255,165,0,0.5)',
        line=dict(color='orange')
    ))

    standard_range_values = [0.5, 0.4, 0.6, 0.3, 0.2, 0.5, 0.4, 0.3, 0.4, 0.2, 0.5, 0.3]
    fig.add_trace(go.Scatterpolar(
        r=standard_range_values,
        theta=categories,
        fill='toself',
        name='Standard Range',
        fillcolor='rgba(128,128,128,0.3)',
        line=dict(color='gray')
    ))

    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
        showlegend=True,
        title="Soil Composition Radar Chart"
    )
    
    return fig

def add_predictions(input_data):
    try:
        model = pickle.load(open("C:/Manasi/NMIMS/Manasi/Capstone Project/Agriculture/Bhoomi/Model/soil_fertility_model.pkl", "rb"))
        scaler = pickle.load(open("C:/Manasi/NMIMS/Manasi/Capstone Project/Agriculture/Bhoomi/Model/soil_fertility_scaler.pkl", "rb"))

        input_df = pd.DataFrame([input_data], columns=input_data.keys())
        input_array_scaled = scaler.transform(input_df)

        prediction = model.predict(input_array_scaled)[0]

        st.subheader("Soil Fertility Classification")
        
        # Check if prediction is string or integer and map accordingly
        if isinstance(prediction, str):
            fertility_classification = prediction
        else:
            classification_labels = ["Less Fertile", "Fertile", "Highly Fertile"]
            fertility_classification = classification_labels[int(prediction)]
        
        # Updated color mapping with orange for "Fertile"
        color_map = {"Less Fertile": "red", "Fertile": "orange", "Highly Fertile": "green"}

        st.markdown(
            f"<div style='padding:10px; border-radius:5px; background-color:{color_map[fertility_classification]}; text-align:center;'>"
            f"<strong>{fertility_classification}</strong>"
            "</div>", 
            unsafe_allow_html=True
        )
        
    except Exception as e:
        st.error(f"An error occurred during prediction: {e}")
        st.write("Please ensure the model and scaler are correctly loaded and compatible with the input format.")

def main():
    st.set_page_config(
        page_title="Bhoomi: Soil Fertility Classifier",
        layout="wide",
        page_icon="🌱",
        initial_sidebar_state="expanded"
    )
    input_data = add_sidebar()

    with st.container():
        st.title("Bhoomi: Soil Fertility Classifier")
        st.write("Adjust the sliders to reflect the elemental composition of your soil sample and check its fertility level.")

    col1, col2 = st.columns([3, 1])
    with col1:
        radar_chart = get_radar_chart(input_data)
        st.plotly_chart(radar_chart, use_container_width=True)
    with col2:
        add_predictions(input_data)

if __name__ == "__main__":
    main()
