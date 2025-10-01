from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/")
def home():
    return "Welcome to the ESPN Box Score API!"

@app.route("/scores")
def scores():
    game_id = request.args.get("game_id")
    if not game_id:
        return jsonify({"error": "Missing game_id"}), 400

    url = f"https://www.espn.com/nfl/boxscore/_/gameId/{game_id}"
headers = {
    "User-Agent": "Mozilla/5.0"
}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')


    tables = soup.find_all('table', class_='Table')
    scores = {}
    for table in tables:
        rows = table.find_all('tr')
        for row in rows:
            cells = row.find_all('td')
            if len(cells) >= 5:
                team = cells[0].text.strip()
                scores[team] = {
                    "q1": cells[1].text.strip(),
                    "q2": cells[2].text.strip(),
                    "q3": cells[3].text.strip(),
                    "q4": cells[4].text.strip()
                }
        if scores:
            break

    return jsonify(scores)
