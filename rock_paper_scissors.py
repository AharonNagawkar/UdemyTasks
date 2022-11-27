import sys
from random import choice, randint

bot = choice(['rock', 'paper', 'scissors'])

player = input('Choose your move: \n 1 - rock \n 2 - paper \n 3 - scissors \n')

while player not in ['1', '2', '3']:
    print('You have to select a number between 1 to 3')
    player = input('Choose your move: \n 1 - rock \n 2 - paper \n 3 - scissors \n ')
else:
    player = int(player)
    print('\nLet\'s play')
    if player == 1:
        player_choice = 'rock'
    elif player == 2:
        player_choice = 'paper'
    else:
        player_choice = 'scissors'

print('\nYou selected: {}\nThe Computer selected: {}'.format(player_choice, bot))

if bot == player_choice:
    print("It's a Tie")
elif (bot == 'rock' and player_choice == 'scissors') or (bot == 'paper' and player_choice == 'rock') or (bot == 'scissors' and player_choice == 'paper'):
    print('Computer Wins')
else:
    print('You Win')