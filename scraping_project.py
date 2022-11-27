'''
1.  Create a file called `scraping_project.py` which, when run,
    grabs data on every quote from the website http://quotes.toscrape.com

2.  You can use `bs4` and `requests` to get the data. For each quote you should grab the text of the quote,
    the name of the person who said the quote, and the href of the link to the person's bio.
    Store all of this information in a list.

3.  Next, display the quote to the user and ask who said it. The player will have four guesses remaining.

4.  After each incorrect guess, the number of guesses remaining will decrement.
    If the player gets to zero guesses without identifying the author, the player loses and the game ends.
    If the player correctly identifies the author, the player wins!

5. After every incorrect guess, the player receives a hint about the author.
    a. For the first hint, make another request to the author's bio page (this is why we originally scrape this data),
    and tell the player the author's birth date and location.
    b. The next two hints are up to you! Some ideas: the first letter of the author's first name,
    the first letter of the author's last name, the number of letters in one of the names, etc.

6.  When the game is over, ask the player if they want to play again.
    If yes, restart the game with a new quote. If no, the program is complete.
'''

# https://quotes.toscrape.com

import requests
from bs4 import BeautifulSoup
from time import sleep
from random import choice
from csv import DictWriter,DictReader
from csv import writer

base_url = 'http://quotes.toscrape.com'

def scrape_quotes():
    all_quotes = []
    url = '/page/1'

    while url:

        res = requests.get(base_url + url)
        res.encoding = 'UTF-8'
        print('Now scraping page {}'.format(base_url + url))
        soup = BeautifulSoup(res.text, 'html.parser')
        quotes = soup.find_all(class_='quote')

        for quote in quotes:
            all_quotes.append({
                "text": quote.find(class_='text').text,
                "author": quote.find(class_='author').text,
                "bio_link": quote.find('a')['href']
            })
            next_btn = soup.find(class_='next')
            url = next_btn.find('a')['href'] if next_btn else None
            sleep(1)
    return all_quotes



def start_game(all_quotes):
    quote = choice(all_quotes)
    remaining_guesses = 4
    print("Here's the quote:")
    print(quote['text'])
    print('FOR TESTING: ' + quote['author'])
    guess = ''
    while guess.lower() != quote["author"].lower() and remaining_guesses > 0:
        guess = input("Who said this quote? you have {} guesses left \n".format(remaining_guesses))
        if guess.lower() == quote["author"].lower():
            print('You got it right')
            break
        remaining_guesses -= 1
        if remaining_guesses == 3:
            res = requests.get(base_url + quote['bio_link'])
            soup = BeautifulSoup(res.text, 'html.parser')
            birth_date = soup.find(class_='author-born-date').text
            birth_place = soup.find(class_='author-born-location').text
            print("Here's a hint: " + "The Author was born on: " + birth_date + " " + birth_place)
        elif remaining_guesses == 2:
            print("The Author First name starts with: " + quote['author'][0])
        elif remaining_guesses == 1:
            print("The author last name starts with:" + quote['author'].split(" ")[1][0])
        else:
            print(f"Sorry, you are out of guesses, the answer was {quote['author']}")

#Write to CSV
def write_csv(list_of_quotes):
    with open('quotes.csv', 'w', encoding='UTF-8') as file:
        headers = ['text', 'author', 'bio_link']
        csv_writer = DictWriter(file, fieldnames=headers)
        csv_writer.writeheader()
        for object in list_of_quotes:
            csv_writer.writerow(object)

def read_csv():
    with open('quotes.csv','r',encoding='UTF-8') as file:
        csv_reader = DictReader(file)
        return list(csv_reader)


#list_of_quotes = scrape_quotes()
#write_csv(list_of_quotes)
all_quotes = read_csv()



start_game(all_quotes)

stop = 0
while stop != 1:
    again = input("Would you like to play again? (y/n) \n")
    if again.lower() in ('yes', 'y'):
        start_game(all_quotes)
    elif again.lower() in ('no', 'n'):
        print("Thanks for playing")
        stop = 1
