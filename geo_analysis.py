import pandas as pd
import numpy as np
from scipy.stats import ttest_ind

def get_de_genes_from_csv(csv_path, group_labels, group1, group2, top_n=20):
    df = pd.read_csv(csv_path, index_col=0)
    expression_data = df.iloc[:, :-1]
    groups = group_labels

    # Get indices for each group
    grp1_idx = [i for i, g in enumerate(groups) if g == group1]
    grp2_idx = [i for i, g in enumerate(groups) if g == group2]

    results = []
    for gene in expression_data.index:
        vals1 = expression_data.iloc[gene, grp1_idx]
        vals2 = expression_data.iloc[gene, grp2_idx]
        stat, p = ttest_ind(vals1, vals2, nan_policy='omit')
        results.append((gene, p, np.mean(vals1), np.mean(vals2)))

    res_df = pd.DataFrame(results, columns=['gene','p_value','mean_' + group1,'mean_' + group2])
    res_df = res_df.sort_values('p_value').head(top_n)
    return res_df.to_dict(orient='records')
