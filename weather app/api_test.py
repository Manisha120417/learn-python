import requests

url = "https://api.open-meteo.com/v1/forecast?latitude=27.7172&longitude=85.3240&current=temperature_2m"

response = requests.get(url)

# Check API connection
if response.status_code == 200:
    print("API Connected Successfully")
else:
    print("Connection Failed")

# Convert response to JSON
data = response.json()

# Display weather information
print("\nWeather Report")
print("----------------")
print("Temperature:", data["current"]["temperature_2m"], "°C")