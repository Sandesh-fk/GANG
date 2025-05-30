import streamlit as st
import pandas as pd
from backend import load_patient_data, assess_patient_health, predict_cancer_type

st.set_page_config(page_title="Patient Gene Expression Analyzer", layout="wide")
st.title("🧬 Patient Gene Expression Analyzer")

st.write(
    "Upload your gene expression data and metadata below. "
    "The app will analyze each patient and determine if they are healthy or show signs of cancer. "
    "If cancer is detected, the app will also try to identify the most likely type based on marker genes."
)

# Upload section
expression_file = st.file_uploader("📄 Upload Gene Expression File (.xlsx)", type=["xlsx"])
metadata_file = st.file_uploader("📄 Upload Patient Metadata File (.xlsx)", type=["xlsx"])

if expression_file and metadata_file:
    expr_df, meta_df = load_patient_data(expression_file, metadata_file)

    st.subheader("📊 Uploaded Gene Expression Data")
    st.dataframe(expr_df)

    st.subheader("📋 Uploaded Patient Metadata")
    st.dataframe(meta_df)

    st.subheader("🧠 Health Assessment Results")
    health_df = assess_patient_health(expr_df, meta_df)
    st.dataframe(health_df)

    st.subheader("🔍 Cancer Type Prediction")
    selected_patient = st.selectbox("Select a Patient ID", meta_df["PatientID"])

    if selected_patient:
        health_status = health_df.loc[health_df["PatientID"] == selected_patient, "Assessment"].values[0]

        st.markdown(f"### 🧾 Diagnosis for `{selected_patient}`")
        st.write(f"- Health Status: **{health_status}**")

        if health_status == "Cancer":
            cancer_type = predict_cancer_type(expr_df, selected_patient)
            st.write(f"- Predicted Cancer Type: **{cancer_type}**")
        else:
            st.write("- Patient is healthy. No signs of cancer detected.")
