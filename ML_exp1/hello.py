# ---------------- Import Libraries ----------------
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.preprocessing import LabelEncoder, StandardScaler
from mpl_toolkits.mplot3d import Axes3D
# from google.colab import files  # Commented out for local Python
import warnings
warnings.filterwarnings('ignore')

# ---------------- File Upload ----------------
# For local Python environment (not Google Colab)
print("📂 Loading plant dataset...")
try:
    # Try to load the file directly (assumes it's in the same directory)
    file_path = "plant_data.csv"
    df = pd.read_csv("plant_prediction_dataset.csv")
except FileNotFoundError:
    # If file not found, prompt user for file path
    file_path = input("Please enter the full path to your CSV file: ")
    df = pd.read_csv(file_path)

# ---------------- Load Dataset ----------------
try:
    df = pd.read_csv(file_path)
    print("\nPlant dataset successfully loaded.")
    print("Shape:", df.shape)
    print("Columns:", df.columns.tolist())
    print("Dataset Head:\n", df.head())
    print("\nUnique Plant Types:", df['Plant Type'].unique())
    print("Plant Type Distribution:\n", df['Plant Type'].value_counts())
except Exception as e:
    print(f"Error loading file: {e}")
    exit()

# ---------------- Data Preprocessing ----------------
# Encode categorical variables
le_soil = LabelEncoder()
le_city = LabelEncoder()
le_plant = LabelEncoder()

df['Soil_Type_Encoded'] = le_soil.fit_transform(df['Soil Type'])
df['City_Encoded'] = le_city.fit_transform(df['City'])
df['Plant_Type_Encoded'] = le_plant.fit_transform(df['Plant Type'])

# Features and target
features = ['pH', 'Temperature (°C)', 'Rainfall (mm)', 'Humidity (%)', 
           'Sunlight (hrs)', 'Soil_Type_Encoded', 'City_Encoded']
target = 'Plant_Type_Encoded'

X = df[features]
y = df[target]

# Standardize features for better performance
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# ---------------- Train-Test Split ----------------
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42
)

# ---------------- Train Models ----------------
# Random Forest Classifier (generally performs well for this type of data)
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# Logistic Regression for comparison
lr_model = LogisticRegression(random_state=42, max_iter=1000)
lr_model.fit(X_train, y_train)

# ---------------- Predictions ----------------
rf_pred = rf_model.predict(X_test)
lr_pred = lr_model.predict(X_test)

# ---------------- Model Evaluation ----------------
rf_accuracy = accuracy_score(y_test, rf_pred)
lr_accuracy = accuracy_score(y_test, lr_pred)

print("\n" + "="*60)
print("MODEL EVALUATION RESULTS")
print("="*60)

print(f"\n🌿 RANDOM FOREST CLASSIFIER")
print(f"Accuracy: {rf_accuracy:.4f} ({rf_accuracy*100:.2f}%)")

print(f"\n🌾 LOGISTIC REGRESSION")  
print(f"Accuracy: {lr_accuracy:.4f} ({lr_accuracy*100:.2f}%)")

# Feature importance for Random Forest
print(f"\n📊 FEATURE IMPORTANCE (Random Forest):")
feature_importance = pd.DataFrame({
    'Feature': features,
    'Importance': rf_model.feature_importances_
}).sort_values('Importance', ascending=False)

for idx, row in feature_importance.iterrows():
    print(f"  {row['Feature']}: {row['Importance']:.4f}")

# Classification report for the better model
better_model = rf_model if rf_accuracy > lr_accuracy else lr_model
better_pred = rf_pred if rf_accuracy > lr_accuracy else lr_pred
model_name = "Random Forest" if rf_accuracy > lr_accuracy else "Logistic Regression"

print(f"\n📋 DETAILED CLASSIFICATION REPORT ({model_name}):")
# Get unique classes in test set to match target names
unique_test_classes = np.unique(np.concatenate([y_test, better_pred]))
target_names_filtered = [le_plant.classes_[i] for i in unique_test_classes]

print(classification_report(y_test, better_pred, 
                          labels=unique_test_classes,
                          target_names=target_names_filtered))

print("="*60)

# ---------------- Visualizations ----------------

# 1. Confusion Matrix
plt.figure(figsize=(12, 8))
cm = confusion_matrix(y_test, better_pred, labels=unique_test_classes)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
            xticklabels=target_names_filtered, 
            yticklabels=target_names_filtered)
plt.title(f'Confusion Matrix - {model_name}', fontsize=16)
plt.xlabel('Predicted Plant Type', fontsize=12)
plt.ylabel('Actual Plant Type', fontsize=12)
plt.xticks(rotation=45)
plt.yticks(rotation=45)
plt.tight_layout()
plt.show()

# 2. Feature Importance Plot
plt.figure(figsize=(10, 8))
feature_importance_sorted = feature_importance.sort_values('Importance')
plt.barh(range(len(feature_importance_sorted)), feature_importance_sorted['Importance'], 
         color='forestgreen', alpha=0.8)
plt.yticks(range(len(feature_importance_sorted)), feature_importance_sorted['Feature'])
plt.xlabel('Feature Importance', fontsize=12)
plt.title('Feature Importance in Plant Type Prediction', fontsize=14)
plt.grid(axis='x', alpha=0.3)
plt.tight_layout()
plt.show()

# 3. 3D Scatter Plot: pH vs Temperature vs Rainfall (colored by plant type)
fig = plt.figure(figsize=(12, 9))
ax = fig.add_subplot(111, projection='3d')

# Create color map for plant types
plant_types = df['Plant Type'].unique()
colors = plt.cm.Set3(np.linspace(0, 1, len(plant_types)))
color_map = dict(zip(plant_types, colors))

for plant in plant_types:
    plant_data = df[df['Plant Type'] == plant]
    ax.scatter(plant_data['pH'], 
              plant_data['Temperature (°C)'], 
              plant_data['Rainfall (mm)'],
              c=[color_map[plant]], 
              label=plant, 
              alpha=0.7, 
              s=50)

ax.set_xlabel('pH Level', fontsize=12)
ax.set_ylabel('Temperature (°C)', fontsize=12)
ax.set_zlabel('Rainfall (mm)', fontsize=12)
ax.set_title('3D Distribution: pH × Temperature × Rainfall by Plant Type', fontsize=14)
ax.legend(bbox_to_anchor=(1.15, 1), loc='upper left')
plt.tight_layout()
plt.show()

# 4. Environmental Conditions Distribution by Plant Type
fig, axes = plt.subplots(2, 3, figsize=(18, 12))
environmental_vars = ['pH', 'Temperature (°C)', 'Rainfall (mm)', 
                     'Humidity (%)', 'Sunlight (hrs)']

for i, var in enumerate(environmental_vars):
    row = i // 3
    col = i % 3
    
    df.boxplot(column=var, by='Plant Type', ax=axes[row, col])
    axes[row, col].set_title(f'{var} by Plant Type')
    axes[row, col].set_xlabel('Plant Type')
    axes[row, col].set_ylabel(var)
    axes[row, col].tick_params(axis='x', rotation=45)

# Remove the last empty subplot
axes[1, 2].axis('off')

plt.suptitle('Environmental Conditions Distribution by Plant Type', 
             fontsize=16, y=1.02)
plt.tight_layout()
plt.show()

# 5. Correlation Heatmap
plt.figure(figsize=(12, 10))
correlation_vars = ['pH', 'Temperature (°C)', 'Rainfall (mm)', 
                   'Humidity (%)', 'Sunlight (hrs)', 'Plant_Type_Encoded']
corr_matrix = df[correlation_vars].corr()

sns.heatmap(corr_matrix, annot=True, cmap='RdYlBu_r', center=0,
            square=True, fmt='.3f')
plt.title('Correlation Matrix: Environmental Factors & Plant Types', fontsize=14)
plt.tight_layout()
plt.show()

# ---------------- Prediction Example ----------------
print("\n" + "="*60)
print("SAMPLE PREDICTION")
print("="*60)

# Example prediction for new data
sample_data = np.array([[7.0, 25.0, 1500, 60, 7.0, 2, 1]])  # pH, Temp, Rainfall, Humidity, Sunlight, Soil(encoded), City(encoded)
sample_scaled = scaler.transform(sample_data)
prediction = better_model.predict(sample_scaled)[0]
predicted_plant = le_plant.inverse_transform([prediction])[0]

print("Sample Environmental Conditions:")
print(f"  pH: 7.0")
print(f"  Temperature: 25.0°C")
print(f"  Rainfall: 1500mm")
print(f"  Humidity: 60%")
print(f"  Sunlight: 7.0 hours")
print(f"  Predicted Plant Type: {predicted_plant}")

# Prediction probabilities (if using Random Forest)
if isinstance(better_model, RandomForestClassifier):
    probabilities = better_model.predict_proba(sample_scaled)[0]
    print(f"\nPrediction Probabilities:")
    for i, prob in enumerate(probabilities):
        plant_name = le_plant.inverse_transform([i])[0]
        print(f"  {plant_name}: {prob:.3f} ({prob*100:.1f}%)")

print("="*60)