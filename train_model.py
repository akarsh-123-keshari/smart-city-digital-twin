import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import pickle

# -------------------------------
# Load dataset
# -------------------------------
df = pd.read_csv("data/city_data.csv")

print("Dataset loaded successfully!")
print("Total rows:", len(df))

# -------------------------------
# Zone Encoding (12 Zones)
# -------------------------------
zone_map = {
    "Zone1": 1,
    "Zone2": 2,
    "Zone3": 3,
    "Zone4": 4,
    "Zone5": 5,
    "Zone6": 6,
    "Zone7": 7,
    "Zone8": 8,
    "Zone9": 9,
    "Zone10": 10,
    "Zone11": 11,
    "Zone12": 12
}

df["zone_encoded"] = df["zone"].map(zone_map)

# -------------------------------
# Features (Inputs)
# -------------------------------
X = df[[
    "zone_encoded",
    "hour",
    "day",
    "is_weekend",
    "is_peak_hour"
]]

# -------------------------------
# Targets (Outputs)
# -------------------------------
y = df[[
    "traffic",
    "aqi",
    "fuel_consumption",
    "power"
]]

# -------------------------------
# Train Model
# -------------------------------
model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

model.fit(X, y)

print("Model training completed!")

# -------------------------------
# Save Model
# -------------------------------
with open("smart_city_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Model saved as smart_city_model.pkl")