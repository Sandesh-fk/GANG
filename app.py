import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from sklearn.decomposition import PCA
from scipy.stats import ttest_ind
from backend import load_patient_data, predict_cancer_type

# Set page configuration
st.set_page_config(page_title="Patient Gene Expression Analyzer", layout="wide")

# Custom CSS for blue theme
st.markdown("""
    <style>
        body {
            background-color: #f0f8ff;
        }
        .main {
            background-color: #ffffff;
        }
        h1, h2, h3 {
            color: #0b5394;
        }
        .stButton>button {
            color: white;
            background-color: #0b5394;
            border: none;
        }
        .stCheckbox>label>div {
            color: #0b5394;
        }
        .stSelectbox>div>div>div {
            color: #0b5394;
        }
    </style>
""", unsafe_allow_html=True)

# Title and intro
st.title("🧬 Patient Gene Expression Analyzer")
st.write("""
Upload your gene expression data and metadata below.  
The app will determine each patient’s condition based on metadata.  
If the patient is diseased, it will predict the cancer type.  
You can also explore the data visually with Heatmap, Volcano Plot, and PCA.
""")

# Upload files
expression_file = st.file_uploader("📄 Upload Gene Expression File (.xlsx)", type=["xlsx"])
metadata_file = st.file_uploader("📄 Upload Patient Metadata File (.xlsx)", type=["xlsx"])

if expression_file and metadata_file:
    expr_df, meta_df = load_patient_data(expression_file, metadata_file)

    st.subheader("📊 Uploaded Gene Expression Data")
    st.dataframe(expr_df)

    st.subheader("📋 Uploaded Patient Metadata")
    st.dataframe(meta_df)

    st.subheader("🧠 Health Assessment with Predicted Cancer Type")

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

    results_df = meta_df.copy()
    results_df["Assessment"] = condition_list
    results_df["Predicted Cancer Type"] = predicted_types

    st.dataframe(results_df)

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

    # --- Visualizations ---
    st.header("📊 Visualize Gene Expression Differences")

    if st.checkbox("🔬 Show Heatmap"):
        st.subheader("🌡️ Gene Expression Heatmap")
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.heatmap(expr_df, cmap="Blues", ax=ax)
        st.pyplot(fig)

    if st.checkbox("🌋 Show Volcano Plot"):
        st.subheader("🌋 Volcano Plot")

        healthy_ids = meta_df[meta_df["Condition"].str.lower() == "healthy"]["PatientID"]
        cancer_ids = meta_df[meta_df["Condition"].str.lower() == "cancer"]["PatientID"]

        log2_fc = []
        p_values = []

        for gene in expr_df.index:
            group1 = expr_df.loc[gene, healthy_ids]
            group2 = expr_df.loc[gene, cancer_ids]
            fc = np.log2((group2.mean() + 1e-6) / (group1.mean() + 1e-6))
            p = ttest_ind(group2, group1, equal_var=False).pvalue
            log2_fc.append(fc)
            p_values.append(p)

        volcano_df = pd.DataFrame({
            "Gene": expr_df.index,
            "log2FC": log2_fc,
            "-log10(p-value)": -np.log10(p_values)
        })

        fig, ax = plt.subplots()
        sns.scatterplot(data=volcano_df, x="log2FC", y="-log10(p-value)", ax=ax, hue=volcano_df["-log10(p-value)"] > 1.3, palette="coolwarm")
        ax.axhline(y=1.3, color='red', linestyle='--')
        ax.axvline(x=1, color='blue', linestyle='--')
        ax.axvline(x=-1, color='blue', linestyle='--')
        st.pyplot(fig)

    if st.checkbox("📈 Show PCA Plot"):
        st.subheader("📈 PCA Plot of Samples")

        X = expr_df.T
        y = meta_df.set_index("PatientID").loc[X.index]["Condition"]

        pca = PCA(n_components=2)
        X_pca = pca.fit_transform(X)

        pca_df = pd.DataFrame(X_pca, columns=["PC1", "PC2"])
        pca_df["Condition"] = y.values

        fig, ax = plt.subplots()
        sns.scatterplot(data=pca_df, x="PC1", y="PC2", hue="Condition", s=100, palette="Blues")
        st.pyplot(fig)
