from __future__ import annotations

import numpy as np
import pandas as pd
import streamlit as st
from sklearn.decomposition import PCA, TruncatedSVD
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns


def run_dimensionality_reduction(df: pd.DataFrame) -> None:
	st.subheader("Dimensionality Reduction (PCA / SVD)")

	num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
	if len(num_cols) < 2:
		st.error("Need at least 2 numeric columns.")
		return

	features = st.multiselect("Select feature columns", num_cols, default=num_cols[: min(6, len(num_cols))], key="dim_features")
	if len(features) < 2:
		st.warning("Select at least 2 features.")
		return

	algo = st.radio("Algorithm", ("PCA", "TruncatedSVD"), index=0, key="dim_algo")
	n_components = st.slider("n_components", 2, min(10, len(features)), value=2, step=1, key="dim_n_components")

	X = df[features].to_numpy()
	X_scaled = StandardScaler().fit_transform(X)

	if algo == "PCA":
		model = PCA(n_components=n_components, random_state=42)
		Z = model.fit_transform(X_scaled)
		explained = model.explained_variance_ratio_
	else:
		model = TruncatedSVD(n_components=n_components, random_state=42)
		Z = model.fit_transform(X)
		explained = model.explained_variance_ratio_

	st.write({"explained_variance_ratio_sum": float(np.sum(explained[:n_components]))})

	# 2D scatter if possible
	if n_components >= 2:
		fig, ax = plt.subplots(figsize=(6, 5))
		sns.scatterplot(x=Z[:, 0], y=Z[:, 1], ax=ax)
		ax.set_xlabel("Component 1")
		ax.set_ylabel("Component 2")
		ax.set_title(f"{algo} 2D projection")
		st.pyplot(fig, clear_figure=True)

	with st.expander("Explained variance per component"):
		fig, ax = plt.subplots(figsize=(6, 3))
		ox = np.arange(1, len(explained) + 1)
		ax.bar(ox, explained)
		ax.set_xlabel("Component")
		ax.set_ylabel("Explained variance ratio")
		st.pyplot(fig, clear_figure=True)
