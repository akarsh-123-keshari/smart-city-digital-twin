from flask import Flask, render_template, request
import pickle
import pandas as pd
import sys
import os
import requests

# Root path add
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from database import create_table, save_prediction, get_history

app = Flask(__name__, template_folder="../templates")

# Load ML model
with open("smart_city_model.pkl", "rb") as f:
    model = pickle.load(f)

create_table()
API_KEY = "7d90610e81b2dfa7c31b3e6f067bd4c2"
TOMTOM_API_KEY = "T3qRRxQa1y1oJDjKIKhmoLi5EkrqOBtd"
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
city_map = {
    "Zone1": "Mumbai",
    "Zone2": "Delhi",
    "Zone3": "Kolkata",
    "Zone4": "Chennai",
    "Zone5": "Bangalore",
    "Zone6": "Hyderabad",
    "Zone7": "Pune",
    "Zone8": "Ahmedabad",
    "Zone9": "Jaipur",
    "Zone10": "Lucknow",
    "Zone11": "Patna",
    "Zone12": "Surat"
}

@app.route("/", methods=["GET", "POST"])
def home():

    prediction = None
    weather = None
    alerts = []
    trend_data = []

    if request.method == "POST":

        zone = request.form["zone"]
        hour = int(request.form["hour"])
        day = int(request.form["day"])

        zone_encoded = zone_map.get(zone, 1)

        # Current prediction
        is_weekend = 1 if day % 7 in [6, 0] else 0
        is_peak_hour = 1 if (7 <= hour <= 10 or 17 <= hour <= 20) else 0

        future = pd.DataFrame({
            "zone_encoded": [zone_encoded],
            "hour": [hour],
            "day": [day],
            "is_weekend": [is_weekend],
            "is_peak_hour": [is_peak_hour]
        })

        pred = model.predict(future)[0]

        traffic = int(pred[0])
        aqi = int(pred[1])
        fuel = round(pred[2], 2)
        power = int(pred[3])
        
        # Real Weather API
        # -------------------------------
        city = city_map.get(zone, "Mumbai")

        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

        response = requests.get(url)

        weather_data = response.json()

        weather = weather_data["weather"][0]["description"]
        temperature = weather_data["main"]["temp"]
        humidity = weather_data["main"]["humidity"]
        # -------------------------------
       # Live AQI API
        lat = weather_data["coord"]["lat"]
        lon = weather_data["coord"]["lon"]

        aqi_url = (
            f"https://api.openweathermap.org/data/2.5/air_pollution"
            f"?lat={lat}&lon={lon}&appid={API_KEY}"
        )

        aqi_response = requests.get(aqi_url)
        aqi_data = aqi_response.json()

        live_aqi = aqi_data["list"][0]["main"]["aqi"]

        if live_aqi == 1:
            live_aqi_text = "Good"
        elif live_aqi == 2:
            live_aqi_text = "Fair"
        elif live_aqi == 3:
            live_aqi_text = "Moderate"
        elif live_aqi == 4:
            live_aqi_text = "Poor"
        else:
            live_aqi_text = "Very Poor"
         # -------------------------------
        # Live Traffic API
        # -------------------------------

        traffic_url = (
            f"https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json"
            f"?key={TOMTOM_API_KEY}&point={lat},{lon}"
        )

        traffic_response = requests.get(traffic_url)
        traffic_data = traffic_response.json()

        current_speed = traffic_data["flowSegmentData"]["currentSpeed"]
        free_speed = traffic_data["flowSegmentData"]["freeFlowSpeed"]

        traffic_congestion = round(
            100 - ((current_speed / free_speed) * 100),
            2
        )

        if traffic_congestion < 30:
            traffic_status = "Low"
        elif traffic_congestion < 60:
            traffic_status = "Moderate"
        else:
            traffic_status = "Heavy"

        # Alerts
        if traffic > 300:
            alerts.append("🚦 High Traffic Alert")
        if aqi > 150:
            alerts.append("😷 Pollution Risk")
        if fuel > 8:
            alerts.append("⛽ High Fuel Consumption")
        if power > 650:
            alerts.append("⚡ Power Demand Risk")
        if not alerts:
            alerts.append("✅ System Stable")

        prediction = {
        "zone": zone,
        "hour": hour,
        "day": day,

        "traffic": traffic,

        "aqi": aqi,   # ML Predicted AQI

        "live_aqi": live_aqi,   # Real AQI
        "live_aqi_text": live_aqi_text,
        "traffic_congestion": traffic_congestion,
        "traffic_status": traffic_status,

        "weather": weather,

        "temperature": temperature,
        "humidity": humidity,

        "fuel": fuel,
        "power": power
    }

        # Save DB
        save_prediction(
            zone, hour, day,
            traffic, aqi, weather,
            fuel, power
        )

        # -------------------------------
        # 6-Hour Future Trend
        # -------------------------------
        for i in range(6):
            future_hour = (hour + i) % 24
            future_day = day + ((hour + i) // 24)

            is_weekend = 1 if future_day % 7 in [6, 0] else 0
            is_peak_hour = 1 if (
                7 <= future_hour <= 10 or
                17 <= future_hour <= 20
            ) else 0

            future_input = pd.DataFrame({
                "zone_encoded": [zone_encoded],
                "hour": [future_hour],
                "day": [future_day],
                "is_weekend": [is_weekend],
                "is_peak_hour": [is_peak_hour]
            })

            future_pred = model.predict(future_input)[0]

            future_aqi = int(future_pred[1])

            # Future weather
            if future_aqi < 80:
                future_weather = "Clear ☀️"
                weather_code = 0
            elif future_aqi < 140:
                future_weather = "Cloudy ☁️"
                weather_code = 1
            else:
                future_weather = "Poor Air / Dusty 🌫️"
                weather_code = 2

            trend_data.append({
                "hour": future_hour,
                "traffic": int(future_pred[0]),
                "aqi": future_aqi,
                "fuel": round(future_pred[2], 2),
                "power": int(future_pred[3]),
                "weather": future_weather,
                "weather_code": weather_code
            })

    history = get_history(20)

    return render_template(
        "index.html",
        prediction=prediction,
        weather=weather,
        alerts=alerts,
        history=history,
        trend_data=trend_data
    )


if __name__ == "__main__":
    app.run(debug=True)