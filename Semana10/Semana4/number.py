number_1 = int(input('Dame un numero'))
number_2 = int(input('Dame un numero otro'))
number_3 = int(input('Dame un numero un ultimo'))

if ((number_1 > number_2) and (number_1 > number_3)):
    print(f'{number_1} es mayor')
elif((number_2 > number_1) and (number_2 > number_3)):
    print(f'{number_2} es mayor')
elif((number_3 > number_1) and (number_3 > number_2)):
    print(f'{number_3} es mayor')