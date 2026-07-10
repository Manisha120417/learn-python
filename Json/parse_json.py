import json

# Open and read the JSON file
with open("sample.json", "r") as file:
    data = json.load(file)

# Print JSON data
print("Name:", data["name"])
print("Age:", data["age"])
print("City:", data["city"])
print("Country:", data["country"])

print("\nSkills:")
for skill in data["skills"]:
    print("-", skill)