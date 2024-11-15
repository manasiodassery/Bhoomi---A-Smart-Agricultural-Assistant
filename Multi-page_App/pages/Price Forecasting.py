import streamlit as st
import joblib
import pandas as pd

# Set page configuration
st.set_page_config(
    page_title="Bhoomi: Crop Price Forecast",
    layout="wide",
    page_icon="📈",
    initial_sidebar_state="expanded"
)

# Load data from the CSV file
@st.cache_data
def load_data():
    data = pd.read_csv('C:/Manasi/NMIMS/Manasi/Capstone Project/Agriculture/Bhoomi/Data/price_forecasting.csv')
    return data

agri_data = load_data()

# Load Encoders and Model with caching
@st.cache_resource
def load_model_and_encoders():
    model = joblib.load("C:/Manasi/NMIMS/Manasi/Capstone Project/Agriculture/Bhoomi/Model/price_forecasting_model.joblib")
    encoders = {
        "State": joblib.load("C:/Manasi/NMIMS/Manasi/Capstone Project/Agriculture/Bhoomi/Model/State_encoder.joblib"),
        "District": joblib.load("C:/Manasi/NMIMS/Manasi/Capstone Project/Agriculture/Bhoomi/Model/District_encoder.joblib"),
        "Market": joblib.load("C:/Manasi/NMIMS/Manasi/Capstone Project/Agriculture/Bhoomi/Model/Market_encoder.joblib"),
        "Commodity": joblib.load("C:/Manasi/NMIMS/Manasi/Capstone Project/Agriculture/Bhoomi/Model/Commodity_encoder.joblib"),
        "Variety": joblib.load("C:/Manasi/NMIMS/Manasi/Capstone Project/Agriculture/Bhoomi/Model/Variety_encoder.joblib"),
        "Grade": joblib.load("C:/Manasi/NMIMS/Manasi/Capstone Project/Agriculture/Bhoomi/Model/Grade_encoder.joblib")
    }
    return model, encoders

model, encoders = load_model_and_encoders()

# Sidebar for user input with cascading dropdowns
def add_sidebar():
    st.sidebar.header("Input Crop and Market Features")
    st.sidebar.markdown("Please select the attributes below to forecast the crop price.")

    # State selection
    state = st.sidebar.selectbox("State", agri_data['State'].unique())
    
    # Filter districts based on the selected state
    filtered_data = agri_data[agri_data['State'] == state]
    district = st.sidebar.selectbox("District", filtered_data['District'].unique())
    
    # Filter markets based on the selected district
    filtered_data = filtered_data[filtered_data['District'] == district]
    market = st.sidebar.selectbox("Market", filtered_data['Market'].unique())
    
    # Filter commodities based on the selected market
    commodity = st.sidebar.selectbox("Commodity", filtered_data['Commodity'].unique())
    
    # Filter varieties based on the selected commodity
    variety = st.sidebar.selectbox("Variety", filtered_data['Variety'].unique())
    
    # Filter grades based on the selected variety
    grade = st.sidebar.selectbox("Grade", filtered_data['Grade'].unique())

    # Encode inputs
    input_data = {
        "State": encoders["State"].transform([state])[0],
        "District": encoders["District"].transform([district])[0],
        "Market": encoders["Market"].transform([market])[0],
        "Commodity": encoders["Commodity"].transform([commodity])[0],
        "Variety": encoders["Variety"].transform([variety])[0],
        "Grade": encoders["Grade"].transform([grade])[0]
    }
    return input_data

# Predict price based on user input
def make_prediction(input_data):
    input_df = pd.DataFrame([input_data])
    prediction = model.predict(input_df)
    return prediction[0]

# Main app interface
def main():
    input_data = add_sidebar()
    
    # Main Title
    st.title("🌾 Bhoomi: Crop Price Forecast")
    st.markdown(
        "Welcome to **Bhoomi**! Use this tool to get forecasted crop prices based on market and crop features."
        " Start by entering your inputs on the left sidebar."
    )

    st.markdown("---")

    # Display prediction button and result area in columns for better UI
    col1, col2 = st.columns([2, 3])
    with col1:
        st.subheader("Predict Price")
        if st.button("Get Forecast"):
            prediction = make_prediction(input_data)
            with col2:
                st.success("Forecast Result")
                st.write(f"The forecasted price for your crop selection is: **₹{prediction:,.2f}**")
    st.markdown("---")
    st.info("Tip: Adjust the inputs in the sidebar to view predictions for different crop conditions!")

if __name__ == "__main__":
    main()
