import streamlit as st
import requests
import pandas as pd
import datetime

# Set up the main header and page configuration
st.set_page_config(page_title="Bhoomi: Smart Irrigation System", layout="wide", page_icon="🌱")
st.title("🌱 Bhoomi: Smart Irrigation System")
st.markdown("Monitor and manage irrigation with real-time data and weather adjustments for optimal water usage.")

# Load data
data = pd.read_csv('C:/Manasi/NMIMS/Manasi/Capstone Project/Agriculture/Bhoomi/Data/Irrigation_usage/data.csv')
demo1 = pd.read_csv('C:/Manasi/NMIMS/Manasi/Capstone Project/Agriculture/Bhoomi/Data/Irrigation_usage/demo1.csv', header=None)
moisture_days = pd.read_csv('C:/Manasi/NMIMS/Manasi/Capstone Project/Agriculture/Bhoomi/Data/Irrigation_usage/moisture_days.csv')
moisture_time = pd.read_csv('C:/Manasi/NMIMS/Manasi/Capstone Project/Agriculture/Bhoomi/Data/Irrigation_usage/moisture_time.csv')

# Define thresholds and settings
daily_moisture_threshold = 500
daily_drop_threshold = 50
time_based_threshold = 400
preferred_irrigation_time = [6, 18]  # Morning and evening preferred times
API_KEY = '6aaae7fd26b0b6de2301c0d68113a578'  # Replace with your OpenWeather API key

# Sidebar for user input
st.sidebar.header("Irrigation System Settings")
st.sidebar.markdown("### 🌍 Location Settings")
city = st.sidebar.text_input("Enter location", "Mumbai")

# DataFrame to store notifications
notifications = []

# Function to get weather condition using OpenWeather API
def get_weather_condition(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"
    response = requests.get(url)
    
    if response.status_code == 200:
        weather_data = response.json()
        weather_main = weather_data.get('weather', [{}])[0].get('main', "").lower()
        return "rain" in weather_main
    else:
        st.warning("Could not retrieve weather data. Check city name or API key.")
        return False

# Function to adjust thresholds based on weather
def adjust_for_weather(city):
    if get_weather_condition(city):
        st.info("💧 Rain expected - adjusting irrigation thresholds.")
        return daily_moisture_threshold - 50
    else:
        st.info("☀️ No rain expected.")
        return daily_moisture_threshold

# Function to log notifications
def log_notification(day=None, time=None, reason=None, duration=None):
    if day is not None:
        notifications.append({"Day/Time": f"Day {day}", "Reason": reason, "Watering Duration (s)": duration})
    else:
        notifications.append({"Day/Time": f"Time {time}h", "Reason": reason, "Watering Duration (s)": duration})

# Function to calculate watering duration
def calculate_watering_duration(current_level, optimal_level=800):
    return max(0, optimal_level - current_level)

# Daily moisture check
def check_daily_moisture(city, moisture_days):
    adjusted_threshold = adjust_for_weather(city)
    for i in range(1, len(moisture_days)):
        moisture_level = moisture_days.loc[i, 'moisture']
        daily_drop = moisture_days.loc[i, 'moisture'] - moisture_days.loc[i - 1, 'moisture']
        
        if moisture_level < adjusted_threshold or daily_drop < -daily_drop_threshold:
            reason = "Low moisture" if moisture_level < adjusted_threshold else "Significant drop"
            duration = calculate_watering_duration(moisture_level)
            log_notification(day=moisture_days.loc[i, 'days'], reason=reason, duration=duration)

# Time-based moisture check
def check_time_based_moisture(moisture_time):
    for i, row in moisture_time.iterrows():
        moisture_level = row['Moisture']
        time_of_day = row['time']
        
        if moisture_level < time_based_threshold or time_of_day in preferred_irrigation_time:
            reason = "Low moisture" if moisture_level < time_based_threshold else "Preferred time"
            duration = calculate_watering_duration(moisture_level)
            log_notification(time=time_of_day, reason=reason, duration=duration)

# Button to run checks and display results
st.markdown("### Irrigation Notifications")
if st.button("Run Irrigation Checks"):
    # Clear previous notifications
    notifications.clear()
    
    # Run daily and time-based moisture checks
    check_daily_moisture(city, moisture_days)
    check_time_based_moisture(moisture_time)
    
    # Display the notifications table with enhancements
    st.subheader("Irrigation Notifications")
    if notifications:
        notifications_df = pd.DataFrame(notifications)
        st.dataframe(notifications_df.style.format({"Watering Duration (s)": "{:.2f}"}))
    else:
        st.write("✅ No irrigation notifications for today.")

# Additional footer with last update information
st.markdown("---")
st.markdown(f"**Last Checked:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
st.caption("Make sure to update weather and moisture data regularly for accurate recommendations.")
