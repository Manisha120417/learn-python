# dictionary store data in key-value pairs

student = {
    "name": "sita",
    "age": 20,
    "course": "Python"
}

print(student)

#Accessing value
print(student["name"]) 
print(student["age"])

# Adding and updating values
student["age"] = 21
student["city"]="Brt"

# deleting values
del student["age"]
print(student)

