# nested_if.py

age = int(input("Enter your age: "))
citizen = input("Are you a citizen? (yes/no): ")

if age >= 18:
    if citizen.lower() == "yes":
        print("You are eligible to vote.")
    else:
        print("You must be a citizen to vote.")
else:
    print("You are under 18 and cannot vote.")