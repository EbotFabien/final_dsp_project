import streamlit as st

st.set_page_config(
    page_title="ML Prediction WebApp",
    page_icon="🔮",
    layout="wide",
)

st.sidebar.title("Navigation")
st.sidebar.markdown("Use the sidebar to navigate between pages.")
st.title("🧠 Machine Learning Prediction Dashboard")

st.markdown("""
Welcome!  
This web app allows you to:
- Make single or batch predictions using a trained model.
- View historical predictions stored in the database.
""")
