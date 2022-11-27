from random import randint

EASY_LEVEL_TURNS = 5
HARD_LEVEL_TURNS = 10


def user_guess(tryout):
    return int(input(f"You have {tryout} attempts remaining to guess the number.\nMake a guess: "))


def difficulty_level(choice):
    if choice == 'easy':
        return EASY_LEVEL_TURNS
    elif choice == 'hard':
        return HARD_LEVEL_TURNS
    else:
        print('Wrong choice, play again')


def proximity(cpu, user):
    if user > cpu:
        return "Too high"
    return "Too low"


def game():
    difficulty = input("""
    Welcome to the Number Guessing Game!
    I'm thinking of a number between 1 and 100.
    Choose a difficulty. Type 'easy' or 'hard':""")

    number_to_guess = randint(1, 100)
    attempts = difficulty_level(difficulty)

    while attempts:
        guess = user_guess(attempts)
        if guess == number_to_guess:
            print("Way to go! you guessed Right")
            break
        else:
            attempts -= 1
            print(proximity(number_to_guess, guess))

    if attempts == 0:
        print("You've failed to guess the number.")


game()
