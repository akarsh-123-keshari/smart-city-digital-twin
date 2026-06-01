import pandas as pd
import random
import os

# -------------------------------
# Create data folder
# -------------------------------
if not os.path.exists("data"):
    os.makedirs("data")

# -------------------------------
# 12 Zones / Cities
# -------------------------------
zones = [
    "Zone1",   # Mumbai
    "Zone2",   # Delhi
    "Zone3",   # Kolkata
    "Zone4",   # Chennai
    "Zone5",   # Bangalore
    "Zone6",   # Hyderabad
    "Zone7",   # Pune
    "Zone8",   # Ahmedabad
    "Zone9",   # Jaipur
    "Zone10",  # Lucknow
    "Zone11",  # Patna
    "Zone12"   # Surat
]

# -------------------------------
# Zone traffic behavior
# -------------------------------
zone_factor = {
    "Zone1": 1.35,
    "Zone2": 1.30,
    "Zone3": 1.10,
    "Zone4": 1.15,
    "Zone5": 1.20,
    "Zone6": 1.18,
    "Zone7": 1.05,
    "Zone8": 1.00,
    "Zone9": 0.92,
    "Zone10": 0.95,
    "Zone11": 0.90,
    "Zone12": 0.88
}

data = []

# -------------------------------
# Generate dataset
# -------------------------------
for zone in zones:

    for day in range(1, 366):

        for hour in range(24):

            # Weekend check
            is_weekend = 1 if day % 7 in [6, 0] else 0

            # Peak hour check
            is_peak_hour = 1 if (
                7 <= hour <= 10 or
                17 <= hour <= 20
            ) else 0

            # Base traffic
            if 7 <= hour <= 10:
                base_traffic = 240

            elif 17 <= hour <= 20:
                base_traffic = 420

            else:
                base_traffic = 140

            # Weekend reduction
            if is_weekend:
                base_traffic -= 30

            # Apply zone factor
            traffic = int(
                base_traffic * zone_factor[zone]
                + random.randint(-35, 35)
            )

            # AQI
            aqi = int(
                traffic * 0.6
                + zone_factor[zone] * 20
                + random.randint(-20, 20)
            )

            # Weather
            weather = random.choice([0, 1, 2])

            # Fuel consumption
            fuel_consumption = round(
                traffic * 0.05 * zone_factor[zone],
                2
            )

            # Power demand
            power = int(
                300
                + traffic * 0.55
                + zone_factor[zone] * 80
                + random.randint(-50, 50)
            )

            data.append([
                zone,
                day,
                hour,
                is_weekend,
                is_peak_hour,
                traffic,
                aqi,
                weather,
                fuel_consumption,
                power
            ])

# -------------------------------
# Create DataFrame
# -------------------------------
df = pd.DataFrame(data, columns=[
    "zone",
    "day",
    "hour",
    "is_weekend",
    "is_peak_hour",
    "traffic",
    "aqi",
    "weather",
    "fuel_consumption",
    "power"
])

# -------------------------------
# Save CSV
# -------------------------------
df.to_csv("data/city_data.csv", index=False)

print("Dataset generated successfully!")
print("Total rows:", len(df))