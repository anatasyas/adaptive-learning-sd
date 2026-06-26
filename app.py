"""
app.py — Fixed Version
"""

import os
from flask import Flask, request, jsonify, send_from_directory, send_file, Response
import random
import sys
import json
from pathlib import Path

sys.path.insert(0, os.path.dirname(__file__))

from ontology import build_ontology, get_kc_info, get_ontology_informed_prior
from bkt_engine import (KCState, StudentModel, process_response, select_next_kc, 
                       DEFAULT_BKT_PARAMS, KC_PARAM_OVERRIDES)
from database import (
    init_db, seed_ontology, count_questions,
    create_student, get_student, add_stars, get_random_question,
    upsert_kc_state, get_all_kc_states, log_interaction
)

app = Flask(__name__, static_folder="static", template_folder="static")
app.config["SECRET_KEY"] = "adaptive-learning-ipb-2025"

# ====================== ROBUST BOOT ======================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "math_grade1.json")
PARAM_PATH = os.path.join(BASE_DIR, "data", "estimated_params.json")

print("🚀 Starting Adaptive Learning SD...")

init_db()

print("🔄 Seeding ontology...")
seed_ontology(DATA_PATH)

if count_questions() == 0:
    from seed_questions import seed
    seed()
    print("✅ Questions seeded")
else:
    print(f"✅ Questions already seeded ({count_questions()} soal)")

G = build_ontology(DATA_PATH)
print(f"✅ Ontology loaded: {G.number_of_nodes()} KC")

TOPIC_ORDER = ["bilangan", "operasi", "geometri", "pengukuran", "pola"]
TOPIC_LABELS = {
    "bilangan": "Bilangan", "operasi": "Operasi Bilangan",
    "geometri": "Geometri", "pengukuran": "Pengukuran",
    "pola": "Pola & Aljabar"
}
print(f"✅ Topics loaded: {len(TOPIC_ORDER)}")

# Load estimated params
estimated_params = {}
if Path(PARAM_PATH).exists():
    with open(PARAM_PATH) as f:
        estimated_params = json.load(f).get("ontologi", {})
print("✅ Boot completed!")
# ====================== END BOOT ======================

# Helpers & Routes tetap sama seperti kode kamu sebelumnya...
# (saya tidak copy semua agar tidak terlalu panjang, tapi kamu bisa merge)

@app.get("/api/topics/<sid>")
def get_topics(sid):
    db_states = get_all_kc_states(sid)
    topic_stats = {}
    for topic in TOPIC_ORDER:
        kcs_in_topic = [n for n, d in G.nodes(data=True) if d.get("topic") == topic]
        n_mastered = sum(1 for kc in kcs_in_topic if db_states.get(kc, {}).get("is_mastered", False))
        topic_stats[topic] = {
            "n_total": len(kcs_in_topic),
            "n_mastered": n_mastered,
            "completed": n_mastered == len(kcs_in_topic) and len(kcs_in_topic) > 0,
        }

    result = []
    for i, topic in enumerate(TOPIC_ORDER):
        s = topic_stats[topic]
        locked = i > 0 and topic_stats[TOPIC_ORDER[i-1]]["n_mastered"] == 0
        result.append({
            "id": topic,
            "label": TOPIC_LABELS.get(topic, topic),
            "n_mastered": s["n_mastered"],
            "n_total": s["n_total"],
            "completed": s["completed"],
            "locked": locked,
        })
    return jsonify(result)

# ... (sisanya route lain bisa kamu copy dari file lama)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_ENV") == "development"
    app.run(host="0.0.0.0", port=port, debug=debug)
