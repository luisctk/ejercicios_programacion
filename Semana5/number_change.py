list_to_change = [1,2,3,4,5,6,7,8,9,10]


change = list_to_change[0]
list_to_change[0] = list_to_change[-1]
list_to_change[-1] = change

print(list_to_change)