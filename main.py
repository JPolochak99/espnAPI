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

    table = soup.find('table', attrs={'data-testid': 'prism-Table'})
    if not table:
        return jsonify({"error": "Score table not found"}), 404

    rows = table.find_all('tr', attrs={'data-testid': 'prism-TableRow'})
    if len(rows) < 3:
        return jsonify({"error": "Insufficient score data"}), 500

    # Parse away team (first row)
    away_q1 = int(away_cells[1].text.strip())
    away_q2 = away_q1 + int(away_cells[2].text.strip())
    away_q3 = away_q2 + int(away_cells[3].text.strip())
    away_final = int(away_cells[5].text.strip())

    home_q1 = int(home_cells[1].text.strip())
    home_q2 = home_q1 + int(home_cells[2].text.strip())
    home_q3 = home_q2 + int(home_cells[3].text.strip())
    home_final = int(home_cells[5].text.strip())

    # Now take last digit
    return jsonify({
        "q1": f"{home_q1 % 10}{away_q1 % 10}",
        "q2": f"{home_q2 % 10}{away_q2 % 10}",
        "q3": f"{home_q3 % 10}{away_q3 % 10}",
        "final": f"{home_final % 10}{away_final % 10}"
})


