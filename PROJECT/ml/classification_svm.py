from __future__ import annotations

import numpy as np
import pandas as pd
import streamlit as st
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix, roc_auc_score, RocCurveDisplay
import matplotlib.pyplot as plt
import seaborn as sns

from .data import split_supervised


def run_svm_classification(df: pd.DataFrame) -> None:
	st.subheader("SVM Classification")

	target_col = st.selectbox("Select target column (SVM)", df.columns.tolist(), index=df.columns.tolist().index("target") if "target" in df.columns else 0, key="svm_target")
	test_size = st.slider("Test size", 0.1, 0.5, value=0.2, step=0.05, key="svm_test_size")
	random_state = st.number_input("Random state", min_value=0, value=42, step=1, key="svm_random_state")
	kernel = st.selectbox("Kernel", ["rbf", "linear", "poly", "sigmoid"], index=0, key="svm_kernel")
	C = st.number_input("C (regularization)", min_value=0.01, value=1.0, step=0.1, key="svm_C")
	gamma = st.selectbox("Gamma", ["scale", "auto"], index=0, key="svm_gamma")

	split = split_supervised(df, target_col, test_size=test_size, random_state=random_state)

	clf = SVC(kernel=kernel, C=C, gamma=gamma, probability=True, random_state=random_state)
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
	sns.heatmap(cm, annot=True, fmt="d", cmap="Greens", ax=ax)
	ax.set_title("Confusion Matrix")
	st.pyplot(fig, clear_figure=True)

	# ROC AUC (binary only)
	try:
		if len(np.unique(split.y_test)) == 2:
			probs = clf.predict_proba(split.X_test)[:, 1]
			auc = roc_auc_score(split.y_test, probs)
			st.metric("ROC AUC", f"{auc:.4f}")
			fig, ax = plt.subplots(figsize=(5,4))
			RocCurveDisplay.from_predictions(split.y_test, probs, ax=ax)
			ax.set_title("ROC Curve")
			st.pyplot(fig, clear_figure=True)
	except Exception:
		pass
