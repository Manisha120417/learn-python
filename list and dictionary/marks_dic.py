marks = {
    "Math":90,
    "Science":85,
    "English": 88
}

highest_subject = max(marks, key = marks.get)
lowest_suject = min(marks, key=marks.get)

average = sum(marks.values())/len(marks)

print("Highest Mark:")
print(highest_subject, "=",marks[highest_subject])

print("\nLowest Mark:")
print(lowest_suject, "=",marks[lowest_suject])

print("\nAverage Mark:", round(average,2))
