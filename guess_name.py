from random import randint

bot = randint(1, 10)

user = 0

while user != bot:
    user = int(input("Guess a number from 1 to 10:\n"))
    if user < bot:
        print('Too Low')
    elif user > bot:
        print('Too High')
    else:
        print(f'Lucky Guess, the number was {bot}')
