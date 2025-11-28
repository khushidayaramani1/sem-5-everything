import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset (replace filename with your CSV)
df = pd.read_csv("plant_prediction_dataset.csv")

df.rename(columns={
    "Temperature (°C)": "Temperature",   # <-- this one is important
    "Rainfall": "Rainfall",
    "Humidity": "Humidity",
    "Sunlight": "Sunlight"
}, inplace=True)

print(df.columns)  # check again


plt.figure(figsize=(10,5))
avg_temp = df.groupby("Plant Type")["Temperature"].mean().sort_values()
avg_temp.plot(kind="bar", color="skyblue")
plt.title("Average Temperature Required by Each Plant")
plt.xlabel("Plant Type")
plt.ylabel("Average Temperature (°C)")
plt.show()

plt.figure(figsize=(12,5))
avg_rainfall = df.groupby("Plant Type")["Rainfall (mm)"].mean()
avg_rainfall.plot(kind="line", marker='o', color="green")
plt.title("Average Rainfall Requirement per Plant")
plt.xlabel("Plant Type")
plt.ylabel("Average Rainfall (mm)")
plt.grid(True)
plt.show()

plt.figure(figsize=(6,6))
soil_counts = df["Soil Type"].value_counts()
plt.pie(soil_counts, labels=soil_counts.index, autopct="%1.1f%%", startangle=90, colors=sns.color_palette("pastel"))
plt.title("Soil Type Distribution")
plt.show()

plt.figure(figsize=(8,5))
plt.hist(df["pH"], bins=15, color="orange", edgecolor="black")
plt.title("Distribution of Soil pH Levels")
plt.xlabel("pH Value")
plt.ylabel("Frequency")
plt.show()

plt.figure(figsize=(10,6))
sns.scatterplot(x="Humidity (%)", y="Sunlight (hrs)", hue="Plant Type", data=df, palette="tab10")
plt.title("Humidity vs Sunlight for Different Plants")
plt.xlabel("Humidity (%)")
plt.ylabel("Sunlight (hrs)")
plt.show()
