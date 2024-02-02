import requests
import re
import logging
import json
from bs4 import BeautifulSoup

# Initialize some variables
mode = int(input("Please select a mode (say q to quit): "))  # Get the mode
game_name = ''
games = []
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

# Define functions
def metacritic():
    # Get the webpage
    url = f"https://www.metacritic.com/game/{game_name}/"
    response = requests.get(url, headers=headers)
    html = response.text  # Get the source code of the webpage
    soup = BeautifulSoup(html, "html.parser")  # Parse the webpage
    scores = soup.find("span",{"data-v-4cdca868":True})  # Get all score elements
    if scores is not None:
        print(f"Metacritic total score: {scores.text}")  # Print the score
    else:
        print("No matching score found")

def ign():
    url = f"https://www.ign.com/games/{game_name}/"
    response = requests.get(url, headers=headers)
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    scores = soup.find("figcaption")
    if scores is not None:
        print(f"IGN score: {scores.text}")
    else:
        print("No matching score found")

def gamespot():
    url = f"https://www.gamespot.com/games/{game_name}/"
    response = requests.get(url, headers=headers)
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    # Find all <span> elements whose 'aria-label' attribute contains 'Review score'
    spans = soup.find('span', attrs={'aria-label': re.compile('Review score')})
    if spans is not None:
        print(f"GameSpot score: {spans.text}")  # Print the score
    else:
        print("No matching score found")

# Load the configuration file
with open("config.json", "r+") as f:
    config = json.load(f)
    is_first_time = config["first-time"]
    proxies = {
      'http': f'http://{config["proxy"]}',
      'https': f'https://{config["proxy"]}'
    }
if is_first_time:  # If it's the first time running the program
    print("First time running the program.Loading the ranking of games from Metacritic...")
    with open("ranking.txt","w")as f:
        rank = 1
        for i in range(1,11):
            url = f"https://www.metacritic.com/browse/game/?releaseYearMin=1958&releaseYearMax=2024&page={i}"
            response = requests.get(url, headers=headers)
            html = response.text
            soup = BeautifulSoup(html, "html.parser")

            # Find all <h3> elements
            h3_elements = soup.find_all("h3", {"class": "c-finderProductCard_titleHeading"})

            # Traverse each <h3> element
            for h3 in h3_elements:
                # Find all <span> elements on each <h3> element
                spans = h3.find_all("span")
                if len(spans) > 1:
                    f.write(f"{spans[1].text},")  # Print the text in the second <span> element
                    rank+=1
                    
with open("ranking.txt","r")as f:
        games = f.read().split(",")

config["first-time"] = False                    
with open("config.json","w")as f:  # Update the config file
    json.dump(config,f)

if mode == 1:
    while(game_name!='q'):
        game_name = input("Please enter the game name: ")
        game_name = game_name.lower()
        for i in game_name:
            if i == ' ':
                game_name = game_name.replace(i, "-")  # Replace spaces with hyphens to prevent errors
        ign()
        gamespot()
        metacritic()

elif mode == 2:
    for i in range(len(games)-1):
        print(f"{i+1}.{games[i]}")

elif mode == 3:
    while(game_name!='q'):
        game_name = input("Please enter the game name or ranking: ")
        if game_name.isdigit():
            print(f"The game name is {games[int(game_name) - 1]}")
        else:
            if game_name in games:
                print(f"The ranking is {games.index(game_name) + 1}")
            else:
                print("The game is not in the list")
