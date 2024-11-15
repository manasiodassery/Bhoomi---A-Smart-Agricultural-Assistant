import streamlit as st
import json

# Load FAQ data from JSON file with error handling
def load_faq_data():
    try:
        with open(r'C:/Manasi/NMIMS/Manasi/Capstone Project/Agriculture/Bhoomi/JSON files/smartfarming.json', 'r') as file:
            faqs = json.load(file)
        return faqs
    except FileNotFoundError:
        st.error("The FAQ file was not found. Please check the path and try again.")
        return {}
    except json.JSONDecodeError:
        st.error("Error decoding the FAQ file. Ensure the file is in proper JSON format.")
        return {}

# Streamlit app interface configuration
st.set_page_config(page_title="Smart Farming FAQs", page_icon="🚜", layout="wide")

# Main title and description
st.title("🌾 Bhoomi: Smart Farming FAQs")
st.markdown("""
    Welcome to the **Smart Farming FAQ** section! Here you can find answers to common questions about smart farming 
    technologies and practices. Use the dropdown menu to select a question and view the answer below.
""")

# Load FAQ data
faqs = load_faq_data()

# Sidebar for additional support
st.sidebar.title("Need Help?")
st.sidebar.markdown("For more assistance, feel free to reach out at [xyz@gmail.com](mailto:xyz@gmail.com)")

# Display FAQ navigation and answer section
if faqs:
    question_list = [faq["Question"] for faq in faqs.get("Smart Farming FAQ", {}).values()]
    
    # FAQ selection with interactive question-answer display
    selected_question = st.selectbox("Select a question:", question_list)
    
    # Show the selected question's answer with improved styling
    st.subheader(f"📌 {selected_question}")
    selected_answer = next((faq["Answer"] for faq in faqs["Smart Farming FAQ"].values() if faq["Question"] == selected_question), "No answer found.")
    st.write(selected_answer)
else:
    st.warning("FAQs are currently unavailable. Please try again later.")

