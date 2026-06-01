import requests

API_KEY = "7d90610e81b2dfa7c31b3e6f067bd4c2"

city = "Mumbai"

url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={"7d90610e81b2dfa7c31b3e6f067bd4c2"}&units=metric"

response = requests.get(url)

data = response.json()

print(data)

print("\n------ LIVE WEATHER ------")
print("City:", data["name"])
print("Temperature:", data["main"]["temp"], "°C")
print("Weather:", data["weather"][0]["description"])
print("Humidity:", data["main"]["humidity"])