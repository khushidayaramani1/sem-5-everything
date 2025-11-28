from __future__ import annotations

import numpy as np
import pandas as pd
import streamlit as st
from typing import List
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import seaborn as sns


def run_linear_regression(df: pd.DataFrame) -> None:
	st.subheader("Linear Regression")

	num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
	if len(num_cols) < 2:
		st.error("Need at least 2 numeric columns (features + target).")
		return

	target = st.selectbox("Select target column (numeric)", num_cols, index=len(num_cols) - 1, key="lr_target")
	feature_candidates = [c for c in num_cols if c != target]
	features = st.multiselect("Select feature columns", feature_candidates, default=feature_candidates[:1], key="lr_features")
	if len(features) == 0:
		st.warning("Select at least one feature column.")
		return

	test_size = st.slider("Test size", 0.1, 0.5, value=0.2, step=0.05, key="lr_test_size")
	random_state = st.number_input("Random state", min_value=0, value=42, step=1, key="lr_random_state")

	X = df[features].to_numpy()
	y = df[target].to_numpy()
	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)

	model = LinearRegression()
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

	with st.expander("Coefficients", expanded=True):
		coef_df = pd.DataFrame({"feature": features, "coefficient": model.coef_})
		coef_df["sign"] = np.where(coef_df["coefficient"] >= 0, "+", "-")
		st.dataframe(coef_df, use_container_width=True)
		st.write(f"Intercept: {model.intercept_:.4f}")

	# Actual vs Predicted table (sample)
	with st.expander("Actual vs Predicted (test set)", expanded=True):
		show_n = st.slider("Rows to show", 5, min(50, len(y_test)), value=min(20, len(y_test)), key="lr_rows_show")
		ap = pd.DataFrame({"actual": y_test, "predicted": y_pred})
		st.dataframe(ap.head(show_n), use_container_width=True)

	# Single-feature: slope sign and regression line with actual points
	if len(features) == 1:
		slope = float(model.coef_[0])
		slope_sign = "positive" if slope >= 0 else "negative"
		st.info(f"Slope for {features[0]} -> {target}: {slope:.4f} ({slope_sign})")

		# Build regression line over full range
		xfull = df[features[0]].to_numpy().reshape(-1, 1)
		yline = model.predict(xfull)

		fig, ax = plt.subplots(figsize=(7, 5))
		sns.scatterplot(x=df[features[0]], y=df[target], color="tab:blue", alpha=0.6, ax=ax, label="Actual points")
		sns.lineplot(x=df[features[0]], y=yline, color="tab:red", ax=ax, label="Regression line")
		ax.set_xlabel(features[0])
		ax.set_ylabel(target)
		ax.set_title("Actual points and regression line")
		st.pyplot(fig, clear_figure=True)

	st.markdown("**Residuals and predictions**")
	fig, axs = plt.subplots(1, 2, figsize=(10, 4))
	sns.scatterplot(x=y_test, y=y_pred, ax=axs[0])
	axs[0].set_xlabel("Actual")
	axs[0].set_ylabel("Predicted")
	axs[0].set_title("Predicted vs Actual")

	residuals = y_test - y_pred
	sns.histplot(residuals, kde=True, ax=axs[1])
	axs[1].set_title("Residual distribution")
	st.pyplot(fig, clear_figure=True)
