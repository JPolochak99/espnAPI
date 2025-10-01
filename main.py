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
    away_cells = rows[1].find_all('td', attrs={'data-testid': 'prism-TableCell'})
    away_q1 = int(away_cells[1].text.strip())% 10
    away_q2 = away_q1 + int(away_cells[2].text.strip())% 10
    away_q3 = away_q2 + int(away_cells[3].text.strip())% 10
    away_final = int(away_cells[5].text.strip())% 10

    # Parse home team (second row)
    home_cells = rows[2].find_all('td', attrs={'data-testid': 'prism-TableCell'})
    home_q1 = int(home_cells[1].text.strip()) % 10
    home_q2 = home_q1 + int(home_cells[2].text.strip()) % 10
    home_q3 = home_q2 + int(home_cells[3].text.strip()) % 10
    home_final = int(home_cells[5].text.strip()) % 10

    # Return flat structure for JS
    return jsonify({
        "q1": f"{home_q1}{away_q1}",
        "q2": f"{home_q2}{away_q2}",
        "q3": f"{home_q3}{away_q3}",
        "final": f"{home_final}{away_final}"
    })


