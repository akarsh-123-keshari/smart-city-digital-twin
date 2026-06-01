import requests

API_KEY = "T3qRRxQa1y1oJDjKIKhmoLi5EkrqOBtd"

# Mumbai coordinates
lat = 19.0760
lon = 72.8777

url = (
    f"https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json"
    f"?key={API_KEY}&point={lat},{lon}"
)

response = requests.get(url)

data = response.json()

print("Current Speed:", data["flowSegmentData"]["currentSpeed"])
print("Free Flow Speed:", data["flowSegmentData"]["freeFlowSpeed"])

current_speed = data["flowSegmentData"]["currentSpeed"]
free_speed = data["flowSegmentData"]["freeFlowSpeed"]

congestion = round(
    100 - ((current_speed / free_speed) * 100),
    2
)

print("Traffic Congestion:", congestion, "%")