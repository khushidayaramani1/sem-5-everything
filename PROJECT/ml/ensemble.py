from __future__ import annotations

import numpy as np
import pandas as pd
import streamlit as st
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

from .data import split_supervised


def run_ensemble_classification(df: pd.DataFrame) -> None:
	st.subheader("Ensemble Learning (Bagging/Boosting)")

	target_col = st.selectbox("Select target column (Ensemble)", df.columns.tolist(), index=df.columns.tolist().index("target") if "target" in df.columns else 0, key="ensemble_target")
	test_size = st.slider("Test size", 0.1, 0.5, value=0.2, step=0.05, key="ensemble_test_size")
	random_state = st.number_input("Random state", min_value=0, value=42, step=1, key="ensemble_random_state")

	algo = st.radio("Algorithm", ("Random Forest (Bagging)", "Gradient Boosting"), index=0, key="ensemble_algo")

	if algo == "Random Forest (Bagging)":
		n_estimators = st.slider("n_estimators", 50, 500, value=200, step=50, key="rf_n_estimators")
		max_depth = st.slider("max_depth", 2, 20, value=6, step=1, key="rf_max_depth")
		model = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth, random_state=random_state)
	else:
		n_estimators = st.slider("n_estimators", 50, 500, value=200, step=50, key="gb_n_estimators")
		learning_rate = st.number_input("learning_rate", min_value=0.01, value=0.1, step=0.01, key="gb_learning_rate")
		max_depth = st.slider("max_depth", 2, 10, value=3, step=1, key="gb_max_depth")
		model = GradientBoostingClassifier(n_estimators=n_estimators, learning_rate=learning_rate, max_depth=max_depth, random_state=random_state)

	split = split_supervised(df, target_col, test_size=test_size, random_state=random_state)
	model.fit(split.X_train, split.y_train)
	y_pred = model.predict(split.X_test)

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
	sns.heatmap(cm, annot=True, fmt="d", cmap="Purples", ax=ax)
	ax.set_title("Confusion Matrix")
	st.pyplot(fig, clear_figure=True)

	# Feature importances if available
	if hasattr(model, "feature_importances_"):
		imp = pd.Series(model.feature_importances_, index=split.feature_names).sort_values(ascending=False)[:20]
		st.markdown("**Top Feature Importances**")
		st.bar_chart(imp)
