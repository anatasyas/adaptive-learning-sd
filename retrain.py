"""
retrain.py — Re-estimasi parameter BKT dari data interaksi nyata siswa.
Jalankan SETELAH export_data.py.

Alur:
  real_interactions.csv → param_estimator (grid search) → estimated_params.json (diupdate)

Setelah selesai, restart app.py agar model pakai parameter baru.
"""

import csv, json, math, itertools, os, sys
from pathlib import Path
from collections import defaultdict

os.chdir(Path(__file__).parent)
sys.path.insert(0, ".")
from ontology import build_ontology, get_ontology_informed_prior

REAL_DATA   = "data/real_interactions.csv"
PARAM_PATH  = "data/estimated_params.json"
DATA_PATH   = "data/math_grade1.json"

GRID = {
    "p_transit": [0.05, 0.10, 0.15, 0.20, 0.30, 0.40],
    "p_guess":   [0.10, 0.15, 0.20, 0.25, 0.30, 0.35],
    "p_slip":    [0.05, 0.08, 0.10, 0.15, 0.20, 0.25],
}

MIN_INTERACTIONS = 5  # KC dengan interaksi < ini pakai parameter sintetis


def _log_likelihood(responses, p0, pT, pG, pS):
    pL = p0
    ll = 0.0
    for correct in responses:
        p_correct = pL * (1 - pS) + (1 - pL) * pG
        p_obs = p_correct if correct else (1 - p_correct)
        if p_obs <= 0:
            return float("-inf")
        ll += math.log(p_obs)
        if correct:
            pL_given = (pL * (1 - pS)) / p_correct
        else:
            pL_given = (pL * pS) / (1 - p_correct)
        pL = pL_given + (1 - pL_given) * pT
        pL = max(0.001, min(0.999, pL))
    return ll


def _grid_search(sequences: dict, p0: float) -> dict:
    """sequences: {student_id: [0/1, ...]}"""
    best_ll  = float("-inf")
    best     = {"p_transit": 0.10, "p_guess": 0.25, "p_slip": 0.10}

    for pT, pG, pS in itertools.product(
        GRID["p_transit"], GRID["p_guess"], GRID["p_slip"]
    ):
        if pG >= (1 - pS):
            continue
        total_ll = sum(
            _log_likelihood(seq, p0, pT, pG, pS)
            for seq in sequences.values()
        )
        if total_ll > best_ll:
            best_ll = total_ll
            best = {"p_transit": pT, "p_guess": pG, "p_slip": pS}

    return best


def load_real_data() -> dict:
    """Load real_interactions.csv → {kc_id: {student_id: [correct, ...]}}"""
    if not Path(REAL_DATA).exists():
        print(f"❌ {REAL_DATA} tidak ditemukan. Jalankan export_data.py dulu.")
        sys.exit(1)

    data = defaultdict(lambda: defaultdict(list))
    with open(REAL_DATA, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            data[row["kc_id"]][row["student_id"]].append(int(row["correct"]))

    return data


def retrain():
    G    = build_ontology(DATA_PATH)
    data = load_real_data()

    # Load existing params sebagai fallback
    existing = {}
    if Path(PARAM_PATH).exists():
        with open(PARAM_PATH) as f:
            existing = json.load(f).get("ontologi", {})

    p0_map = {kc: get_ontology_informed_prior(G, kc) for kc in G.nodes}

    new_params = {}
    reused     = []
    retrained  = []

    for kc_id in sorted(G.nodes):
        sequences  = data.get(kc_id, {})
        n_inter    = sum(len(s) for s in sequences.values())

        if n_inter < MIN_INTERACTIONS:
            # Tidak cukup data nyata — pakai parameter lama
            new_params[kc_id] = existing.get(kc_id, {
                "p_transit": 0.10, "p_guess": 0.25, "p_slip": 0.10
            })
            reused.append(f"  {kc_id}: {n_inter} interaksi → pakai param lama")
        else:
            best = _grid_search(sequences, p0_map[kc_id])
            new_params[kc_id] = best
            retrained.append(
                f"  {kc_id}: {n_inter} interaksi → "
                f"pT={best['p_transit']} pG={best['p_guess']} pS={best['p_slip']}"
            )

    # Simpan
    out = {}
    if Path(PARAM_PATH).exists():
        with open(PARAM_PATH) as f:
            out = json.load(f)
    out["ontologi"] = new_params

    with open(PARAM_PATH, "w") as f:
        json.dump(out, f, indent=2)

    print(f"── Re-trained dari data nyata ({len(retrained)} KC) ──")
    for s in retrained:
        print(s)

    if reused:
        print(f"\n── Pakai parameter lama (data < {MIN_INTERACTIONS} interaksi) ──")
        for s in reused:
            print(s)

    print(f"\n✅ Parameter disimpan ke {PARAM_PATH}")
    print("Restart app.py agar model menggunakan parameter baru.")


if __name__ == "__main__":
    retrain()
