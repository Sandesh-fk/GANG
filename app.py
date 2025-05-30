import streamlit as st
import pandas as pd
import plotly.express as px
from backend import load_data, preprocess_data, differential_expression

def main():
    st.title("Gene Expression Explorer")

    expression_file = st.file_uploader("Upload Gene Expression Data", type=["xlsx"])
    metadata_file = st.file_uploader("Upload Sample Metadata", type=["xlsx"])

    if expression_file and metadata_file:
        expression_data, metadata = load_data(expression_file, metadata_file)
        expression_data = preprocess_data(expression_data)

        st.write("Gene Expression Data", expression_data.head())
        st.write("Sample Metadata", metadata.head())

        results = differential_expression(expression_data, metadata)
        st.write("Differential Expression Results", results.head())

        fig = px.histogram(results, x='adjusted_p_value', nbins=50, title="Distribution of Adjusted p-values")
        st.plotly_chart(fig)

        gene = st.text_input("Enter Gene ID to View Expression Levels")
        if gene:
            if gene in expression_data.index:
                gene_expression = expression_data.loc[gene]
                st.write(f"Expression Levels for {gene}", gene_expression)
            else:
                st.write("Gene not found in the dataset.")

if __name__ == "__main__":
    main()
