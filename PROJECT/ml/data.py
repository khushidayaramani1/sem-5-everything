from __future__ import annotations

from dataclasses import dataclass
from typing import List

import numpy as np
import pandas as pd
from sklearn.datasets import load_iris, load_wine, load_breast_cancer, fetch_california_housing


EXAMPLE_NAME_TO_LOADER = {
	"Example: Iris (classification)": load_iris,
	"Example: Wine (classification)": load_wine,
	"Example: Breast Cancer (classification)": load_breast_cancer,
	"Example: California Housing (regression)": fetch_california_housing,
}


def load_example_dataset(name: str) -> pd.DataFrame:
	loader = EXAMPLE_NAME_TO_LOADER[name]
	bunch = loader()

	if hasattr(bunch, "frame") and bunch.frame is not None:
		df = bunch.frame.copy()
	else:
		data = bunch.data
		feature_names = list(bunch.feature_names)
		df = pd.DataFrame(data, columns=feature_names)
		if hasattr(bunch, "target"):
			df["target"] = bunch.target
	return df


def ensure_numeric_dataframe(df: pd.DataFrame) -> pd.DataFrame:
	numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
	if len(numeric_cols) == 0:
		raise ValueError("No numeric columns found. Provide numeric data or encode categoricals.")
	return df[numeric_cols].copy()


@dataclass
class SplitData:
	X_train: np.ndarray
	X_test: np.ndarray
	y_train: np.ndarray
	y_test: np.ndarray
	feature_names: List[str]


def split_supervised(
	df: pd.DataFrame,
	target_column: str,
	test_size: float = 0.2,
	random_state: int = 42,
	one_hot_encode_categoricals: bool = True,
) -> SplitData:
	from sklearn.model_selection import train_test_split
	from sklearn.compose import ColumnTransformer
	from sklearn.preprocessing import OneHotEncoder

	X = df.drop(columns=[target_column])
	y = df[target_column]

	categorical_cols = X.select_dtypes(include=["object", "category"]).columns.tolist()
	numeric_cols = X.select_dtypes(include=[np.number]).columns.tolist()

	transformers = []
	if one_hot_encode_categoricals and len(categorical_cols) > 0:
		transformers.append((
			"cat",
			OneHotEncoder(handle_unknown="ignore", sparse_output=False),
			categorical_cols,
		))
	if len(numeric_cols) > 0:
		transformers.append(("num", "passthrough", numeric_cols))

	if len(transformers) == 0:
		X_proc = X.to_numpy()
		feature_names = list(X.columns)
	else:
		ct = ColumnTransformer(transformers)
		X_proc = ct.fit_transform(X)
		feature_names = []
		for name, trans, cols in transformers:
			if name == "cat":
				encoder = ct.named_transformers_["cat"]
				enc_names = encoder.get_feature_names_out(cols).tolist()
				feature_names.extend(enc_names)
			else:
				feature_names.extend(cols)

	X_train, X_test, y_train, y_test = train_test_split(
		X_proc, y.to_numpy(), test_size=test_size, random_state=random_state
	)

	return SplitData(
		X_train=X_train,
		X_test=X_test,
		y_train=y_train,
		y_test=y_test,
		feature_names=feature_names,
	)
