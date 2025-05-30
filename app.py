import streamlit as st
import pandas as pd
from backend import load_patient_data, predict_cancer_type

st.set_page_config(page_title="Patient Gene Expression Analyzer", layout="wide")
st.title("🧬 Patient Gene Expression Analyzer")

st.write("""
Upload your gene expression data and metadata below. 
The app will determine each patient’s condition based on the metadata, 
and if the patient is diseased, it will attempt to identify the likely type of cancer using gene expression markers.
""")

# Upload section
expression_file = st.file_uploader("📄 Upload Gene Expression File (.xlsx)", type=["xlsx"])
metadata_file = st.file_uploader("📄 Upload Patient Metadata File (.xlsx)", type=["xlsx"])

if expression_file and metadata_file:
    expr_df, meta_df = load_patient_data(expression_file, metadata_file)

    st.subheader("📊 Uploaded Gene Expression Data")
    st.dataframe(expr_df)

    st.subheader("📋 Uploaded Patient Metadata")
    st.dataframe(meta_df)

    st.subheader("🧠 Health Assessment with Predicted Cancer Type")

    # Add a column for cancer type if patient is diseased
    condition_list = []
    predicted_types = []

    for _, row in meta_df.iterrows():
        patient_id = row["PatientID"]
        condition = row["Condition"].strip().capitalize()

        if condition == "Cancer":
            predicted_type = predict_cancer_type(expr_df, patient_id)
            condition_list.append("Diseased")
            predicted_types.append(predicted_type)
        else:
            condition_list.append("Healthy")
            predicted_types.append("N/A")

    # Build the display table
    results_df = meta_df.copy()
    results_df["Assessment"] = condition_list
    results_df["Predicted Cancer Type"] = predicted_types

    st.dataframe(results_df)

    # Individual patient diagnosis
    st.subheader("🔍 Individual Patient Report")
    selected_patient = st.selectbox("Select a Patient ID", meta_df["PatientID"])

    if selected_patient:
        patient_info = results_df[results_df["PatientID"] == selected_patient].iloc[0]
        st.markdown(f"### 🧾 Diagnosis for `{selected_patient}`")
        st.write(f"- Health Status: **{patient_info['Assessment']}**")
        if patient_info["Assessment"] == "Diseased":
            st.write(f"- Predicted Cancer Type: **{patient_info['Predicted Cancer Type']}**")
        else:
            st.write("- Patient is healthy. No signs of cancer detected.")
