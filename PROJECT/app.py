import streamlit as st
import pandas as pd
from typing import Optional

from ml.data import (
	ensure_numeric_dataframe,
)
from ml.visualization import run_visualizations
from ml.regression_linear import run_linear_regression
from ml.classification_tree import run_tree_classification
from ml.classification_svm import run_svm_classification
from ml.ensemble import run_ensemble_classification
from ml.regression_nonlinear import run_nonlinear_regression
from ml.clustering import run_clustering
from ml.dimreduction import run_dimensionality_reduction


st.set_page_config(page_title="ML Playground", layout="wide")

# Minimal style touch
st.markdown(
	"""
	<style>
		.block-container {padding-top: 2rem;}
		.sidebar .sidebar-content {padding-top: 1rem;}
	</style>
	""",
	unsafe_allow_html=True,
)


def load_data_ui() -> Optional[pd.DataFrame]:
	st.sidebar.header("Upload Dataset")
	uploaded = st.sidebar.file_uploader("Upload a CSV file", type=["csv"]) 
	if uploaded is not None:
		try:
			df = pd.read_csv(uploaded)
			return df
		except Exception as exc:
			st.sidebar.error(f"Failed to read CSV: {exc}")
			return None
	return None


def main():
	st.title("Interactive ML Playground ✨")
	st.caption("Upload a CSV on the left, then use the tabs below to explore.")

	df = load_data_ui()

	if df is None:
		st.info("Please upload a CSV to begin.")
		return

	with st.expander("Dataset Preview", expanded=False):
		st.dataframe(df.head(), use_container_width=True)

	# Tabs for tasks
	tab_vis, tab_lin, tab_tree, tab_svm, tab_ens, tab_nl, tab_cluster, tab_dim = st.tabs([
		"Visualization",
		"Linear Regression",
		"Decision Tree (ID3)",
		"SVM Classification",
		"Ensembles",
		"Nonlinear Regression",
		"Clustering",
		"Dimensionality Reduction",
	])

	with tab_vis:
		run_visualizations(df)

	with tab_lin:
		numeric_df = ensure_numeric_dataframe(df)
		run_linear_regression(numeric_df)

	with tab_tree:
		run_tree_classification(df)

	with tab_svm:
		run_svm_classification(df)

	with tab_ens:
		run_ensemble_classification(df)

	with tab_nl:
		numeric_df = ensure_numeric_dataframe(df)
		run_nonlinear_regression(numeric_df)

	with tab_cluster:
		numeric_df = ensure_numeric_dataframe(df)
		run_clustering(numeric_df)

	with tab_dim:
		numeric_df = ensure_numeric_dataframe(df)
		run_dimensionality_reduction(numeric_df)


if __name__ == "__main__":
	main()
