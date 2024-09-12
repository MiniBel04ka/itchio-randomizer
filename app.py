from flask import Flask, render_template, jsonify
import requests
from bs4 import BeautifulSoup
import random

app = Flask(__name__)

def get_random_game():
    random_page = random.randint(1, 200)
    url = f'https://itch.io/games?page={random_page}'
    response = requests.get(url)
    
    if response.status_code != 200:
        return None
    
    soup = BeautifulSoup(response.text, 'html.parser')
    games = soup.find_all('div', class_='game_cell')
    
    if not games:
        return None
    
    random_game = random.choice(games)
    game_title = random_game.find('a', class_='title').text.strip()
    game_url = random_game.find('a', class_='title')['href']
    
    return game_title, game_url

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_game', methods=['GET'])
def get_game():
    game = get_random_game()
    if game:
        return jsonify({'title': game[0], 'url': f'{game[1]}'})
    else:
        return jsonify({'error': 'Couldn`t find the game'}), 500
    
if __name__ == '__main__':
    app.run(debug=True)

