import streamlit as st
import requests
import os

# Function to fetch weather data
def get_weather(city, api_key):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "description": data["weather"][0]["description"],
            "icon": data["weather"][0]["icon"]
        }
    else:
        return None

# Streamlit app interface
st.set_page_config(page_title="Bhoomi: Weather Forecasting", page_icon="🌦️", layout="wide")
st.title("Bhoomi: Weather Update")
st.markdown("Get real-time weather updates to make informed agricultural decisions.")

# Sidebar for location input
st.sidebar.header("Enter Location")
city = st.sidebar.text_input("Location", placeholder="e.g., Mumbai")

# Fetch API key from environment variable or hardcode for testing
# api_key = os.getenv("WEATHER_API")
api_key = "6aaae7fd26b0b6de2301c0d68113a578"

# Display weather information
st.subheader("Weather Forecast")
if city:
    with st.spinner("Fetching weather data..."):
        weather_data = get_weather(city, api_key)
    if weather_data:
        col1, col2 = st.columns([1, 4])

        # Display weather icon in the first column
        with col1:
            icon_url = f"http://openweathermap.org/img/wn/{weather_data['icon']}@4x.png"
            st.image(icon_url, width=120)  # Increased icon size for better visibility

        # Display weather details in the second column within a styled container
        with col2:
            st.markdown(
                f"""
                <div style="padding:20px; border-radius:10px; background-color:#f0f2f6; text-align:left;">
                    <h2 style="color:#333; margin-bottom:10px;">Weather in <strong>{weather_data['city']}</strong></h2>
                    <p style="font-size:30px; color:#444; margin:5px 0;"><strong>{weather_data['temperature']} °C 🌡️</strong></p>
                    <p style="font-size:20px; color:#555; margin:5px 0;">💧 <strong>Humidity:</strong> {weather_data['humidity']}%</p>
                    <p style="font-size:20px; color:#555; margin:5px 0;">🌤️ <strong>Condition:</strong> {weather_data['description'].capitalize()}</p>
                </div>
                """, 
                unsafe_allow_html=True
            )
    else:
        st.error("Could not retrieve weather data. Please try again.")
else:
    st.info("Please enter a location in the sidebar to get weather updates.")
