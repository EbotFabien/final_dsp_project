import streamlit as st
import pandas as pd
from utils.api_client import make_predictions

st.title("🔮 Prediction Page")

st.markdown("### Make a Single Prediction")
col1, col2 = st.columns(2)

# Example feature inputs (you can customize based on your model)
feature1 = col1.number_input("Feature 1", value=0.0)
feature2 = col2.number_input("Feature 2", value=0.0)

single_data = pd.DataFrame([{"feature1": feature1, "feature2": feature2}])

if st.button("Predict Single Sample"):
    try:
        preds = make_predictions(single_data)
        st.success("Prediction complete!")
        result_df = single_data.copy()
        result_df["prediction"] = preds
        st.dataframe(result_df, use_container_width=True)
    except Exception as e:
        st.error(f"Error: {e}")

st.divider()
st.markdown("### Upload a CSV for Multi Prediction")

uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    st.write("Data Preview:", data.head())

    if st.button("Predict from CSV"):
        try:
            preds = make_predictions(data)
            st.success("Batch predictions complete!")
            result_df = data.copy()
            result_df["prediction"] = preds
            st.dataframe(result_df, use_container_width=True)
        except Exception as e:
            st.error(f"Error: {e}")
