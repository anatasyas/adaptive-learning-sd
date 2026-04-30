"""
export_data.py — Export data interaksi siswa nyata dari DB ke CSV
Dijalankan SETELAH sesi testing selesai.

Output:
  data/real_interactions.csv
  data/real_students.csv
  data/real_kc_states.csv
"""

import csv, os, sys
from pathlib import Path

os.chdir(Path(__file__).parent)
sys.path.insert(0, ".")
from database import get_conn

OUT_DIR = Path("data")
OUT_DIR.mkdir(exist_ok=True)


def export_interactions():
    with get_conn() as conn:
        rows = conn.execute("""
            SELECT i.student_id, s.name, i.kc_id, i.correct,
                   i.p_before, i.p_after, i.timestamp
            FROM interactions i
            JOIN students s ON s.id = i.student_id
            ORDER BY i.student_id, i.timestamp
        """).fetchall()

    if not rows:
        print("Tidak ada data interaksi di DB.")
        return 0

    path = OUT_DIR / "real_interactions.csv"
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["student_id","name","kc_id","correct","p_before","p_after","timestamp"])
        w.writerows(rows)
    print(f"✅ Interaksi : {path} ({len(rows)} baris)")
    return len(rows)


def export_students():
    with get_conn() as conn:
        rows = conn.execute("""
            SELECT s.id, s.name, s.total_stars, s.created_at,
                   COUNT(i.id) as total_interactions,
                   SUM(i.correct) as total_correct,
                   COUNT(DISTINCT CASE WHEN ks.is_mastered=1 THEN ks.kc_id END) as kc_mastered
            FROM students s
            LEFT JOIN interactions i ON i.student_id = s.id
            LEFT JOIN kc_states ks ON ks.student_id = s.id
            GROUP BY s.id
            ORDER BY s.created_at
        """).fetchall()

    if not rows:
        print("Tidak ada data siswa di DB.")
        return 0

    path = OUT_DIR / "real_students.csv"
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["student_id","name","total_stars","created_at",
                    "total_interactions","total_correct","kc_mastered"])
        w.writerows(rows)
    print(f"✅ Siswa     : {path} ({len(rows)} siswa)")
    return len(rows)


def export_kc_states():
    with get_conn() as conn:
        rows = conn.execute("""
            SELECT ks.student_id, s.name, ks.kc_id,
                   ks.p_know, ks.n_correct, ks.n_incorrect, ks.is_mastered
            FROM kc_states ks
            JOIN students s ON s.id = ks.student_id
            ORDER BY ks.student_id, ks.kc_id
        """).fetchall()

    path = OUT_DIR / "real_kc_states.csv"
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["student_id","name","kc_id","p_know","n_correct","n_incorrect","is_mastered"])
        w.writerows(rows)
    print(f"✅ KC States : {path} ({len(rows)} baris)")
    return len(rows)


def print_summary():
    with get_conn() as conn:
        n_students = conn.execute("SELECT COUNT(*) FROM students").fetchone()[0]
        n_inter    = conn.execute("SELECT COUNT(*) FROM interactions").fetchone()[0]
        n_mastered = conn.execute("SELECT COUNT(*) FROM kc_states WHERE is_mastered=1").fetchone()[0]
        acc_row    = conn.execute("SELECT AVG(correct) FROM interactions").fetchone()[0]

    print("\n── Ringkasan Data Testing ──────────────────────")
    print(f"  Jumlah siswa      : {n_students}")
    print(f"  Total interaksi   : {n_inter}")
    print(f"  KC mastered       : {n_mastered}")
    if acc_row:
        print(f"  Akurasi rata-rata : {acc_row*100:.1f}%")
    print("─────────────────────────────────────────────────\n")


if __name__ == "__main__":
    print("Mengekspor data dari DB...\n")
    export_interactions()
    export_students()
    export_kc_states()
    print_summary()
    print("Jalankan retrain.py untuk re-estimasi parameter dari data nyata.")
