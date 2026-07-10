numbers = [2, 1, 4, 3, 79, 56, 77]

even_num = []
odd_num = []

for num in numbers:
    if num % 2 == 0:
        even_num.append(num)
    else:
        odd_num.append(num)

print("Even:", even_num)
print("Odd:", odd_num)