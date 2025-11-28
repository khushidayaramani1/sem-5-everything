from __future__ import annotations

import numpy as np
import pandas as pd
import streamlit as st
from typing import List
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

from .data import split_supervised


def run_tree_classification(df: pd.DataFrame) -> None:
	st.subheader("Decision Tree Classification (ID3 - Entropy)")

	if "target" not in df.columns:
		st.info("No 'target' column found. Please ensure your dataset has a target column for classification.")

	target_col = st.selectbox("Select target column", df.columns.tolist(), index=df.columns.tolist().index("target") if "target" in df.columns else 0, key="tree_target")

	test_size = st.slider("Test size", 0.1, 0.5, value=0.2, step=0.05, key="tree_test_size")
	random_state = st.number_input("Random state", min_value=0, value=42, step=1, key="tree_random_state")

	split = split_supervised(df, target_col, test_size=test_size, random_state=random_state)

	# ID3-style: entropy criterion, full depth
	clf = DecisionTreeClassifier(criterion="entropy", random_state=random_state)
	clf.fit(split.X_train, split.y_train)
	y_pred = clf.predict(split.X_test)

	acc = accuracy_score(split.y_test, y_pred)
	prec, rec, f1, _ = precision_recall_fscore_support(split.y_test, y_pred, average="weighted", zero_division=0)
	c1, c2, c3 = st.columns(3)
	with c1:
		st.metric("Accuracy", f"{acc:.4f}")
	with c2:
		st.metric("Precision(w)", f"{prec:.4f}")
	with c3:
		st.metric("F1(w)", f"{f1:.4f}")

	cm = confusion_matrix(split.y_test, y_pred)
	fig, ax = plt.subplots(figsize=(5,4))
	sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", ax=ax)
	ax.set_title("Confusion Matrix")
	st.pyplot(fig, clear_figure=True)

	# Full tree visualization (can be large)
	with st.expander("Show full decision tree (may be large)", expanded=True):
		nodes = clf.tree_.node_count
		if nodes > 300:
			st.warning(f"The tree has {nodes} nodes and may be hard to read.")
		fig, ax = plt.subplots(figsize=(min(20, 4 + nodes * 0.02), 12))
		plot_tree(
			clf,
			feature_names=split.feature_names,
			filled=True,
			class_names=True,
			proportion=True,
			fontsize=8,
		)
		st.pyplot(fig, clear_figure=True)
