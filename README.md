Bhoomi: A Smart Agricultural Assistant
Bhoomi is an AI-powered platform designed to empower farmers with real-time, data-driven insights to improve crop yield, reduce resource waste, and promote sustainable farming practices. With features like crop and fertilizer recommendations, irrigation management, price forecasting, soil fertility assessment, and government scheme information, Bhoomi offers an all-in-one solution tailored to the unique needs of the agricultural sector.

Features
Crop Recommendation: Suggests the best crops based on soil composition, weather patterns, and historical data, using a Random Forest model with 99.09% accuracy.
Fertilizer Recommendation: Provides precise fertilizer recommendations (type and dosage) based on soil nutrients and crop requirements, powered by an XGBoost model.
Irrigation Management: Dynamically adjusts irrigation schedules based on real-time weather and soil moisture data, optimizing water use.
Price Forecasting: Predicts future crop prices using an XGBoost model, helping farmers make informed selling decisions.
Soil Fertility Assessment: Analyzes soil health, classifying fertility levels to guide soil management practices, utilizing a Random Forest model.
Government Schemes: Provides information on relevant government schemes and subsidies to help farmers access financial support.
Smart Farming Hub: Offers a knowledge base with FAQs on modern farming techniques and sustainable practices.
Chatbot Assistance: Google Gemini AI-powered chatbot provides real-time answers to farming-related questions.

Methodology
User Access & Interface Navigation: Farmers access Bhoomi through an intuitive Streamlit interface, available on both desktop and mobile.
Feature Selection: Users select from various features, triggering the backend processes for each.
Data Collection & Integration: Aggregates data from weather APIs, market data, soil metrics, and government databases for accurate insights.
Model Execution: Machine learning models (Random Forest, XGBoost) are used to provide recommendations and predictions.
Real-Time Chatbot Assistance: Google Gemini chatbot offers immediate support and guidance for users.
Feedback & Continuous Improvement: Feedback loops and regular updates ensure Bhoomi’s accuracy and relevance.

Technology Stack
Backend: Python, Streamlit
Machine Learning Models: Random Forest, XGBoost

Data Sources: OpenWeather API, Agricultural Market Databases, Government Databases
Cloud Platform: Deployed using cloud-based infrastructure for scalability
Chatbot: Google Gemini AI for real-time, interactive support

Installation
To run Bhoomi locally, follow these steps:

Future Enhancements
Advanced Yield Prediction: Integrate advanced models for precise yield forecasting.
Pest & Disease Detection: Implement AI-driven tools for early detection.
Scalability: Expand cloud infrastructure and mobile functionality to support a larger user base.
Multi-Language Support: Increase accessibility with additional language options.

Contributing
We welcome contributions to Bhoomi. Please fork the repository and submit a pull request with any improvements or bug fixes.

License
This project is licensed under the MIT License - see the LICENSE file for details.
