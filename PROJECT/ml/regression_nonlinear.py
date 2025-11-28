from __future__ import annotations

import numpy as np
import pandas as pd
import streamlit as st
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import Ridge
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import seaborn as sns


def run_nonlinear_regression(df: pd.DataFrame) -> None:
	st.subheader("Multivariate Nonlinear Regression (Polynomial + Ridge)")

	num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
	if len(num_cols) < 2:
		st.error("Need at least 2 numeric columns (features + target).")
		return

	target = st.selectbox("Select target column (numeric)", num_cols, index=len(num_cols) - 1, key="nlr_target")
	feature_candidates = [c for c in num_cols if c != target]
	features = st.multiselect("Select feature columns", feature_candidates, default=feature_candidates, key="nlr_features")
	if len(features) == 0:
		st.warning("Select at least one feature column.")
		return

	degree = st.slider("Polynomial degree", 2, 6, value=3, step=1, key="nlr_degree")
	alpha = st.number_input("Ridge alpha", min_value=0.0, value=1.0, step=0.1, key="nlr_alpha")
	test_size = st.slider("Test size", 0.1, 0.5, value=0.2, step=0.05, key="nlr_test_size")
	random_state = st.number_input("Random state", min_value=0, value=42, step=1, key="nlr_random_state")

	X = df[features].to_numpy()
	y = df[target].to_numpy()
	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)

	model = Pipeline([
		("poly", PolynomialFeatures(degree=degree, include_bias=False)),
		("ridge", Ridge(alpha=alpha, random_state=random_state)),
	])
	model.fit(X_train, y_train)
	y_pred = model.predict(X_test)

	mae = mean_absolute_error(y_test, y_pred)
	mse = mean_squared_error(y_test, y_pred)
	rmse = np.sqrt(mse)
	r2 = r2_score(y_test, y_pred)

	c1, c2, c3, c4 = st.columns(4)
	with c1:
		st.metric("MAE", f"{mae:.4f}")
	with c2:
		st.metric("RMSE", f"{rmse:.4f}")
	with c3:
		st.metric("R^2", f"{r2:.4f}")
	with c4:
		st.metric("Features", str(len(features)))

	st.markdown("**Predicted vs Actual and Residuals**")
	fig, axs = plt.subplots(1, 2, figsize=(10, 4))
	sns.scatterplot(x=y_test, y=y_pred, ax=axs[0])
	axs[0].set_xlabel("Actual")
	axs[0].set_ylabel("Predicted")
	axs[0].set_title("Predicted vs Actual")

	residuals = y_test - y_pred
	sns.histplot(residuals, kde=True, ax=axs[1])
	axs[1].set_title("Residual distribution")
	st.pyplot(fig, clear_figure=True)
