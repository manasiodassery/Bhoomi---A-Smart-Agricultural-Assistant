import streamlit as st
from PIL import Image

# Set page configuration
st.set_page_config(page_title="Bhoomi: A Smart Agricultural Assistant", page_icon="🌱", layout="wide")

# Display header and logo image
logo = Image.open("C:/Manasi/NMIMS/Manasi/Capstone Project/Agriculture/Bhoomi/Image/Bhoomi.png")
st.image(logo, width=100)
st.title("🌾 Bhoomi: A Smart Agricultural Assistant 🌾")
st.markdown("### Empowering Farmers with Data-Driven Insights and Smart Farming Tools")

# Brief introduction
st.markdown("""
Welcome to **Bhoomi**, your smart agricultural assistant designed to provide actionable insights and support sustainable farming. Bhoomi brings together multiple tools into a single platform, offering real-time recommendations for crop selection, fertilizer application, irrigation management, price forecasting, soil analysis, and access to government schemes. Use the sidebar to explore each feature.
""")

# Create columns for feature descriptions
st.write("### Explore Bhoomi's Key Features:")
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("🌾 Crop Recommendation")
    st.write("Get the best crop recommendations based on soil, climate, and environmental factors to optimize yields.")

    st.subheader("💧 Irrigation Management")
    st.write("Optimize water usage with real-time, weather-adjusted irrigation advice tailored to your farm’s needs.")

with col2:
    st.subheader("🌱 Fertilizer Recommendation")
    st.write("Receive precise fertilizer recommendations tailored to your crop and soil conditions for optimal growth.")

    st.subheader("📈 Price Forecasting")
    st.write("Forecast commodity prices and gain insights to maximize profitability in the market.")

with col3:
    st.subheader("🌍 Government Schemes")
    st.write("Access information on government schemes, subsidies, and support available for farmers.")

    st.subheader("🤖 Smart Farming Information")
    st.write("Explore FAQs and learn about smart farming practices, precision agriculture, and the latest technologies.")

# Divider line
st.markdown("---")

# Chatbot introduction
st.write("### 💬 Need Assistance? Chat with Bhoomi!")
st.markdown("""
Get instant answers to your farming-related queries with Bhoomi’s AI-powered chatbot. Simply type your questions, and our intelligent assistant will provide helpful responses based on the latest agricultural information and best practices.
""")

# Footer or additional information
st.markdown("""
---
**Bhoomi: Empowering Agriculture for a Sustainable Future**
""")
