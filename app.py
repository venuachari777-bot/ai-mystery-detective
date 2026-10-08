import os
import time
from flask import Flask, render_template, jsonify, request, session
from dotenv import load_dotenv
from google import genai
from game_data import LEVELS
import database

# Environment variables load cheyadam
load_dotenv()

# SQLite Database tables ni initialize cheyadam
database.init_db()

app = Flask(__name__)
app.secret_key = "mystery_detective_stress_meter_v4"

# Gemini client initialization
api_key = os.getenv("GEMINI_API_KEY")
client = None
if api_key:
    client = genai.Client(api_key=api_key)

def calculate_stress(suspect_id, question, is_culprit, current_stress):
    q = question.lower()
    clue_keywords = [
        "shoe", "footprint", "fabric", "dress", "silk", "camera", "door", "lock",
        "usb", "badge", "8809", "coffee", "latte", "hazelnut", "wine", "poison",
        "almond", "receipt", "pin", "4412", "cyanide", "stole", "kill", "murder"
    ]
    
    hits = sum(1 for kw in clue_keywords if kw in q)
    
    if is_culprit:
        # Culprit evidence dorkithe tension baga peruguthundi
        added = 15 + (hits * 18)
        new_stress = min(95, current_stress + added)
    else:
        # Innocent suspects ki stress max 40% daggara restrict avthundi
        added = 5 + (hits * 6)
        new_stress = min(40, current_stress + added)
        
    return new_stress

@app.route('/')
def home():
    stats = database.get_stats()
    if 'current_level' not in session:
        session['current_level'] = stats['level']
        session['inventory'] = []
        session['stress_levels'] = {}

    lvl_num = session.get('current_level', stats['level'])
    current_level_data = LEVELS.get(lvl_num, LEVELS[1])
    return render_template('index.html', level=current_level_data, level_num=lvl_num, stats=stats)

@app.route('/api/collect-clue', methods=['POST'])
def collect_clue():
    clue_id = request.json.get('clue_id')
    lvl_num = session.get('current_level', 1)
    current_level_data = LEVELS.get(lvl_num, LEVELS[1])

    if 'inventory' not in session:
        session['inventory'] = []

    inventory = session['inventory']
    for clue in current_level_data['clues']:
        if clue['id'] == clue_id and not any(item['id'] == clue_id for item in inventory):
            inventory.append(clue)
            session['inventory'] = inventory
            session.modified = True
            database.log_clue(lvl_num, clue['id'], clue['name'])
            return jsonify({"status": "success", "inventory": inventory})

    return jsonify({"status": "already_collected", "inventory": inventory})

def get_fallback_suspect_response(suspect, question):
    q = question.lower()
    name = suspect['name'].lower()
    
    if "where" in q or "time" in q:
        if "vikram" in name:
            return "I swear I was at my guard post, detective! I only took a brief breather because of the exhausting night shift."
        elif "anita" in name:
            return "I was cataloging the gallery inventory until late, detective. Everything was locked up when I checked."
        elif "rahul" in name:
            return "I was finishing the hallway sweep on the ground floor. Why are you questioning me when I'm just doing my job?"
        elif "marcus" in name:
            return "I was handling regular server maintenance from the terminal. Tech issues don't sleep, you know."
        elif "elena" in name:
            return "I left the laboratory earlier in the evening after securing my research drafts."
        elif "priya" in name:
            return "I was at the study nook preparing for my upcoming certification exam all evening."
        elif "rohan" in name:
            return "I was attending to Mr. Singhania's dinner service in the penthouse dining hall around that time."
        elif "meera" in name:
            return "I was on duty at City Hospital performing an emergency surgery until late night."
        elif "arjun" in name:
            return "I had a brief business dispute with Singhania, but I walked out of the main lobby before 9:30 PM."
            
    if "wear" in q or "shoe" in q or "fabric" in q:
        if "anita" in name:
            return "I attended the evening art gala, so I was dressed formally in an elegant black silk evening dress."
        elif "rahul" in name:
            return "Just my standard issue cleaning overalls and my lightweight size 7 sneakers. Comfortable for walking."
        elif "vikram" in name:
            return "Standard security uniform and heavy boots, as always on duty."

    if "coffee" in q or "drink" in q or "wine" in q or "poison" in q or "receipt" in q or "pin" in q:
        if "marcus" in name:
            return "Yeah, I usually grab a sweet hazelnut latte to stay awake during long code deployments."
        elif "elena" in name:
            return "I cannot stand coffee, detective. It upsets my stomach completely."
        elif "priya" in name:
            return "I only drink herbal green tea to focus while studying."
        elif "rohan" in name:
            return "I poured the master his vintage wine at 10:10 PM using my service key PIN. I know nothing about poison!"
        elif "arjun" in name:
            return "I don't drink wine, only single malt whisky, and I left well before 10 PM."

    return "I've told you what I know about this case, detective. Check the facts yourself."

@app.route('/api/interrogate', methods=['POST'])
def interrogate():
    data = request.json or {}
    suspect_id = data.get('suspect_id')
    player_question = data.get('question', '').strip()

    lvl_num = session.get('current_level', 1)
    current_level_data = LEVELS.get(lvl_num, LEVELS[1])
    suspect = current_level_data['suspects'].get(suspect_id)

    if not suspect:
        return jsonify({"reply": "Suspect not found."})

    # Suspect stress tracking logic
    if 'stress_levels' not in session:
        session['stress_levels'] = {}
    
    current_stress = session['stress_levels'].get(suspect_id, 15)
    is_culprit = (suspect_id == current_level_data['culprit'])
    new_stress = calculate_stress(suspect_id, player_question, is_culprit, current_stress)
    session['stress_levels'][suspect_id] = new_stress
    session.modified = True

    inventory = session.get('inventory', [])
    clues_text = ", ".join([f"{c['name']} ({c['desc']})" for c in inventory]) or "None yet"

    prompt = f"""
    You are roleplaying as a suspect in a mystery detective game.
    Current Case: {current_level_data['title']}
    Name: {suspect['name']}
    Role: {suspect['role']}
    Personality: {suspect['personality']}
    Hidden Secret: {suspect['secret']}
    Clues collected by detective: {clues_text}
    Current Stress/Suspicion Level: {new_stress}%

    Instructions:
    - Respond strictly in English.
    - Stay 100% in-character.
    - If Stress > 70%, show noticeable nervousness, hesitation, or stutter in your dialogue.
    - Keep answers concise (1-2 sentences maximum).
    - If innocent, defend yourself naturally.
    - If culprit, deflect without directly confessing unless directly caught with clear evidence.

    Detective asks: "{player_question}"
    """

    candidate_models = ["gemini-3.8-flash", "gemini-2.0-flash", "gemini-1.5-flash"]
    reply = None

    if client:
        for model_name in candidate_models:
            for _ in range(2):
                try:
                    response = client.models.generate_content(
                        model=model_name,
                        contents=prompt,
                    )
                    if response and response.text:
                        reply = response.text.strip()
                        break
                except Exception as e:
                    if "503" in str(e):
                        time.sleep(1)
                        continue
                    else:
                        break
            if reply:
                break

    if not reply:
        reply = get_fallback_suspect_response(suspect, player_question)

    return jsonify({"reply": reply, "stress": new_stress, "suspect_id": suspect_id})

@app.route('/api/accuse', methods=['POST'])
def accuse():
    accused_suspect = request.json.get('suspect_id')
    lvl_num = session.get('current_level', 1)
    current_level_data = LEVELS.get(lvl_num, LEVELS[1])

    if accused_suspect == current_level_data['culprit']:
        next_lvl = current_level_data.get('next_level')
        
        # SQLite Database lo stats update cheyadam
        database.update_score_on_solve(next_lvl if next_lvl else lvl_num)
        
        culprit_data = current_level_data['suspects'][accused_suspect]
        confession = f"🚨 Culprit Caught: {culprit_data['name']}\n\n🕵️ Case Breakdown & Secret:\n{culprit_data['secret']}"
        
        if next_lvl:
            return jsonify({
                "result": "correct",
                "has_next": True,
                "message": f"{confession}\n\n⭐ +100 PTS Added! Case {lvl_num} Solved successfully. Ready for Level {next_lvl}?"
            })
        else:
            return jsonify({
                "result": "correct",
                "has_next": False,
                "message": f"{confession}\n\n🏆 Congratulations! You have successfully cracked all 3 cases, Master Detective!"
            })
    else:
        return jsonify({
            "result": "wrong",
            "has_next": False,
            "message": "❌ Wrong Accusation!\n\nYou accused an innocent person without sufficient evidence. The real culprit has escaped into the night!"
        })

@app.route('/api/next-level', methods=['POST'])
def next_level():
    lvl_num = session.get('current_level', 1)
    current_level_data = LEVELS.get(lvl_num, LEVELS[1])
    next_lvl = current_level_data.get('next_level')

    if next_lvl:
        session['current_level'] = next_lvl
        session['inventory'] = []
        session['stress_levels'] = {}
        session.modified = True
        return jsonify({"status": "ok"})
    return jsonify({"status": "no_more_levels"})

@app.route('/api/restart', methods=['POST'])
def restart():
    database.reset_db_progress()
    session['current_level'] = 1
    session['inventory'] = []
    session['stress_levels'] = {}
    session.modified = True
    return jsonify({"status": "restarted"})

if __name__ == '__main__':
    app.run(debug=True)