my_list = [4, 6, 2, 29]

def sum_list(numbers):
    total = 0
    for num in numbers:
        total += num
    return total

result = sum_list(my_list)
print(result)