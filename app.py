import pandas as pd
import pickle
import matplotlib.pyplot as plt

# -------------------------------
# Load trained model
# -------------------------------
try:
    with open("smart_city_model.pkl", "rb") as f:
        model = pickle.load(f)
    print("✅ Model loaded successfully!")
except:
    print("❌ Model file not found. Run train_model.py first.")
    exit()

# -------------------------------
# User input
# -------------------------------
zone_input = input("Enter Zone (Zone1-Zone5): ")
hour_input = int(input("Enter Current Hour (0-23): "))
day_input = int(input("Enter Current Day (1-365): "))

print("\n==============================")
print(" SMART CITY PREDICTION SYSTEM ")
print("==============================")

alerts_triggered = False

# Weather labels
weather_map = {
    0: "Clear",
    1: "Cloudy",
    2: "Rain"
}

# Graph storage
forecast_steps = []
traffic_list = []
aqi_list = []
fuel_list = []
power_list = []

# -------------------------------
# Current + Next 6 hour forecast
# -------------------------------
for i in range(0, 7):

    future_hour = (hour_input + i) % 24
    future_day = day_input

    # Day rollover
    if hour_input + i >= 24:
        future_day += 1

    is_weekend = 1 if future_day % 7 in [6, 0] else 0
    is_peak_hour = 1 if (7 <= future_hour <= 10 or 17 <= future_hour <= 20) else 0

    future = pd.DataFrame({
        'hour': [future_hour],
        'day': [future_day],
        'is_weekend': [is_weekend],
        'is_peak_hour': [is_peak_hour]
    })

    prediction = model.predict(future)[0]

    traffic = int(prediction[0])
    aqi = int(prediction[1])
    weather = int(prediction[2])
    fuel = round(prediction[3], 2)
    power = int(prediction[4])

    weather_text = weather_map.get(weather, "Unknown")

    # Save for graph (continuous timeline)
    forecast_steps.append(i)
    traffic_list.append(traffic)
    aqi_list.append(aqi)
    fuel_list.append(fuel)
    power_list.append(power)

    print(f"\n🕒 Time: {future_hour}:00")
    print(f"Traffic: {traffic} vehicles/hour")
    print(f"AQI: {aqi} AQI")
    print(f"Weather: {weather_text}")
    print(f"Fuel Consumption: {fuel} L/hour")
    print(f"Power Demand: {power} kW")

    # -------------------------------
    # Alerts
    # -------------------------------
    if traffic > 320:
        print("⚠ High Traffic Expected")
        alerts_triggered = True

    if aqi > 180:
        print("⚠ Pollution Risk Expected")
        alerts_triggered = True

    if weather == 2:
        print("⚠ Rain Expected")
        alerts_triggered = True

    if fuel > 18:
        print("⚠ High Fuel Consumption Expected")
        alerts_triggered = True

    if power > 500:
        print("⚠ High Power Demand Expected")
        alerts_triggered = True

# -------------------------------
# Final summary
# -------------------------------
print("\n==============================")

if alerts_triggered:
    print("🚨 EARLY WARNING: Risks detected in upcoming hours!")
else:
    print("✅ System Stable: No major risks detected.")

print("==============================")

# -------------------------------
# Graph Visualization
# -------------------------------
plt.figure(figsize=(10, 6))

plt.plot(forecast_steps, traffic_list, marker='o', label="Traffic")
plt.plot(forecast_steps, aqi_list, marker='o', label="AQI")
plt.plot(forecast_steps, fuel_list, marker='o', label="Fuel Consumption")
plt.plot(forecast_steps, power_list, marker='o', label="Power Demand")

plt.xlabel("Forecast Hours (0 = current, 6 = next 6th hour)")
plt.ylabel("Prediction Values")
plt.title("Smart City Forecast Timeline (Next 6 Hours)")
plt.legend()
plt.grid(True)

plt.show()