import pandas as pd
import numpy as np
from scipy.stats import ttest_ind

def load_data(expression_file, metadata_file):
    expression_data = pd.read_excel(expression_file, index_col=0)
    metadata = pd.read_excel(metadata_file)
    return expression_data, metadata

def preprocess_data(expression_data):
    expression_data = expression_data.replace(0, np.nan)
    return expression_data

def differential_expression(expression_data, metadata):
    groups = metadata['Condition'].unique()
    group1 = metadata[metadata['Condition'] == groups[0]]
    group2 = metadata[metadata['Condition'] == groups[1]]

    group1_data = expression_data[group1['SampleID']]
    group2_data = expression_data[group2['SampleID']]

    p_values = []
    for gene in expression_data.index:
        _, p_value = ttest_ind(group1_data.loc[gene], group2_data.loc[gene])
        p_values.append(p_value)

    results = pd.DataFrame({
        'Gene': expression_data.index,
        'p_value': p_values
    })
    results['adjusted_p_value'] = results['p_value'] * len(results)  # Simple Bonferroni correction
    return results

def save_results(results, output_file):
    results.to_csv(output_file, index=False)
