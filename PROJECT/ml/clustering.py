from __future__ import annotations

import numpy as np
import pandas as pd
import streamlit as st
from sklearn.cluster import KMeans, DBSCAN
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns


def run_clustering(df: pd.DataFrame) -> None:
	st.subheader("Clustering (KMeans / DBSCAN)")

	num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
	if len(num_cols) < 2:
		st.error("Need at least 2 numeric columns.")
		return

	features = st.multiselect("Select feature columns", num_cols, default=num_cols[: min(5, len(num_cols))], key="cluster_features")
	if len(features) < 2:
		st.warning("Select at least 2 features for visualization.")
		return

	algo = st.radio("Algorithm", ("KMeans", "DBSCAN"), index=0, key="cluster_algo")
	X = df[features].to_numpy()
	X_scaled = StandardScaler().fit_transform(X)

	if algo == "KMeans":
		k = st.slider("n_clusters (k)", 2, 10, value=3, step=1, key="kmeans_k")
		model = KMeans(n_clusters=k, n_init=10, random_state=42)
		labels = model.fit_predict(X_scaled)
	else:
		eps = st.slider("eps", 0.1, 5.0, value=0.8, step=0.1, key="dbscan_eps")
		min_samples = st.slider("min_samples", 3, 20, value=5, step=1, key="dbscan_min_samples")
		model = DBSCAN(eps=eps, min_samples=min_samples)
		labels = model.fit_predict(X_scaled)

	st.write({"num_clusters": len(set(labels)) - (1 if -1 in labels else 0), "num_noise": int(np.sum(labels == -1))})

	# 2D plot using first two features selected
	fig, ax = plt.subplots(figsize=(6, 5))
	sns.scatterplot(x=X[:, 0], y=X[:, 1], hue=labels, palette="tab10", ax=ax)
	ax.set_xlabel(features[0])
	ax.set_ylabel(features[1])
	ax.set_title("Clusters (by first two selected features)")
	st.pyplot(fig, clear_figure=True)
