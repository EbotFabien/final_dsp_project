import streamlit as st
import pandas as pd
from utils.api_client import get_past_predictions

st.title("📊 Past Predictions")

col1, col2, col3 = st.columns(3)

source = col1.selectbox(
    "Prediction Source",
    options=["all", "webapp", "scheduled predictions"],
    index=0,
)

start_date = col2.date_input("Start Date")
end_date = col3.date_input("End Date")

if st.button("Fetch Predictions"):
    try:
        results = get_past_predictions(
            source=source,
            start_date=str(start_date),
            end_date=str(end_date)
        )
        if results:
            df = pd.DataFrame(results)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No predictions found for this period.")
    except Exception as e:
        st.error(f"Error fetching predictions: {e}")
