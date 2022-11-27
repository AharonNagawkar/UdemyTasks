'''

def titleize(long_string):
    string_list = long_string.split()
    print(' '.join([word[0].upper()+word[1:] for word in string_list]))


titleize('this is awesome') # "This Is Awesome"
titleize('oNLy cAPITALIZe fIRSt') # "ONLy CAPITALIZe FIRSt"
titleize('i have a dream')

'''

'''

def includes(*args):
    if type(args[0]) is str or type(args[0]) is list:
        if len(args) == 3:
            index = args[2]
            return args[1] in args[0][index:]
        return args[1] in args[0]
    elif type(args[0]) is dict:
        return args[1] in args[0].values()


print(includes([1, 2, 3], 1)) # True
print(includes([1, 2, 3], 1, 2)) # False
print(includes({ 'a': 1, 'b': 2 }, 1)) # True
print(includes({ 'a': 1, 'b': 2 }, 'a')) # False
print(includes('abcd', 'b')) # True
print(includes('abcd', 'e')) # False

'''

'''

def two_list_dictionary(keys_list, values_list):
    my_dict = {}
    min_length = min(len(keys_list),len(values_list))
    for i in range(0,min_length):
        my_dict[keys_list[i]] = values_list[i]
    if len(keys_list) > len(values_list):
        for i in range(min_length,len(keys_list)):
            my_dict[keys_list[i]] = None
    print(my_dict)


two_list_dictionary(['a', 'b', 'c', 'd'], [1, 2, 3]) # {'a': 1, 'b': 2, 'c': 3, 'd': None}
two_list_dictionary(['a', 'b', 'c']  , [1, 2, 3, 4]) # {'a': 1, 'b': 2, 'c': 3}
two_list_dictionary(['x', 'y', 'z']  , [1,2]) # {'x': 1, 'y': 2, 'z': None}
'''

'''

def range_in_list(num_list, *args):
    if len(args) == 2:
        min_index = args[0]
        max_index = min(args[1] + 1 , len(num_list))
    elif len(args) == 1:
        min_index =args[0]
        max_index = len(num_list)
    else:
        min_index = 0
        max_index = len(num_list)

    print(sum(num_list[min_index:max_index]))



range_in_list([1, 2, 3, 4], 0, 2)  # 6
range_in_list([1, 2, 3, 4], 0, 3)  # 10
range_in_list([1, 2, 3, 4], 1)  # 9
range_in_list([1, 2, 3, 4])  # 10
range_in_list([1, 2, 3, 4], 0, 100)  # 10
range_in_list([], 0, 1)  # 0

'''

'''

def sum_up_diagonals(my_list):
    diagonal_sum = 0
    for x in range(len(my_list)):
        diagonal_sum += my_list[x][x] + my_list[x][len(my_list)-x-1]
    print(diagonal_sum)


list1 = [
    [1, 2],
    [3, 4]
]

sum_up_diagonals(list1)  # 10

list2 = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

sum_up_diagonals(list2)  # 30

list3 = [
    [4, 1, 0],
    [-1, -1, 0],
    [0, 0, 9]
]

sum_up_diagonals(list3)  # 11

list4 = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12],
    [13, 14, 15, 16]
]

sum_up_diagonals(list4)  # 68

'''


'''

def reverse_vowels(my_string):
    indexes = []
    vowels = ''
    reverse = ''

    for i in range(len(my_string)):
        if my_string[i].lower() in 'aeiou':
            indexes.append(i)
            vowels += my_string[i]
    vowels = vowels[::-1]

    index = 0
    for j in range(len(my_string)):
        if j in indexes:
            reverse += vowels[index]
            index += 1
        else:
            reverse += my_string[j]
    return reverse



#reverse_vowels("Hello!") # "Holle!"
#reverse_vowels("Tomatoes") # "Temotaos"
reverse_vowels("Reverse Vowels In A String") # "RivArsI Vewols en e Streng"
#reverse_vowels("aeiou") # "uoiea"
#reverse_vowels("why try, shy fly?") # "why try, shy fly?"


'''

'''
def running_average():
    running_average.accumulator = 0
    running_average.size = 0

    def inner(number):
        running_average.accumulator += number
        running_average.size += 1
        return running_average.accumulator / running_average.size

    return inner

rAvg = running_average()
print(rAvg(10)) # 10.0
rAvg(11) # 10.5
rAvg(12) # 11

rAvg2 = running_average()
rAvg2(1) # 1
rAvg2(3) # 2
'''

'''
key = input('Hit \'q\' to quit the program or \'p]\' to say Hello')

while key != 'q':
    if key == 'p':
        print("Hello")
    key = input('Hit \'q\' to quit the program or \'p]\' to say Hello')

'''


import random

# This line creates a set with 6 random numbers
lottery_numbers = set(random.sample(range(22), 6))

# Here are your players; find out who has the most numbers matching lottery_numbers!
players = [
    {'name': 'Rolf', 'numbers': {1, 3, 5, 7, 9, 11}},
    {'name': 'Charlie', 'numbers': {2, 7, 9, 22, 10, 5}},
    {'name': 'Anna', 'numbers': {13, 14, 15, 16, 17, 18}},
    {'name': 'Jen', 'numbers': {19, 20, 12, 7, 3, 5}}
]

# Then, print out a line such as "Jen won 1000.".
# The winnings are calculated with the formula:
# 100 ** len(numbers_matched)

players_wins = [(player['name'], 100*len(player['numbers'].intersection(lottery_numbers))) for player in players]
print(players_wins)
win=0
for winner in players_wins:
    price=winner[1]
    if winner[1] > win:
        name = winner[0]
        win = price
print(f"{name} won {win}")