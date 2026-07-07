# for i in range(10):
#     print(i)

# name = input("Enter your name: ")

# for i in range(5):
#     print(name)


# print even number from 1 to 20
# for i in range(2,21,2):
#     print(i)
    
# print odd number from 1 to 20
# for i in range(1,21,2):
#    print(i)

# print the multiplication tables of a number entered by the user.

# num = int(input("Enter a number: "))

# for i in range(1,11):
#     print(num, "x", i,"=", num*i)

# 7. print the square of numbers from 1 to 10
# for i in range(1,10):
#     square=i**2
#     print(f"The square of {i} is {square}")
   
   
# for i in range(1,10):
#     cube= i**3
#     print(f"The cube of {i} is {cube}")


# 9. sum of first n natural number
# num = int(input("Enter the number:"))
# total_sum = 0
# for i in range(1, num + 1):
#      total_sum += i
#      print(f"The sum of first {num} natural numbers is {total_sum}")

#10. find the sum of all even numbers from 1 to n
num = int(input("Enter the number: " ))
sum = 0
for i in range(2, num+1, 2):
    sum += i
    print("Sum of even numbers =", sum)