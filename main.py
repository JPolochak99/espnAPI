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

    # Find the specific table using data-testid
    table = soup.find('table', attrs={'data-testid': 'prism-Table'})
    if not table:
        return jsonify({"error": "Score table not found"}), 404

    scores = {}
    rows = table.find_all('tr', attrs={'data-testid': 'prism-TableRow'})
    for row in rows[1:]:  # skip header row
        cells = row.find_all('td', attrs={'data-testid': 'prism-TableCell'})
        if len(cells) >= 6:
            # Extract team name from the nested <a> tag
            team_tag = cells[0].find('a', attrs={'data-testid': 'prism-linkbase'})
            team_name = team_tag.text.strip() if team_tag else cells[0].text.strip()

            scores[team_name] = {
                "q1": cells[1].text.strip(),
                "q2": cells[2].text.strip(),
                "q3": cells[3].text.strip(),
                "q4": cells[4].text.strip(),
                "total": cells[5].text.strip()
            }

    return jsonify(scores)

