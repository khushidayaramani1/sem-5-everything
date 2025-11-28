import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Generate synthetic dataset
np.random.seed(42)
n = 200
temperature = np.random.randint(15, 40, n)
rainfall = np.random.randint(50, 400, n)
humidity = np.random.randint(40, 90, n)
soil_ph = np.round(np.random.uniform(6.0, 7.5, n), 2)

yield_data = (temperature * 20 + rainfall * 15 + humidity * 10 - soil_ph * 50) + np.random.randint(-500, 500, n)

df = pd.DataFrame({
    'Temperature': temperature,
    'Rainfall': rainfall,
    'Humidity': humidity,
    'Soil_pH': soil_ph,
    'Yield': yield_data
})

# Features and target (only Rainfall for 2D plotting)
X = df[['Rainfall']]
y = df['Yield']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Train Linear Regression with NO intercept (line goes through origin)
model = LinearRegression(fit_intercept=False)
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)

# ✅ Model Evaluation Metrics
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)

print("\n📊 Model Evaluation Metrics (Through Origin):")
print("Mean Absolute Error (MAE):", mae)
print("Mean Squared Error (MSE):", mse)
print("Root Mean Squared Error (RMSE):", rmse)
print("R² Score:", r2)

# 📈 Visualization
# Scatter: Test Data (green dots)
plt.scatter(X_test, y_test, color="green", label="Test data")

# Regression line (straight red line through origin)
x_line = np.linspace(0, X.max(), 100).reshape(-1, 1)   # starts from 0
y_line = model.predict(x_line)
plt.plot(x_line, y_line, color="red", linewidth=2, label="Regression line (through origin)")

# Pick 10 random samples from test set for highlighting
sample_idx = np.random.choice(range(len(X_test)), size=10, replace=False)
X_sample = X_test.iloc[sample_idx]
y_actual_sample = y_test.iloc[sample_idx]
y_pred_sample = y_pred[sample_idx]

# Actual samples (orange circles)
plt.scatter(X_sample, y_actual_sample, color="orange", s=100, edgecolor="black", label="Actual (Sample)")

# Predicted samples (purple X)
plt.scatter(X_sample, y_pred_sample, color="purple", marker="x", s=100, label="Predicted (Sample)")

# Labels & Title
plt.xlabel("Rainfall (mm)")
plt.ylabel("Yield (kg/acre)")
plt.title("Test Data Predictions vs Actual Yield (Through Origin)")
plt.legend()
plt.grid(True)
plt.show()
