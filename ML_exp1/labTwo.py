import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestClassifier

# -----------------
# Load dataset
# -----------------
df = pd.read_csv("plant_prediction_dataset.csv")  # <-- your dataset name

# Encode categorical columns
le_city = LabelEncoder()
le_soil = LabelEncoder()
le_plant = LabelEncoder()

df['City'] = le_city.fit_transform(df['City'])
df['Soil Type'] = le_soil.fit_transform(df['Soil Type'])
df['Plant Type'] = le_plant.fit_transform(df['Plant Type'])

# -----------------
# Split data
# -----------------
X = df.drop(columns=['Plant Type'])
y = df['Plant Type']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# -----------------
# Train model
# -----------------
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# -----------------
# Now you can safely pick random samples
# -----------------
random_indices = np.random.choice(X_test.index, 10, replace=False)
sample_actual = y_test.loc[random_indices]
sample_pred = model.predict(X_test.loc[random_indices])

# -----------------
# Scatter + regression line plot
# -----------------
actual_numeric = sample_actual.values.reshape(-1, 1)
pred_numeric = sample_pred.reshape(-1, 1)

reg = LinearRegression()
reg.fit(actual_numeric, pred_numeric)
line_x = np.linspace(min(sample_actual.min(), sample_pred.min()),
                     max(sample_actual.max(), sample_pred.max()), 100).reshape(-1, 1)
line_y = reg.predict(line_x)

plt.figure(figsize=(8,5))
plt.scatter(sample_actual, sample_pred, color='blue', label='Data Points')
plt.plot(line_x, line_y, color='red', linewidth=2, label='Regression Line')
plt.xlabel("Actual Encoded Plant Type")
plt.ylabel("Predicted Encoded Plant Type")
plt.title("Actual vs Predicted Plant Types (with Regression Line)")
plt.legend()
plt.show()
