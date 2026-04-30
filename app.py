"""
app.py — Flask backend
BKT + Ontologi Adaptive Learning
"""

import os, sys, json, random
from pathlib import Path
from flask import Flask, request, jsonify, send_from_directory, send_file, Response

BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
DATA_PATH  = os.path.join(BASE_DIR, "data", "math_grade1.json")
PARAM_PATH = os.path.join(BASE_DIR, "data", "estimated_params.json")
STATIC_DIR = os.path.join(BASE_DIR, "static")

sys.path.insert(0, BASE_DIR)

from ontology import (
    build_ontology, get_kc_info,
    get_available_kcs, get_ontology_informed_prior, get_prerequisites,
)
from bkt_engine import (
    KCState, StudentModel,
    process_response, select_next_kc,
    DEFAULT_BKT_PARAMS, KC_PARAM_OVERRIDES,
)
from database import (
    init_db, create_student, get_student, add_stars,
    get_random_question, upsert_kc_state, get_all_kc_states,
    log_interaction, get_conn, count_questions, DB_PATH,
)

# ── Boot ──────────────────────────────────────────────────────────────────────
app = Flask(__name__, static_folder=STATIC_DIR)
app.config["SECRET_KEY"] = "adaptive-learning-ipb-2025"

G = build_ontology(DATA_PATH)
init_db()

# Seed soal jika belum ada
if count_questions() == 0:
    try:
        exec(open(os.path.join(BASE_DIR, "seed_questions.py")).read())
    except Exception as e:
        print(f"[WARN] seed_questions failed: {e}")

# Load estimated params (opsional)
estimated_params: dict = {}
if Path(PARAM_PATH).exists():
    try:
        with open(PARAM_PATH) as f:
            estimated_params = json.load(f).get("ontologi", {})
        print(f"Loaded estimated_params for {len(estimated_params)} KCs")
    except Exception as e:
        print(f"[WARN] Could not load estimated_params: {e}")


# ── Helpers ───────────────────────────────────────────────────────────────────
def _get_params(kc_id: str) -> dict:
    """Ambil parameter BKT untuk KC tertentu."""
    params = dict(DEFAULT_BKT_PARAMS)
    if kc_id in KC_PARAM_OVERRIDES:
        params.update(KC_PARAM_OVERRIDES[kc_id])
    ep = estimated_params.get(kc_id, {})
    for key in ("p_transit", "p_guess", "p_slip"):
        if key in ep:
            params[key] = float(ep[key])
    return params


def _rebuild_student_model(student_id: str) -> StudentModel:
    student   = StudentModel(student_id=student_id)
    db_states = get_all_kc_states(student_id)

    for kc_id in G.nodes:
        params = _get_params(kc_id)
        db     = db_states.get(kc_id)

        student.kc_states[kc_id] = KCState(
            kc_id             = kc_id,
            p_know            = float(db["p_know"]) if db else get_ontology_informed_prior(G, kc_id),
            p_transit         = float(params["p_transit"]),
            p_guess           = float(params["p_guess"]),
            p_slip            = float(params["p_slip"]),
            mastery_threshold = float(params["mastery_threshold"]),
            n_correct         = int(db["n_correct"])   if db else 0,
            n_incorrect       = int(db["n_incorrect"]) if db else 0,
        )
    return student


def _sync_to_db(student: StudentModel):
    for kc_id, state in student.kc_states.items():
        upsert_kc_state(
            student.student_id, kc_id, state.p_know,
            state.n_correct, state.n_incorrect, state.is_mastered
        )


def _get_question(kc_id: str) -> dict:
    q       = get_random_question(kc_id)
    kc_name = get_kc_info(G, kc_id).get("name", kc_id)
    if not q:
        return {"kc_id": kc_id, "kc_name": kc_name,
                "q": f"Soal untuk {kc_name} belum tersedia.",
                "options": ["A", "B", "C", "D"], "answer": "A"}
    return {**q, "kc_name": kc_name}


def _progress_summary(student_id: str) -> dict:
    db_states = get_all_kc_states(student_id)
    total     = G.number_of_nodes()
    mastered  = sum(1 for s in db_states.values() if s["is_mastered"])
    stars     = (get_student(student_id) or {}).get("total_stars", 0)
    return {
        "mastered": mastered,
        "total":    total,
        "stars":    stars,
        "pct":      round(mastered / total * 100) if total else 0,
    }


# ── Routes ────────────────────────────────────────────────────────────────────

@app.get("/api/topics/<sid>")
def topics(sid):
    """Status semua topik untuk siswa — untuk topic selection screen."""
    try:
        db_states = get_all_kc_states(sid)
        mastered  = {kc for kc, s in db_states.items() if s["is_mastered"]}
        available = set(get_available_kcs(G, mastered))

        topic_meta = G.graph.get("topics", {})
        result = []

        for topic_id, meta in topic_meta.items():
            kcs_in_topic = [
                n for n, d in G.nodes(data=True) if d.get("topic") == topic_id
            ]
            n_total    = len(kcs_in_topic)
            n_mastered = sum(1 for k in kcs_in_topic if k in mastered)
            n_available = sum(1 for k in kcs_in_topic if k in available)
            locked     = n_available == 0 and n_mastered < n_total
            completed  = n_mastered == n_total

            result.append({
                "id":         topic_id,
                "label":      meta.get("label", topic_id),
                "nctm":       meta.get("nctm", ""),
                "n_total":    n_total,
                "n_mastered": n_mastered,
                "locked":     locked,
                "completed":  completed,
            })

        return jsonify(result)
    except Exception as e:
        import traceback; traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route("/")
def index():
    for candidate in [
        os.path.join(STATIC_DIR, "index.html"),
        os.path.join(BASE_DIR, "index.html"),
    ]:
        if os.path.exists(candidate):
            with open(candidate, encoding="utf-8") as f:
                return f.read()
    return "index.html tidak ditemukan.", 404


@app.get("/debug")
def debug():
    return jsonify({
        "db_path":        DB_PATH,
        "db_exists":      os.path.exists(DB_PATH),
        "data_exists":    os.path.exists(DATA_PATH),
        "n_questions":    count_questions(),
        "ontology_nodes": G.number_of_nodes(),
        "estimated_kcs":  len(estimated_params),
        "static_dir":     STATIC_DIR,
        "index_exists":   os.path.exists(os.path.join(STATIC_DIR, "index.html")),
    })


@app.post("/api/register")
def register():
    try:
        data   = request.json or {}
        name   = (data.get("name") or "Siswa").strip() or "Siswa"
        avatar = int(data.get("avatar", 1))
        sid    = f"S{random.randint(10000, 99999)}"

        create_student(sid, name, avatar)

        for kc_id in G.nodes:
            upsert_kc_state(sid, kc_id,
                            get_ontology_informed_prior(G, kc_id),
                            0, 0, False)

        return jsonify({"student_id": sid, "name": name})
    except Exception as e:
        import traceback; traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@app.get("/api/student/<sid>")
def student_info(sid):
    s = get_student(sid)
    if not s:
        return jsonify({"error": "not found"}), 404
    return jsonify({**s, **_progress_summary(sid)})


@app.get("/api/next-question/<sid>")
def next_question(sid):
    try:
        topic_filter = request.args.get("topic")   # opsional
        student  = _rebuild_student_model(sid)
        mastered = student.mastered_set()
        available = get_available_kcs(G, mastered)

        if topic_filter:
            available = [
                k for k in available
                if get_kc_info(G, k).get("topic") == topic_filter
            ]

        if not available:
            # Cek apakah topik ini sudah selesai semua
            if topic_filter:
                kcs_in_topic = [
                    n for n, d in G.nodes(data=True)
                    if d.get("topic") == topic_filter
                ]
                if all(k in mastered for k in kcs_in_topic):
                    return jsonify({"done": True,
                                    "message": "Topik ini sudah selesai! 🎉"})
                return jsonify({"done": True,
                                "message": "Selesaikan topik lain dulu ya! 🔒"})
            return jsonify({"done": True, "message": "Semua materi selesai! 🎉"})

        # Pilih KC dengan P(L) terendah di antara yang available
        next_kc = min(available, key=lambda k: student.kc_states[k].p_know)
        q = _get_question(next_kc)
        return jsonify({"done": False, **q})
    except Exception as e:
        import traceback; traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@app.post("/api/answer/<sid>")
def answer(sid):
    try:
        data    = request.json or {}
        kc_id   = data["kc_id"]
        correct = bool(data["correct"])

        student = _rebuild_student_model(sid)
        result  = process_response(student, G, kc_id, correct)
        _sync_to_db(student)
        log_interaction(sid, kc_id, correct, result["p_before"], result["p_after"])

        stars_earned = 0
        if correct:
            stars_earned = 2 if result["mastered"] else 1
            add_stars(sid, stars_earned)

        return jsonify({
            "correct":      correct,
            "mastered":     result["mastered"],
            "p_know":       round(result["p_after"], 3),
            "propagated":   result["propagated"],
            "stars_earned": stars_earned,
            "progress":     _progress_summary(sid),
        })
    except Exception as e:
        import traceback; traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@app.get("/api/progress/<sid>")
def progress(sid):
    try:
        db_states = get_all_kc_states(sid)
        topics: dict = {}
        for kc_id, state in db_states.items():
            topic = get_kc_info(G, kc_id).get("topic", "unknown")
            if topic not in topics:
                topics[topic] = {"mastered": 0, "total": 0}
            topics[topic]["total"] += 1
            if state["is_mastered"]:
                topics[topic]["mastered"] += 1
        return jsonify({**_progress_summary(sid), "topics": topics})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ── Admin Routes ──────────────────────────────────────────────────────────────
ADMIN_KEY = os.environ.get("ADMIN_KEY", "skripsi2025")

def _auth(req):
    return req.args.get("key") == ADMIN_KEY

@app.get("/admin/stats")
def admin_stats():
    if not _auth(request):
        return jsonify({"error": "Unauthorized"}), 401
    with get_conn() as conn:
        n_s   = conn.execute("SELECT COUNT(*) FROM students").fetchone()[0]
        n_i   = conn.execute("SELECT COUNT(*) FROM interactions").fetchone()[0]
        n_m   = conn.execute("SELECT COUNT(*) FROM kc_states WHERE is_mastered=1").fetchone()[0]
        acc   = conn.execute("SELECT AVG(correct) FROM interactions").fetchone()[0]
        rows  = conn.execute("""
            SELECT s.name,
                   COUNT(i.id) as n_inter,
                   ROUND(AVG(i.correct)*100,1) as acc,
                   COUNT(DISTINCT CASE WHEN ks.is_mastered=1 THEN ks.kc_id END) as mastered
            FROM students s
            LEFT JOIN interactions i  ON i.student_id=s.id
            LEFT JOIN kc_states ks    ON ks.student_id=s.id
            GROUP BY s.id ORDER BY s.created_at
        """).fetchall()
    return jsonify({
        "total_students":     n_s,
        "total_interactions": n_i,
        "total_kc_mastered":  n_m,
        "avg_accuracy_pct":   round((acc or 0)*100, 1),
        "students":           [dict(r) for r in rows],
    })

@app.get("/admin/export-csv")
def export_csv():
    if not _auth(request):
        return jsonify({"error": "Unauthorized"}), 401
    import csv, io
    out = io.StringIO()
    w   = csv.writer(out)
    w.writerow(["student_id","name","kc_id","correct","p_before","p_after","timestamp"])
    with get_conn() as conn:
        rows = conn.execute("""
            SELECT i.student_id, s.name, i.kc_id, i.correct,
                   i.p_before, i.p_after, i.timestamp
            FROM interactions i JOIN students s ON s.id=i.student_id
            ORDER BY i.student_id, i.timestamp
        """).fetchall()
    w.writerows(rows)
    return Response(out.getvalue(), mimetype="text/csv",
                    headers={"Content-Disposition": "attachment; filename=interactions.csv"})

@app.get("/admin/download-db")
def download_db():
    if not _auth(request):
        return jsonify({"error": "Unauthorized"}), 401
    return send_file(DB_PATH, as_attachment=True,
                     download_name="adaptive_learning.db",
                     mimetype="application/octet-stream")


# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    port  = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_ENV") == "development"
    app.run(host="0.0.0.0", port=port, debug=debug)
