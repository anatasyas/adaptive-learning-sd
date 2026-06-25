"""
app.py — Flask backend
Adaptive Learning SD - BKT + Ontologi
"""

import os
from flask import Flask, request, jsonify, send_from_directory, send_file, Response
import random
import sys

sys.path.insert(0, os.path.dirname(__file__))

# Import semua modul
from ontology import build_ontology
from bkt_engine import StudentModel
from database import (
    init_db, seed_ontology, count_questions,
    create_student, get_student, add_stars,
    get_random_question, upsert_kc_state, get_all_kc_states,
    get_mastered_kcs, get_kc_state, log_interaction,
    get_interaction_count
)
from seed_questions import seed

app = Flask(__name__, static_folder="static", template_folder="static")
app.config["SECRET_KEY"] = "adaptive-learning-ipb-2025"

# ====================== BOOT SEQUENCE ======================
print("🚀 Starting Adaptive Learning SD...")

BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
DATA_PATH  = os.path.join(BASE_DIR, "data", "math_grade1.json")
PARAM_PATH = os.path.join(BASE_DIR, "data", "estimated_params.json")

# 1. Init Database
init_db()

# 2. Seeding
print("🔄 Running seeding...")
seed_ontology(DATA_PATH)

if count_questions() == 0:
    seed()
    print("✅ Questions seeded successfully")
else:
    print(f"✅ Questions already exist ({count_questions()} soal)")

# 3. Load Ontology
G = build_ontology(DATA_PATH)
print(f"✅ Ontology loaded successfully: {G.number_of_nodes()} KC nodes")

# 4. Topic definitions (dipindah ke atas)
TOPIC_ORDER  = ["bilangan", "operasi", "geometri", "pengukuran", "pola"]
TOPIC_LABELS = {
    "bilangan":   "Bilangan",
    "operasi":    "Operasi Bilangan",
    "geometri":   "Geometri",
    "pengukuran": "Pengukuran",
    "pola":       "Pola & Aljabar",
}
print(f"✅ Topics ready: {len(TOPIC_ORDER)} topik")
print("🚀 App boot completed successfully!\n")
# ====================== END BOOT ======================

# Load estimated params jika ada
estimated_params = {}
if os.path.exists(PARAM_PATH):
    import json
    with open(PARAM_PATH) as f:
        estimated_params = json.load(f).get("ontologi", {})


# ─── Helpers ──────────────────────────────────────────────────────────────────
def _rebuild_student_model(student_id: str) -> StudentModel:
    student = StudentModel(student_id=student_id)
    db_states = get_all_kc_states(student_id)

    for kc_id in G.nodes:
        params = {"p_transit": 0.10, "p_guess": 0.25, "p_slip": 0.10, "mastery_threshold": 0.80}
        if kc_id in estimated_params:
            params.update(estimated_params[kc_id])

        if kc_id in db_states:
            s = db_states[kc_id]
            p_know = s["p_know"]
            n_correct = s["n_correct"]
            n_incorrect = s["n_incorrect"]
        else:
            from ontology import get_ontology_informed_prior
            p_know = get_ontology_informed_prior(G, kc_id)
            n_correct = n_incorrect = 0

        student.kc_states[kc_id] = bkt_engine.KCState(
            kc_id=kc_id, p_know=p_know,
            p_transit=params["p_transit"], p_guess=params["p_guess"],
            p_slip=params["p_slip"], mastery_threshold=params["mastery_threshold"],
            n_correct=n_correct, n_incorrect=n_incorrect,
        )
    return student


def _sync_to_db(student: StudentModel):
    for kc_id, state in student.kc_states.items():
        upsert_kc_state(
            student.student_id, kc_id, state.p_know,
            state.n_correct, state.n_incorrect, state.is_mastered
        )


def _get_question(kc_id: str) -> dict:
    q = get_random_question(kc_id)
    if not q:
        q = {"kc_id": kc_id, "q": "Pilih jawaban yang benar!", 
             "options": ["A","B","C","D"], "answer": "A"}
    from ontology import get_kc_info
    q["kc_name"] = get_kc_info(G, kc_id)["name"]
    return q


def _progress_summary(student_id: str) -> dict:
    db_states = get_all_kc_states(student_id)
    total = G.number_of_nodes()
    mastered = sum(1 for s in db_states.values() if s.get("is_mastered", False))
    student = get_student(student_id)
    stars = student["total_stars"] if student else 0
    return {"mastered": mastered, "total": total, "stars": stars,
            "pct": round(mastered / total * 100) if total > 0 else 0}


# ─── Routes ───────────────────────────────────────────────────────────────────
@app.route("/")
def index():
    return send_from_directory("static", "index.html")


@app.post("/api/register")
def register():
    data = request.json
    name = data.get("name", "Siswa").strip() or "Siswa"
    avatar = int(data.get("avatar", 1))
    sid = f"S{random.randint(10000,99999)}"

    if get_student(sid):
        return jsonify({"error": "ID collision"}), 500

    create_student(sid, name, avatar)

    # Inisialisasi KC state
    from ontology import get_ontology_informed_prior
    for kc_id in G.nodes:
        upsert_kc_state(sid, kc_id, get_ontology_informed_prior(G, kc_id), 0, 0, False)

    return jsonify({"student_id": sid, "name": name})


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
        locked = False
        if i > 0:
            prev = TOPIC_ORDER[i-1]
            locked = topic_stats[prev]["n_mastered"] == 0

        result.append({
            "id": topic,
            "label": TOPIC_LABELS.get(topic, topic),
            "n_mastered": s["n_mastered"],
            "n_total": s["n_total"],
            "completed": s["completed"],
            "locked": locked,
        })

    return jsonify(result)


# Route lainnya tetap sama (next-question, answer, dll)
# ... (saya singkat karena panjang, tapi kamu bisa copy dari file lama kamu)

@app.get("/api/next-question/<sid>")
def next_question(sid):
    student = _rebuild_student_model(sid)
    from bkt_engine import select_next_kc
    next_kc = select_next_kc(student, G)

    if next_kc is None:
        return jsonify({"done": True, "message": "Semua materi selesai! 🎉"})

    q = _get_question(next_kc)
    return jsonify({"done": False, **q})


@app.post("/api/answer/<sid>")
def answer(sid):
    data = request.json
    kc_id = data["kc_id"]
    correct = bool(data["correct"])

    student = _rebuild_student_model(sid)
    from bkt_engine import process_response
    result = process_response(student, G, kc_id, correct)
    _sync_to_db(student)
    log_interaction(sid, kc_id, correct, result["p_before"], result["p_after"])

    stars_earned = 0
    if correct:
        stars_earned = 2 if result["mastered"] else 1
        add_stars(sid, stars_earned)

    progress = _progress_summary(sid)

    return jsonify({
        "correct": correct,
        "mastered": result["mastered"],
        "p_know": round(result["p_after"], 3),
        "stars_earned": stars_earned,
        "progress": progress,
    })


# Admin routes (tetap sama)
ADMIN_KEY = os.environ.get("ADMIN_KEY", "skripsi2025")

@app.get("/admin/download-db")
def download_db():
    if request.args.get("key") != ADMIN_KEY:
        return jsonify({"error": "Unauthorized"}), 401
    from database import DB_PATH
    return send_file(DB_PATH, as_attachment=True, download_name="adaptive_learning.db")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_ENV") == "development"
    app.run(host="0.0.0.0", port=port, debug=debug)
