numbers = []

for i in range(10):
    num = int(input("Enter a number: "))
    numbers.append(num)

highest_number = numbers[0]

for num in numbers:
    if num > highest_number:
        highest_number = num

print("Numbers entered:", numbers)
print("Highest number:", highest_number)
