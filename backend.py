import pandas as pd

# Marker genes for simple cancer prediction
CANCER_MARKERS = {
    "Breast Cancer": ["BRCA1", "BRCA2"],
    "Lung Cancer": ["EGFR", "ALK"],
    "Prostate Cancer": ["TP53", "PTEN"],
    "Colorectal Cancer": ["KRAS", "APC"]
}

# Load data
def load_patient_data(expression_file, metadata_file):
    expr_df = pd.read_excel(expression_file, index_col=0)
    meta_df = pd.read_excel(metadata_file)
    return expr_df, meta_df

# Determine if expression is abnormally high -> cancer
def assess_patient_health(expr_df, meta_df, threshold=4.0):
    assessments = []
    for patient in meta_df["PatientID"]:
        if patient in expr_df.columns:
            mean_expr = expr_df[patient].mean()
            status = "Cancer" if mean_expr > threshold else "Healthy"
            assessments.append({"PatientID": patient, "Assessment": status})
        else:
            assessments.append({"PatientID": patient, "Assessment": "Data Missing"})
    return pd.DataFrame(assessments)

# Predict cancer type based on sum of marker gene expression
def predict_cancer_type(expr_df, patient_id):
    if patient_id not in expr_df.columns:
        return "Unknown"
    patient_expr = expr_df[patient_id]
    scores = {}
    for cancer_type, markers in CANCER_MARKERS.items():
        score = sum([patient_expr.get(gene, 0) for gene in markers])
        scores[cancer_type] = score
    # Return cancer type with highest marker expression
    return max(scores, key=scores.get)
