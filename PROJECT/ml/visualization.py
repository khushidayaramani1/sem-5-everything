from __future__ import annotations

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st


def run_visualizations(df: pd.DataFrame) -> None:
	st.subheader("Data Visualization")

	cols = df.columns.tolist()

	st.markdown("**Basic Info**")
	c1, c2, c3 = st.columns(3)
	with c1:
		st.write(f"Rows: {df.shape[0]}")
	with c2:
		st.write(f"Columns: {df.shape[1]}")
	with c3:
		st.write(f"Missing values: {int(df.isna().sum().sum())}")

	with st.expander("Summary statistics"):
		st.dataframe(df.describe(include="all").transpose(), use_container_width=True)

	st.markdown("**Distributions**")
	num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
	if len(num_cols) > 0:
		selected = st.multiselect("Select numeric columns", num_cols, default=num_cols[: min(3, len(num_cols))], key="vis_numeric_cols")
		if len(selected) > 0:
			fig, axs = plt.subplots(nrows=len(selected), ncols=1, figsize=(6, 3 * len(selected)))
			if len(selected) == 1:
				axs = [axs]
			for ax, col in zip(axs, selected):
				sns.histplot(df[col].dropna(), kde=True, ax=ax)
				ax.set_title(f"Distribution: {col}")
			st.pyplot(fig, clear_figure=True)
	else:
		st.info("No numeric columns to plot distributions.")

	st.markdown("**Correlation Heatmap**")
	if len(num_cols) >= 2:
		corr = df[num_cols].corr(numeric_only=True)
		fig, ax = plt.subplots(figsize=(6, 5))
		sns.heatmap(corr, cmap="coolwarm", vmin=-1, vmax=1, annot=False, ax=ax)
		ax.set_title("Correlation heatmap")
		st.pyplot(fig, clear_figure=True)

	st.markdown("**Pairplot (sampled)**")
	if len(num_cols) >= 2:
		sample_df = df.sample(min(300, len(df)), random_state=42)
		with st.spinner("Building pairplot (may take a few seconds)..."):
			g = sns.pairplot(sample_df[num_cols[: min(5, len(num_cols))]])
		st.pyplot(g.fig)
