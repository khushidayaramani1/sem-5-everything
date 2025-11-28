## ML Playground (Streamlit)

An interactive Streamlit app to explore classic ML workflows on your own CSV or built‑in example datasets. It includes:

- Data Visualization (distributions, correlations, pairplots)
- Linear Regression (metrics, coefficients, slope sign for single-feature, residuals)
- Multivariate Nonlinear Regression (PolynomialFeatures + Ridge)
- Decision Tree Classification (ID3-style entropy support, confusion matrix, tree visualization)
- SVM Classification (metrics, ROC AUC for binary, confusion matrix, 2D hyperplane when feasible)
- Ensemble Learning (RandomForest bagging and GradientBoosting boosting)
- Clustering (KMeans / DBSCAN) with 2D cluster visualization
- Dimensionality Reduction (PCA / TruncatedSVD) with explained variance and 2D projection


### 1) Getting Started

Prerequisites:
- Python 3.10+
- pip

Install dependencies:
```bash
pip install -r requirements.txt
```

Run the app:
```bash
streamlit run app.py
```

Streamlit will open a local URL (e.g., `http://localhost:8501`).


### 2) Project Structure

```
.
├── app.py                     # Streamlit UI & routing
├── requirements.txt
├── ml/
│   ├── __init__.py
│   ├── data.py                # Dataset loading/utilities (examples, encoding, splitting)
│   ├── visualization.py       # EDA plots
│   ├── regression_linear.py   # Linear Regression
│   ├── regression_nonlinear.py# Polynomial + Ridge regression
│   ├── classification_tree.py # Decision Tree classification + visualization
│   ├── classification_svm.py  # SVM classification + ROC
│   ├── ensemble.py            # RandomForest & GradientBoosting
│   ├── clustering.py          # KMeans & DBSCAN
│   └── dimreduction.py        # PCA & TruncatedSVD
```


### 3) Usage Guide

- Sidebar → choose a dataset source:
  - Upload CSV: Provide your own data (CSV). Ensure a `target` column exists for supervised tasks.
  - Example datasets: Iris, Wine, Breast Cancer, California Housing.
- Sidebar → choose a task:
  - Data Visualization: Explore summary, distribution plots, correlations, pairplots.
  - Linear Regression: Select numeric features and a numeric target; shows metrics, coefficients, residuals.
    - If you select exactly one feature, the app displays the slope sign (positive/negative), actual points, and regression line.
  - Multivariate Nonlinear Regression: PolynomialFeatures + Ridge; tune degree and alpha.
  - Decision Tree Classification: Select target; model uses one-hot encoding for categoricals; shows confusion matrix and a tree preview.
  - SVM Classification: Select kernel (rbf/linear/poly/sigmoid), C, gamma.
    - For binary targets, ROC AUC and ROC curve are shown.
    - For two selected numeric features, a 2D hyperplane plot is displayed (if separable and kernel supports it).
  - Ensemble Learning: RandomForest (bagging) or GradientBoosting (boosting); top feature importances when available.
  - Clustering: KMeans/DBSCAN; shows 2D scatter by first two selected features.
  - Dimensionality Reduction: PCA/SVD; shows explained variance and 2D projection plot.

Tips:
- For supervised tasks (regression/classification), ensure your data has a `target` column.
- Non-numeric columns are one-hot encoded automatically for classification tasks via the preprocessing pipeline.
- Some plots sample rows for speed (pairplots).


### 4) Working With Your CSV

- The app reads CSV headers as column names.
- For regression tasks, your target must be numeric.
- For classification, target can be numeric or categorical (strings are supported via encoding).
- Missing values: Basic handling is provided by pandas/encoders; ensure data quality for best results.


### 5) Algorithms & References

- Linear Regression: scikit-learn `LinearRegression`
- Polynomial Regression: `PolynomialFeatures` + `Ridge`
- Decision Trees: `DecisionTreeClassifier` (entropy for ID3-style)
- SVM: `SVC`
- Ensembles: `RandomForestClassifier`, `GradientBoostingClassifier`
- Clustering: `KMeans`, `DBSCAN`
- Dimensionality Reduction: `PCA`, `TruncatedSVD`


### 6) Troubleshooting

- Streamlit not found: Run `pip install -r requirements.txt`.
- Import errors: Check Python version (3.10+ recommended) and re-install requirements.
- App won’t open in browser: Copy the terminal URL (e.g., `http://localhost:8501`) into your browser.
- Large CSVs: Loading/plots may be slow; consider sampling your data first.


### 7) License

This project is provided for educational purposes. You may use and modify it freely in your coursework or personal projects.
