import pandas as pd

# Define marker genes for illustrative cancer types
CANCER_MARKERS = {
    "Breast Cancer": ["BRCA1", "BRCA2"],
    "Lung Cancer": ["EGFR", "ALK"],
    "Prostate Cancer": ["TP53", "PTEN"],
    "Colorectal Cancer": ["KRAS", "APC"]
}

def load_patient_data(expression_file, metadata_file):
    expr_df = pd.read_excel(expression_file, index_col=0)
    meta_df = pd.read_excel(metadata_file)
    return expr_df, meta_df

def assess_patient_health(expr_df, meta_df):
    assessment = []

    for patient in meta_df["PatientID"]:
        patient_profile = expr_df[patient]
        # Simple rule: high MYC or EGFR expression might indicate cancer
        if patient_profile.get("MYC", 0) > 5 or patient_profile.get("EGFR", 0) > 5:
            health = "Cancer"
        else:
            health = "Healthy"
        assessment.append({"PatientID": patient, "Assessment": health})

    return pd.DataFrame(assessment)

def predict_cancer_type(expr_df, patient_id):
    patient_data = expr_df[patient_id]
    max_score = 0
    predicted_type = "Unknown"

    for cancer_type, markers in CANCER_MARKERS.items():
        score = patient_data.get(markers, pd.Series(0)).sum()
        if score > max_score:
            max_score = score
            predicted_type = cancer_type

    return predicted_type
