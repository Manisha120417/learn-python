import json

# use json.dumps() to convert a python object into a JSON stirng.
# python dictionary to JSON
# student = {
#     "name":"Mansiha",
#     "age":20,
#     "course":"BCA"
# }

# json_string= json.dumps(student)
# print(json_string)
# print(type(json_string))

# json string to python dictionary

# json_string = '{"name": "Manisha", "age":20,"couse":"BCA"}'

# student = json.loads(json_string)
# print(student)
# print(type(student))
# print(student["name"])

# write JSON to a fle
# use json.dump() to save data to a  JSON file.add()
import json

student = {
    "name": "Manisha",
    "age": 22,
    "course": "BCA"
}

with open("student.json", "w") as file:
    json.dump(student, file, indent=4)

print("Data saved successfully.")