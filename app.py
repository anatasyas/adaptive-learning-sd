"""
app.py — Flask backend
Menghubungkan: ontologi + BKT engine + SQLite database
"""

import os
from flask import Flask, request, jsonify, send_from_directory, send_file, Response
import random, os, sys

sys.path.insert(0, os.path.dirname(__file__))

from ontology   import build_ontology, get_kc_info, get_available_kcs, get_ontology_informed_prior
from bkt_engine import (KCState, StudentModel, bkt_update, process_response,
                        select_next_kc, DEFAULT_BKT_PARAMS, KC_PARAM_OVERRIDES)
from database   import (init_db, create_student, get_student, add_stars, get_random_question,
                        upsert_kc_state, get_all_kc_states, get_mastered_kcs,
                        get_kc_state, log_interaction, get_interaction_count,
                        get_random_question)

import json
from pathlib import Path

app = Flask(__name__, static_folder="static", template_folder="static")
app.config["SECRET_KEY"] = "adaptive-learning-ipb-2025"

# ─── Boot ─────────────────────────────────────────────────────────────────────
BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
DATA_PATH  = os.path.join(BASE_DIR, "data", "math_grade1.json")
PARAM_PATH = os.path.join(BASE_DIR, "data", "estimated_params.json")

G = build_ontology(DATA_PATH)
init_db()

# Load estimated params jika ada
estimated_params = {}
if Path(PARAM_PATH).exists():
    with open(PARAM_PATH) as f:
        estimated_params = json.load(f).get("ontologi", {})



# ─── Helpers ──────────────────────────────────────────────────────────────────
def _rebuild_student_model(student_id: str) -> StudentModel:
    """Rebuild StudentModel dari DB state."""
    student = StudentModel(student_id=student_id)
    db_states = get_all_kc_states(student_id)

    for kc_id in G.nodes:
        params = dict(DEFAULT_BKT_PARAMS)
        if kc_id in KC_PARAM_OVERRIDES:
            params.update(KC_PARAM_OVERRIDES[kc_id])
        if kc_id in estimated_params:
            params.update(estimated_params[kc_id])

        if kc_id in db_states:
            s = db_states[kc_id]
            p_know = s["p_know"]
            n_correct = s["n_correct"]
            n_incorrect = s["n_incorrect"]
        else:
            p_know = get_ontology_informed_prior(G, kc_id)
            n_correct = n_incorrect = 0

        student.kc_states[kc_id] = KCState(
            kc_id=kc_id, p_know=p_know,
            p_transit=params["p_transit"], p_guess=params["p_guess"],
            p_slip=params["p_slip"], mastery_threshold=params["mastery_threshold"],
            n_correct=n_correct, n_incorrect=n_incorrect,
        )
    return student


def _sync_to_db(student: StudentModel):
    """Simpan semua KC state ke DB."""
    for kc_id, state in student.kc_states.items():
        upsert_kc_state(
            student.student_id, kc_id, state.p_know,
            state.n_correct, state.n_incorrect, state.is_mastered
        )


def _get_question(kc_id: str) -> dict:
    q = get_random_question(kc_id)
    if not q:
        # Fallback jika soal belum di-seed
        q = {"kc_id": kc_id, "q": "Pilih jawaban yang benar!",
             "options": ["A","B","C","D"], "answer": "A"}
    q["kc_name"] = get_kc_info(G, kc_id)["name"]
    return q


def _progress_summary(student_id: str) -> dict:
    db_states = get_all_kc_states(student_id)
    total = G.number_of_nodes()
    mastered = sum(1 for s in db_states.values() if s["is_mastered"])
    stars = get_student(student_id)["total_stars"] if get_student(student_id) else 0
    return {"mastered": mastered, "total": total, "stars": stars,
            "pct": round(mastered / total * 100)}


# ─── Routes ───────────────────────────────────────────────────────────────────
@app.route("/")
def index():
    # Coba serve dari static/ dulu, fallback ke inline
    static_path = os.path.join(os.path.dirname(__file__), "static", "index.html")
    if os.path.exists(static_path):
        return send_from_directory(
            os.path.join(os.path.dirname(__file__), "static"), "index.html"
        )
    # Fallback: baca dari file manapun yang ada
    for candidate in ["static/index.html", "index.html"]:
        if os.path.exists(candidate):
            with open(candidate, encoding="utf-8") as f:
                return f.read()
    return "index.html tidak ditemukan. Upload file static/index.html.", 404


@app.post("/api/register")
def register():
    data = request.json
    name   = data.get("name", "Siswa").strip() or "Siswa"
    avatar = int(data.get("avatar", 1))
    sid    = f"S{random.randint(10000,99999)}"

    if get_student(sid):
        return jsonify({"error": "ID collision"}), 500

    create_student(sid, name, avatar)

    # Inisialisasi semua KC state
    for kc_id in G.nodes:
        upsert_kc_state(sid, kc_id,
                        get_ontology_informed_prior(G, kc_id),
                        0, 0, False)

    return jsonify({"student_id": sid, "name": name})


@app.get("/api/student/<sid>")
def student_info(sid):
    s = get_student(sid)
    if not s:
        return jsonify({"error": "not found"}), 404
    progress = _progress_summary(sid)
    return jsonify({**s, **progress})


@app.get("/api/next-question/<sid>")
def next_question(sid):
    """Pilih KC berikutnya via adaptive engine, kembalikan soal."""
    student = _rebuild_student_model(sid)
    next_kc = select_next_kc(student, G)

    if next_kc is None:
        return jsonify({"done": True, "message": "Semua materi selesai! 🎉"})

    q = _get_question(next_kc)
    return jsonify({"done": False, **q})


@app.post("/api/answer/<sid>")
def answer(sid):
    """Proses jawaban siswa, update BKT state, simpan ke DB."""
    data    = request.json
    kc_id   = data["kc_id"]
    correct = bool(data["correct"])

    student = _rebuild_student_model(sid)
    result  = process_response(student, G, kc_id, correct)
    _sync_to_db(student)
    log_interaction(sid, kc_id, correct, result["p_before"], result["p_after"])

    # Beri bintang
    stars_earned = 0
    if correct:
        stars_earned = 2 if result["mastered"] else 1
        add_stars(sid, stars_earned)

    progress = _progress_summary(sid)

    return jsonify({
        "correct":      correct,
        "mastered":     result["mastered"],
        "p_know":       round(result["p_after"], 3),
        "propagated":   result["propagated"],
        "stars_earned": stars_earned,
        "progress":     progress,
    })


@app.get("/api/progress/<sid>")
def progress(sid):
    db_states = get_all_kc_states(sid)
    topics: dict[str, dict] = {}
    for kc_id, state in db_states.items():
        info  = get_kc_info(G, kc_id)
        topic = info["topic"]
        if topic not in topics:
            topics[topic] = {"mastered": 0, "total": 0}
        topics[topic]["total"] += 1
        if state["is_mastered"]:
            topics[topic]["mastered"] += 1
    summary = _progress_summary(sid)
    return jsonify({**summary, "topics": topics})



# ─── Admin Routes (untuk peneliti) ───────────────────────────────────────────
ADMIN_KEY = os.environ.get("ADMIN_KEY", "skripsi2025")  # ganti via env var

def _check_admin(req):
    return req.args.get("key") == ADMIN_KEY

@app.get("/admin/download-db")
def download_db():
    """Download SQLite DB langsung. Akses: /admin/download-db?key=ADMIN_KEY"""
    if not _check_admin(request):
        return jsonify({"error": "Unauthorized"}), 401
    from database import DB_PATH
    return send_file(DB_PATH, as_attachment=True,
                     download_name="adaptive_learning.db",
                     mimetype="application/octet-stream")

@app.get("/admin/export-csv")
def export_csv():
    """Export semua interaksi sebagai CSV. Akses: /admin/export-csv?key=ADMIN_KEY"""
    if not _check_admin(request):
        return jsonify({"error": "Unauthorized"}), 401

    from database import get_conn
    import csv, io
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["student_id","name","kc_id","correct","p_before","p_after","timestamp"])

    with get_conn() as conn:
        rows = conn.execute("""
            SELECT i.student_id, s.name, i.kc_id, i.correct,
                   i.p_before, i.p_after, i.timestamp
            FROM interactions i
            JOIN students s ON s.id = i.student_id
            ORDER BY i.student_id, i.timestamp
        """).fetchall()
    writer.writerows(rows)

    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=interactions.csv"}
    )

@app.get("/admin/stats")
def admin_stats():
    """Statistik cepat. Akses: /admin/stats?key=ADMIN_KEY"""
    if not _check_admin(request):
        return jsonify({"error": "Unauthorized"}), 401

    from database import get_conn
    with get_conn() as conn:
        n_students = conn.execute("SELECT COUNT(*) FROM students").fetchone()[0]
        n_inter    = conn.execute("SELECT COUNT(*) FROM interactions").fetchone()[0]
        n_mastered = conn.execute("SELECT COUNT(*) FROM kc_states WHERE is_mastered=1").fetchone()[0]
        acc        = conn.execute("SELECT AVG(correct) FROM interactions").fetchone()[0]
        students   = conn.execute("""
            SELECT s.name,
                   COUNT(i.id) as n_inter,
                   ROUND(AVG(i.correct)*100,1) as acc,
                   COUNT(DISTINCT CASE WHEN ks.is_mastered=1 THEN ks.kc_id END) as mastered
            FROM students s
            LEFT JOIN interactions i  ON i.student_id  = s.id
            LEFT JOIN kc_states    ks ON ks.student_id = s.id
            GROUP BY s.id ORDER BY s.created_at
        """).fetchall()

    return jsonify({
        "total_students":    n_students,
        "total_interactions": n_inter,
        "total_kc_mastered": n_mastered,
        "avg_accuracy_pct":  round((acc or 0) * 100, 1),
        "students": [dict(r) for r in students]
    })


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    # debug=False untuk production (Render/Replit)
    debug = os.environ.get("FLASK_ENV") == "development"
    app.run(host="0.0.0.0", port=port, debug=debug)
