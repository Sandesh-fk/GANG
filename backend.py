import pandas as pd

# Load uploaded Excel files
def load_patient_data(expression_file, metadata_file):
    expr_df = pd.read_excel(expression_file, index_col=0)
    meta_df = pd.read_excel(metadata_file)
    return expr_df, meta_df

# Predict cancer type based on expression levels
def predict_cancer_type(expr_df, patient_id):
    # Get patient-specific gene expression
    patient_data = expr_df[patient_id]

    # Simple rule-based classification (you can replace this with a trained model)
    if patient_data["BRCA1"] > 3.0 and patient_data["BRCA2"] > 3.0:
        return "Breast Cancer"
    elif patient_data["EGFR"] > 4.0 and patient_data["ALK"] > 4.0:
        return "Lung Cancer"
    elif patient_data["KRAS"] > 4.0 and patient_data["APC"] > 4.0:
        return "Colorectal Cancer"
    elif patient_data["TP53"] > 4.0 and patient_data["PTEN"] > 4.0:
        return "Prostate Cancer"
    else:
        return "Unknown"
