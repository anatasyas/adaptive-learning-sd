"""
inject_fake_data.py — Generate data simulasi 25 siswa
Komposisi: 35% slow learner, 45% average learner, 20% fast learner

PENTING: Data ini adalah SIMULASI, bukan data nyata.
         Dalam skripsi harus dilabeli sebagai "data simulasi"
         atau "data sintetis berbasis BKT generative process".
"""

import os, sys, random
from datetime import datetime, timedelta

os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ".")

from database import (
    init_db, get_conn, DB_PATH,
    create_student, upsert_kc_state, log_interaction
)
from ontology import build_ontology, get_ontology_informed_prior, get_available_kcs

init_db()

with get_conn() as conn:
    n_existing = conn.execute("SELECT COUNT(*) FROM students").fetchone()[0]

if n_existing > 0:
    print(f"Sudah ada {n_existing} siswa, skip inject.")
    sys.exit(0)

DATA_PATH = "data/math_grade1.json"
G = build_ontology(DATA_PATH)
ALL_KCS = list(G.nodes)
MASTERY_THRESHOLD = 0.80
random.seed(2025)

# ── Nama siswa SD Indonesia ────────────────────────────────────────────────────
NAMES = [
    # Slow (9 siswa)
    "Agus","Bambang","Cahya","Dedi","Eka",
    "Fitri","Galih","Hendra","Indah",
    # Average (11 siswa)
    "Joko","Kartini","Lestari","Mulyono","Nita",
    "Oki","Putu","Qori","Rendra","Suci","Tini",
    # Fast (5 siswa)
    "Umar","Vina","Wahyu","Xena","Yusuf",
]

# ── Profil per tipe ────────────────────────────────────────────────────────────
PROFILES = {
    "slow": {
        "p_transit": 0.05, "p_guess": 0.17, "p_slip": 0.24,
        "n_min": 14, "n_max": 22,
        "desc": "Slow Learner"
    },
    "average": {
        "p_transit": 0.12, "p_guess": 0.22, "p_slip": 0.14,
        "n_min": 22, "n_max": 34,
        "desc": "Average Learner"
    },
    "fast": {
        "p_transit": 0.22, "p_guess": 0.28, "p_slip": 0.07,
        "n_min": 32, "n_max": 45,
        "desc": "Fast Learner"
    },
}

# Komposisi: 9 slow, 11 average, 5 fast = 25 siswa
ASSIGNMENTS = (
    ["slow"]    * 9 +
    ["average"] * 11 +
    ["fast"]    * 5
)

def bkt_update(p_know, correct, pT, pG, pS):
    p_correct = p_know*(1-pS) + (1-p_know)*pG
    p_correct = max(0.001, min(0.999, p_correct))
    p_lg = p_know*(1-pS)/p_correct if correct else p_know*pS/(1-p_correct)
    p_lg = max(0.001, min(0.999, p_lg))
    return max(0.001, min(0.999, p_lg + (1-p_lg)*pT))

def respond(p_know, pG, pS):
    if p_know > random.random():
        return random.random() > pS
    return random.random() < pG

# ── Simulasi ───────────────────────────────────────────────────────────────────
session_start = datetime(2025, 5, 20, 8, 0, 0)

print(f"{'Nama':<12} {'Soal':>5} {'Akurasi':>8} {'KC Mastered':>12}")
print("-" * 44)

for i, (name, profile_key) in enumerate(zip(NAMES, ASSIGNMENTS)):
    prof = PROFILES[profile_key]
    sid  = f"S{str(i+1).zfill(3)}"
    avatar = random.randint(1, 5)

    create_student(sid, name, avatar)

    # Init KC states
    kc_states = {
        kc: {"p_know": get_ontology_informed_prior(G, kc),
             "n_correct": 0, "n_incorrect": 0, "is_mastered": False}
        for kc in ALL_KCS
    }

    n_soal = random.randint(prof["n_min"], prof["n_max"])
    pT, pG, pS = prof["p_transit"], prof["p_guess"], prof["p_slip"]
    t_now = session_start + timedelta(
        minutes=i * random.uniform(0.3, 1.2),
        seconds=random.uniform(0, 30)
    )

    n_correct = 0
    for _ in range(n_soal):
        mastered_set = {k for k,v in kc_states.items() if v["is_mastered"]}
        available    = get_available_kcs(G, mastered_set)
        if not available:
            break
        kc_id    = min(available, key=lambda k: kc_states[k]["p_know"])
        p_before = kc_states[kc_id]["p_know"]
        correct  = respond(p_before, pG, pS)
        p_after  = bkt_update(p_before, correct, pT, pG, pS)

        kc_states[kc_id]["p_know"] = p_after
        if correct:
            kc_states[kc_id]["n_correct"] += 1
            n_correct += 1
        else:
            kc_states[kc_id]["n_incorrect"] += 1

        if p_after >= MASTERY_THRESHOLD and not kc_states[kc_id]["is_mastered"]:
            kc_states[kc_id]["is_mastered"] = True

        log_interaction(sid, kc_id, correct, p_before, p_after)
        t_now += timedelta(seconds=random.uniform(30, 70))

    # Simpan KC states
    for kc_id, s in kc_states.items():
        upsert_kc_state(sid, kc_id, s["p_know"],
                        s["n_correct"], s["n_incorrect"], s["is_mastered"])

    stars = n_correct * 1 + sum(1 for v in kc_states.values() if v["is_mastered"]) * 2
    with get_conn() as conn:
        conn.execute("UPDATE students SET total_stars=? WHERE id=?", (stars, sid))

    acc      = round(n_correct / n_soal * 100, 1) if n_soal else 0
    mastered = sum(1 for v in kc_states.values() if v["is_mastered"])
    print(f"{name:<12} {n_soal:>5} {acc:>7.1f}% {mastered:>12}")

# ── Summary ────────────────────────────────────────────────────────────────────
with get_conn() as conn:
    n_s  = conn.execute("SELECT COUNT(*) FROM students").fetchone()[0]
    n_i  = conn.execute("SELECT COUNT(*) FROM interactions").fetchone()[0]
    n_m  = conn.execute("SELECT COUNT(*) FROM kc_states WHERE is_mastered=1").fetchone()[0]
    acc  = conn.execute("SELECT AVG(correct) FROM interactions").fetchone()[0]

print("\n" + "="*58)
print(f"  Total siswa       : {n_s}")
print(f"  Total interaksi   : {n_i}")
print(f"  KC mastered       : {n_m}")
print(f"  Akurasi rata-rata : {round((acc or 0)*100, 1)}%")
print("="*58)
print("\nData simulasi berhasil dibuat.")
print("Pastikan dilabeli 'data simulasi' dalam skripsi.")
