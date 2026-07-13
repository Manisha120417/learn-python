import requests

url = "https://api.open-meteo.com/v1/forecast?latitude=27.7172&longitude=85.3240&current=temperature_2m"

response = requests.get(url)

print("Status Code:", response.status_code)

data = response.json()

print("\nCurrent Weather")
print("----------------")
print("Temperature:", data["current"]["temperature_2m"], "°C")
