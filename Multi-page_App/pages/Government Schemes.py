import streamlit as st
import json

# Load schemes data from JSON file with error handling
def load_schemes_data():
    try:
        with open(r'C:\Manasi\NMIMS\Manasi\Capstone Project\Agriculture\Bhoomi\JSON files\schemes.json', 'r') as file:
            schemes = json.load(file)
        return schemes
    except FileNotFoundError:
        st.error("The schemes file was not found. Please check the path and try again.")
        return {}
    except json.JSONDecodeError:
        st.error("Error decoding the schemes file. Ensure the file is in proper JSON format.")
        return {}

# Streamlit app interface configuration
st.set_page_config(
    page_title="Bhoomi: Government Schemes and Subsidies",
    page_icon="🌾",
    layout="wide"
)
st.title("Bhoomi: Government Schemes and Subsidies")
st.markdown("""
Explore various government schemes and subsidies available to support farmers.
Use the search feature in the sidebar to find specific schemes or keywords.
""")

# Load schemes data
schemes = load_schemes_data()

# Sidebar search input
st.sidebar.header("🔍 Search Schemes")
search_query = st.sidebar.text_input("Enter scheme name or keyword", "")

# Filter schemes based on search query
filtered_schemes = {
    name: details for name, details in schemes.items() 
    if search_query.lower() in name.lower() or any(search_query.lower() in str(detail).lower() for detail in details.values())
}

# Display filtered schemes
st.subheader("Available Schemes")
if filtered_schemes:
    for scheme_name, details in filtered_schemes.items():
        with st.expander(f"🌱 {scheme_name}", expanded=False):
            # Dynamically display all available details from JSON
            for key, value in details.items():
                if isinstance(value, dict):  # Handle nested dictionaries
                    st.markdown(f"**{key}:**")
                    for sub_key, sub_value in value.items():
                        st.markdown(f"- **{sub_key}:** {sub_value}")
                elif isinstance(value, list):  # Handle lists
                    st.markdown(f"**{key}:**")
                    for item in value:
                        if isinstance(item, dict):
                            for item_key, item_value in item.items():
                                st.markdown(f"- **{item_key}:** {item_value}")
                        else:
                            st.markdown(f"- {item}")
                else:
                    st.markdown(f"**{key}:** {value}")
            # Add link to more information if available
            if 'More Information' in details:
                st.markdown(f"[More Information]({details['More Information']})", unsafe_allow_html=True)
else:
    st.info("No schemes found. Please enter a different search term.")

# Add a footer with relevant information
st.markdown("---")
st.markdown("**Note:** The information displayed is based on the latest available data. For further assistance, contact your local agricultural office.")
