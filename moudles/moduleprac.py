# import math
# print(math.pi)
# result = math.sqrt(144)
# print(result)

# generate random num between 1 to 100
# import random
# number = random.randint(1,100)
# print(number)

# fruits= ["apple","orange","pinapple"]
# fruits = random.choice(fruits)
# print(fruits)

# print the cureent date and time
# import datetime
# current = datetime.datetime.now()
# print(current)

# today = datetime.datetime.now()
# print(today.strftime("%d-%m-%y"))

#print the calender of a month entered by the user
# import calendar

# year = int(input("Enter year: "))
# month = int(input("Enter month(1-12): "))
# print(calendar.month(year,month))

# print the current working directory
# import os
# print("Current Directory:")
# print(os.getcwd())

# create a folder with a name entered by the user
import os
folder = input("Enter folder name: ")

if not os.path.exists(folder):
    os.mkdir(folder)
    print("Folder created successfully.")
    
else:
    print("Folder already exists.")