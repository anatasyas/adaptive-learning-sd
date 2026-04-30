"""
Adaptive Engine + Evaluator
Membandingkan: BKT+Ontologi vs BKT Baseline (tanpa ontologi)

Metrik:
  Level 1 (prediksi) : AUC-ROC, RMSE, Accuracy
  Level 2 (ontologi) : avg attempts to mastery, path validity,
                       parameter recovery RMSE, % students completed
"""

import csv
import json
import math
import random
from collections import defaultdict
from pathlib import Path
from typing import Optional

import networkx as nx

from ontology import (
    build_ontology,
    get_available_kcs,
    get_kc_info,
    get_ontology_informed_prior,
    get_prerequisites,
)
from bkt_engine import (
    StudentModel, KCState,
    bkt_update, init_student, process_response,
    select_next_kc, DEFAULT_BKT_PARAMS, KC_PARAM_OVERRIDES,
)


# ─── 0. Load Estimated Parameters ────────────────────────────────────────────
def load_estimated_params(path: str = "data/estimated_params.json") -> dict:
    """
    Load hasil estimasi dari param_estimator.py.
    Jika belum ada, kembalikan dict kosong (fallback ke default).
    """
    p = Path(path)
    if not p.exists():
        print(f"  [WARN] {path} not found — using default params. "
              "Run param_estimator.py first for better results.")
        return {"ontologi": {}, "baseline": {}}
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def _resolve_params(kc_id: str, estimated: dict) -> dict:
    """Ambil estimated params jika ada, fallback ke DEFAULT_BKT_PARAMS."""
    if kc_id in estimated:
        return {
            "p_transit": estimated[kc_id]["p_transit"],
            "p_guess":   estimated[kc_id]["p_guess"],
            "p_slip":    estimated[kc_id]["p_slip"],
            "mastery_threshold": DEFAULT_BKT_PARAMS["mastery_threshold"],
        }
    params = dict(DEFAULT_BKT_PARAMS)
    if kc_id in KC_PARAM_OVERRIDES:
        params.update(KC_PARAM_OVERRIDES[kc_id])
    return params


# ─── 1. Baseline Model ────────────────────────────────────────────────────────
FLAT_PRIOR = 0.35

def init_student_baseline(
    student_id: str,
    G: nx.DiGraph,
    estimated_params: dict = None,
) -> StudentModel:
    """BKT Baseline: flat P(L0), tanpa info ontologi."""
    student = StudentModel(student_id=student_id)
    est     = estimated_params or {}
    for kc_id in G.nodes:
        params = _resolve_params(kc_id, est)
        student.kc_states[kc_id] = KCState(
            kc_id             = kc_id,
            p_know            = FLAT_PRIOR,
            p_transit         = params["p_transit"],
            p_guess           = params["p_guess"],
            p_slip            = params["p_slip"],
            mastery_threshold = params["mastery_threshold"],
        )
    return student


def select_next_kc_baseline(
    student: StudentModel,
    G: nx.DiGraph,
    kc_order: list[str],  # urutan random yang di-fix saat init siswa
) -> Optional[str]:
    """
    Baseline KC selection: urutan random (di-fix per siswa, tapi acak).
    Tidak ada prerequisite check — ini yang membedakan dari ontologi.
    """
    for kc_id in kc_order:
        if not student.kc_states[kc_id].is_mastered:
            return kc_id
    return None


# ─── 2. Load Dataset ──────────────────────────────────────────────────────────
def load_dataset(csv_path: str) -> list[dict]:
    rows = []
    with open(csv_path, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            rows.append({
                "student_id":           row["student_id"],
                "kc_id":                row["kc_id"],
                "opportunity":          int(row["opportunity"]),
                "correct":              int(row["correct"]),
                "true_knowledge_state": int(row["true_knowledge_state"]),
                "true_p0":              float(row["true_p0"]),
                "true_pT":              float(row["true_pT"]),
                "true_pG":              float(row["true_pG"]),
                "true_pS":              float(row["true_pS"]),
            })
    return rows


def group_by_student(rows: list[dict]) -> dict[str, list[dict]]:
    groups = defaultdict(list)
    for row in rows:
        groups[row["student_id"]].append(row)
    return dict(groups)


# ─── 3. Replay — untuk metrik prediksi (Level 1) ─────────────────────────────
def replay_student(
    student_rows: list[dict],
    G: nx.DiGraph,
    use_ontology: bool,
    est_params: dict = None,
) -> list[dict]:
    """
    Replay interaksi dari dataset. Catat P(correct) sebelum update
    (one-step-ahead prediction). Standar evaluasi BKT — Baker et al. (2008).
    """
    student_id = student_rows[0]["student_id"]
    student = (init_student(student_id, G) if use_ontology
               else init_student_baseline(student_id, G, est_params))

    predictions = []
    for row in student_rows:
        kc_id   = row["kc_id"]
        state   = student.kc_states[kc_id]
        pL, pG, pS = state.p_know, state.p_guess, state.p_slip

        # Prediksi sebelum update
        p_pred = pL * (1 - pS) + (1 - pL) * pG
        predictions.append({
            "actual":    row["correct"],
            "predicted": p_pred,
        })

        process_response(student, G, kc_id, bool(row["correct"]))

    return predictions


# ─── 4. Simulate Adaptive Session — untuk metrik ontologi (Level 2) ──────────
def simulate_adaptive_session(
    student_id: str,
    G: nx.DiGraph,
    use_ontology: bool,
    question_bank: dict[str, list[int]],
    rng: random.Random,
    max_questions: int = 1000,
    est_params: dict = None,
) -> dict:
    """
    Simulasi sesi adaptive dari awal sampai semua KC mastered atau habis quota.
    """
    student    = (init_student(student_id, G) if use_ontology
                  else init_student_baseline(student_id, G, est_params))

    # Baseline pakai urutan KC random yang di-fix untuk siswa ini
    # Ini yang membuat baseline benar-benar tidak prerequisite-aware
    kc_order_baseline = list(G.nodes)
    rng.shuffle(kc_order_baseline)

    total_q    = 0
    mastered   = set()
    path_log   = []
    valid_steps = 0

    for _ in range(max_questions):
        # KC selection
        if use_ontology:
            next_kc = select_next_kc(student, G)
        else:
            next_kc = select_next_kc_baseline(student, G, kc_order_baseline)

        if next_kc is None:
            break

        # Cek validitas step ini secara ontologi (untuk kedua model)
        prereqs = get_prerequisites(G, next_kc)
        if all(p in mastered for p in prereqs):
            valid_steps += 1

        path_log.append(next_kc)

        # Ambil respons dari question_bank
        pool    = question_bank.get(next_kc, [0, 1])
        correct = rng.choice(pool)

        result  = process_response(student, G, next_kc, bool(correct))
        total_q += 1

        if result["mastered"] and next_kc not in mastered:
            mastered.add(next_kc)

    n_total       = G.number_of_nodes()
    path_validity = valid_steps / len(path_log) if path_log else 0

    return {
        "student_id":          student_id,
        "n_mastered":          len(mastered),
        "n_total":             n_total,
        "completed":           len(mastered) == n_total,
        "pct_kcs_mastered":    round(len(mastered) / n_total * 100, 1),
        "total_questions":     total_q,
        "avg_attempts_per_kc": round(total_q / max(len(mastered), 1), 2),
        "path_validity":       round(path_validity, 4),
    }


# ─── 5. Parameter Recovery ────────────────────────────────────────────────────
def compute_parameter_recovery(
    rows_by_student: dict[str, list[dict]],
    G: nx.DiGraph,
    use_ontology: bool,
) -> float:
    """
    RMSE antara P(L0) yang diestimasi sistem vs true P(L0) dari data sintetis.
    Hanya bisa dihitung karena ground truth tersedia di data sintetis.
    """
    errors = []
    for student_rows in rows_by_student.values():
        student_id = student_rows[0]["student_id"]
        student    = (init_student(student_id, G) if use_ontology
                      else init_student_baseline(student_id, G))
        seen = set()
        for row in student_rows:
            kc_id = row["kc_id"]
            if kc_id not in seen:
                est_p0  = student.kc_states[kc_id].p_know
                true_p0 = row["true_p0"]
                errors.append((est_p0 - true_p0) ** 2)
                seen.add(kc_id)
            process_response(student, G, kc_id, bool(row["correct"]))

    return round(math.sqrt(sum(errors) / len(errors)), 4) if errors else 0.0


# ─── 6. Prediction Metrics ────────────────────────────────────────────────────
def compute_auc_roc(predictions: list[dict]) -> float:
    actual, predicted = [p["actual"] for p in predictions], [p["predicted"] for p in predictions]
    n_pos = sum(actual); n_neg = len(actual) - n_pos
    if n_pos == 0 or n_neg == 0:
        return 0.5

    thresholds = sorted(set(predicted), reverse=True)
    tpr_list, fpr_list = [0.0], [0.0]
    for t in thresholds:
        tp = sum(1 for a, p in zip(actual, predicted) if p >= t and a == 1)
        fp = sum(1 for a, p in zip(actual, predicted) if p >= t and a == 0)
        tpr_list.append(tp / n_pos)
        fpr_list.append(fp / n_neg)
    tpr_list.append(1.0); fpr_list.append(1.0)

    auc = sum(
        (fpr_list[i] - fpr_list[i-1]) * (tpr_list[i] + tpr_list[i-1]) / 2
        for i in range(1, len(tpr_list))
    )
    return round(auc, 4)


def compute_rmse(predictions: list[dict]) -> float:
    errors = [(p["predicted"] - p["actual"]) ** 2 for p in predictions]
    return round(math.sqrt(sum(errors) / len(errors)), 4)


def compute_accuracy(predictions: list[dict], threshold: float = 0.5) -> float:
    correct = sum(
        1 for p in predictions
        if (p["predicted"] >= threshold) == bool(p["actual"])
    )
    return round(correct / len(predictions), 4)


# ─── 7. Full Evaluation ───────────────────────────────────────────────────────
def evaluate(
    test_csv: str,
    G: nx.DiGraph,
    use_ontology: bool,
    rng: random.Random,
    estimated_params_path: str = "data/estimated_params.json",
) -> dict:
    rows       = load_dataset(test_csv)
    by_student = group_by_student(rows)

    # Load estimated params dari training
    all_est   = load_estimated_params(estimated_params_path)
    est_params = all_est["ontologi"] if use_ontology else all_est["baseline"]

    # Level 1: prediction metrics
    all_preds = []
    for student_rows in by_student.values():
        all_preds.extend(replay_student(student_rows, G, use_ontology, est_params))

    param_rmse = compute_parameter_recovery(by_student, G, use_ontology)

    # Level 2: adaptive session metrics
    question_bank = defaultdict(list)
    for row in rows:
        question_bank[row["kc_id"]].append(row["correct"])

    session_results = [
        simulate_adaptive_session(
            student_id   = sid,
            G            = G,
            use_ontology = use_ontology,
            question_bank= question_bank,
            rng          = random.Random(rng.randint(0, 9999)),
            est_params   = est_params,
        )
        for sid in by_student
    ]

    n = len(session_results)
    return {
        # Level 1
        "auc_roc":              compute_auc_roc(all_preds),
        "rmse":                 compute_rmse(all_preds),
        "accuracy":             compute_accuracy(all_preds),
        "param_recovery_rmse":  param_rmse,
        # Level 2
        "avg_attempts_per_kc":    round(sum(r["avg_attempts_per_kc"] for r in session_results) / n, 2),
        "avg_kcs_mastered_pct":   round(sum(r["pct_kcs_mastered"]    for r in session_results) / n, 1),
        "path_validity_pct":      round(sum(r["path_validity"]        for r in session_results) / n * 100, 1),
        "pct_students_completed": round(sum(r["completed"]            for r in session_results) / n * 100, 1),
    }


# ─── 8. Run ───────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import os
    os.chdir(Path(__file__).parent)

    G        = build_ontology("data/math_grade1.json")
    test_csv = "data/matematika_grade1_test.csv"

    print("Evaluating on test set...\n")
    results = {}
    for label, use_onto in [("BKT + Ontologi", True), ("BKT Baseline", False)]:
        print(f"  Running {label}...")
        results[label] = evaluate(test_csv, G, use_onto, random.Random(42))

    metrics = [
        ("AUC-ROC",                     "auc_roc",                "↑"),
        ("RMSE",                        "rmse",                   "↓"),
        ("Accuracy",                    "accuracy",               "↑"),
        ("Param Recovery RMSE P(L0)",   "param_recovery_rmse",    "↓"),
        ("Avg attempts per KC",         "avg_attempts_per_kc",    "↓"),
        ("Avg KCs mastered (%)",        "avg_kcs_mastered_pct",   "↑"),
        ("Path validity (%)",           "path_validity_pct",      "↑"),
        ("Students completed (%)",      "pct_students_completed", "↑"),
    ]

    w = 30
    print(f"\n{'─'*72}")
    print(f"  {'Metric':<{w}}  {'BKT+Ontologi':>14}  {'BKT Baseline':>14}  Better")
    print(f"{'─'*72}")
    for label, key, direction in metrics:
        v1 = results["BKT + Ontologi"][key]
        v2 = results["BKT Baseline"][key]
        better_model = "BKT+Onto" if (
            (direction == "↑" and v1 > v2) or
            (direction == "↓" and v1 < v2)
        ) else ("Baseline" if v1 != v2 else "tie")
        print(f"  {label:<{w}}  {str(v1):>14}  {str(v2):>14}  {better_model}")
    print(f"{'─'*72}")
