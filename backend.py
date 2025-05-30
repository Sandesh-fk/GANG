import pandas as pd

# Marker genes for basic cancer prediction
CANCER_MARKERS = {
    "Breast Cancer": ["BRCA1", "BRCA2"],
    "Lung Cancer": ["EGFR", "ALK"],
    "Prostate Cancer": ["TP53", "PTEN"],
    "Colorectal Cancer": ["KRAS", "APC"]
}

# Load Excel files
def load_patient_data(expression_file, metadata_file):
    expr_df = pd.read_excel(expression_file, index_col=0)
    meta_df = pd.read_excel(metadata_file)
    return expr_df, meta_df

# Predict the cancer type using expression values
def predict_cancer_type(expr_df, patient_id):
    if patient_id not in expr_df.columns:
        return "Unknown"
    
    patient_expr = expr_df[patient_id]
    scores = {}
    
    for cancer_type, markers in CANCER_MARKERS.items():
        # Sum the expression values for each set of markers
        score = sum([patient_expr.get(gene, 0) for gene in markers])
        scores[cancer_type] = score

    # Return the cancer type with the highest score
    return max(scores, key=scores.get)
