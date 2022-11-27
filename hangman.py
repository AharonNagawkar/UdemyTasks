from random import choice

words_bank = ['Aharon', 'Seemi', 'Orna', 'Norin']
attempt = 3
chosen = choice(words_bank).lower()
guess_word = list('-'*len(chosen))

while (attempt > 0) and ('-' in guess_word):
    letter = input(f"You have {attempt} attempts:\n{' '.join(guess_word)}\nGuess a letter:\n")
    if letter in chosen:
        for i in range(len(chosen)):
            if letter.lower() == chosen[i]:
                guess_word[i] = letter
    else:
        attempt -= 1

if '-' not in guess_word:
    print(f"The word is {guess_word[0].upper()+''.join(guess_word[1:])}, you Won")
else:
    print(f"{attempt} attempt reached, you lost")
