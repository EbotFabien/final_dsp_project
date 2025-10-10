import streamlit as st
import requests
import pandas as pd

st.set_page_config(
    page_title="ML Prediction WebApp",
    page_icon="🔮",
    layout="wide",
)

API_URL = "http://127.0.0.1:8000/predict_single/"
PAST_URL = "http://127.0.0.1:8000/past-predictions"
st.sidebar.title("Navigation")
st.sidebar.markdown("Use the sidebar to navigate between pages.")
st.title("🧠 Machine Learning Prediction Dashboard")

st.markdown("""
Welcome!  
This web app allows you to:
- Make single or batch predictions using a trained model.
- View historical predictions stored in the database.
""")

page = st.sidebar.selectbox("Navigate", ["🔮 Prediction", "📊 Past Predictions"])

if page == "🔮 Prediction":
    st.header("🏠 Make a House Price Prediction")

    col1, col2 = st.columns(2)

    with col1:
        squareMeters = st.number_input("Square Meters", min_value=1.0)
        numberOfRooms = st.number_input("Number of Rooms", min_value=1)
        hasYard = st.selectbox("Has Yard?", [0, 1])
        hasPool = st.selectbox("Has Pool?", [0, 1])
        floors = st.number_input("Floors", min_value=1)
        cityCode = st.number_input("City Code", min_value=1)
        cityPartRange = st.number_input("City Part Range", min_value=1)
        numPrevOwners = st.number_input("Number of Previous Owners", min_value=0)

    with col2:
        made = st.number_input("Year Built", min_value=1800, max_value=2025)
        isNewBuilt = st.selectbox("Is Newly Built?", [0, 1])
        hasStormProtector = st.selectbox("Has Storm Protector?", [0, 1])
        basement = st.number_input("Basement Size (m²)", min_value=0.0)
        attic = st.number_input("Attic Size (m²)", min_value=0.0)
        garage = st.number_input("Garage Size (m²)", min_value=0.0)
        hasStorageRoom = st.selectbox("Has Storage Room?", [0, 1])
        hasGuestRoom = st.number_input("Guest Rooms", min_value=0)

    if st.button("🚀 Predict Single House"):
        # Here you will send the data to your FastAPI backend
        payload = {
            "squareMeters": squareMeters,
            "numberOfRooms": numberOfRooms,
            "hasYard": hasYard,
            "hasPool": hasPool,
            "floors": floors,
            "cityCode": cityCode,
            "cityPartRange": cityPartRange,
            "numPrevOwners": numPrevOwners,
            "made": made,
            "isNewBuilt": isNewBuilt,
            "hasStormProtector": hasStormProtector,
            "basement": basement,
            "attic": attic,
            "garage": garage,
            "hasStorageRoom": hasStorageRoom,
            "hasGuestRoom": hasGuestRoom
        }

        response = requests.post(API_URL, json=payload)
        print(response.status_code)
        if response.status_code == 200:
            
            prediction = response.json()
            st.success(f"Predicted price: {prediction['price']}")
            st.dataframe(pd.DataFrame([payload]))
        else:
            st.error("Error making prediction")
        st.success("Prediction will appear here after connecting the backend!")

    #st.divider()
    #st.subheader("📂 Upload CSV for Multiple Predictions")
    #uploaded_file = st.file_uploader("Upload CSV", type=["csv"])
    #if uploaded_file is not None:
        #st.info("CSV prediction will appear here after connecting the backend!")'''

elif page == "📊 Past Predictions":
    st.header("📊 Past Predictions")
    #st.info("You can later connect this page to your backend to view past predictions.")
    start_date = st.date_input("Start Date")
    end_date = st.date_input("End Date")
    source = st.selectbox("Source", ["webapp", "scheduled", "all"])

    if st.button("Fetch Past Predictions"):
        params = {"start_date": str(start_date), "end_date": str(end_date), "source": source}
        response = requests.get(PAST_URL, params=params)
        if response.status_code == 200:
            st.dataframe(pd.DataFrame(response.json()))
        else:
            st.error("Error fetching past predictions")
    

