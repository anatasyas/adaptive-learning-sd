"""
database.py — SQLite schema dan CRUD
Tabel: students, kc_states, interactions, questions
"""

import sqlite3
from pathlib import Path
from datetime import datetime
from contextlib import contextmanager

import os as _os
_BASE = _os.path.dirname(_os.path.abspath(__file__))
DB_PATH = _os.path.join(_BASE, "data", "adaptive_learning.db")

@contextmanager
def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db():
    Path(DB_PATH).parent.mkdir(exist_ok=True)
    with get_conn() as conn:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS students (
            id          TEXT PRIMARY KEY,
            name        TEXT NOT NULL,
            subject     TEXT NOT NULL DEFAULT 'matematika',
            grade       INTEGER NOT NULL DEFAULT 1,
            avatar      INTEGER NOT NULL DEFAULT 1,
            total_stars INTEGER NOT NULL DEFAULT 0,
            created_at  TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS kc_states (
            student_id  TEXT NOT NULL,
            kc_id       TEXT NOT NULL,
            p_know      REAL NOT NULL,
            n_correct   INTEGER NOT NULL DEFAULT 0,
            n_incorrect INTEGER NOT NULL DEFAULT 0,
            is_mastered INTEGER NOT NULL DEFAULT 0,
            updated_at  TEXT NOT NULL,
            PRIMARY KEY (student_id, kc_id),
            FOREIGN KEY (student_id) REFERENCES students(id)
        );

        CREATE TABLE IF NOT EXISTS interactions (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id  TEXT NOT NULL,
            kc_id       TEXT NOT NULL,
            correct     INTEGER NOT NULL,
            p_before    REAL NOT NULL,
            p_after     REAL NOT NULL,
            timestamp   TEXT NOT NULL,
            FOREIGN KEY (student_id) REFERENCES students(id)
        );

        CREATE TABLE IF NOT EXISTS questions (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            kc_id      TEXT NOT NULL,
            question   TEXT NOT NULL,
            opt_a      TEXT NOT NULL,
            opt_b      TEXT NOT NULL,
            opt_c      TEXT NOT NULL,
            opt_d      TEXT NOT NULL,
            answer     TEXT NOT NULL CHECK(answer IN ('a','b','c','d')),
            difficulty INTEGER NOT NULL DEFAULT 1
        );
        """)


# ── Students ──────────────────────────────────────────────────────────────────
def create_student(student_id, name, avatar=1):
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO students (id,name,avatar,created_at) VALUES (?,?,?,?)",
            (student_id, name, avatar, datetime.now().isoformat())
        )
    return get_student(student_id)

def get_student(student_id):
    with get_conn() as conn:
        row = conn.execute("SELECT * FROM students WHERE id=?", (student_id,)).fetchone()
    return dict(row) if row else None

def add_stars(student_id, stars):
    with get_conn() as conn:
        conn.execute("UPDATE students SET total_stars=total_stars+? WHERE id=?", (stars, student_id))


# ── KC States ─────────────────────────────────────────────────────────────────
def upsert_kc_state(student_id, kc_id, p_know, n_correct, n_incorrect, is_mastered):
    with get_conn() as conn:
        conn.execute("""
            INSERT INTO kc_states (student_id,kc_id,p_know,n_correct,n_incorrect,is_mastered,updated_at)
            VALUES (?,?,?,?,?,?,?)
            ON CONFLICT(student_id,kc_id) DO UPDATE SET
                p_know=excluded.p_know, n_correct=excluded.n_correct,
                n_incorrect=excluded.n_incorrect, is_mastered=excluded.is_mastered,
                updated_at=excluded.updated_at
        """, (student_id, kc_id, p_know, n_correct, n_incorrect,
              int(is_mastered), datetime.now().isoformat()))

def get_kc_state(student_id, kc_id):
    with get_conn() as conn:
        row = conn.execute("SELECT * FROM kc_states WHERE student_id=? AND kc_id=?",
                           (student_id, kc_id)).fetchone()
    return dict(row) if row else None

def get_all_kc_states(student_id):
    with get_conn() as conn:
        rows = conn.execute("SELECT * FROM kc_states WHERE student_id=?", (student_id,)).fetchall()
    return {r["kc_id"]: dict(r) for r in rows}

def get_mastered_kcs(student_id):
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT kc_id FROM kc_states WHERE student_id=? AND is_mastered=1", (student_id,)
        ).fetchall()
    return {r["kc_id"] for r in rows}


# ── Interactions ──────────────────────────────────────────────────────────────
def log_interaction(student_id, kc_id, correct, p_before, p_after):
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO interactions (student_id,kc_id,correct,p_before,p_after,timestamp) VALUES (?,?,?,?,?,?)",
            (student_id, kc_id, int(correct), p_before, p_after, datetime.now().isoformat())
        )

def get_interaction_count(student_id):
    with get_conn() as conn:
        r = conn.execute("SELECT COUNT(*) as n FROM interactions WHERE student_id=?", (student_id,)).fetchone()
    return r["n"]


# ── Questions ─────────────────────────────────────────────────────────────────
def insert_question(kc_id, question, opt_a, opt_b, opt_c, opt_d, answer, difficulty=1):
    """answer: 'a'|'b'|'c'|'d' — huruf opsi yang benar."""
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO questions (kc_id,question,opt_a,opt_b,opt_c,opt_d,answer,difficulty) VALUES (?,?,?,?,?,?,?,?)",
            (kc_id, question, opt_a, opt_b, opt_c, opt_d, answer.lower(), difficulty)
        )

def get_random_question(kc_id):
    """Ambil satu soal acak untuk KC tertentu. Return dict siap pakai frontend."""
    with get_conn() as conn:
        row = conn.execute(
            "SELECT * FROM questions WHERE kc_id=? ORDER BY RANDOM() LIMIT 1", (kc_id,)
        ).fetchone()
    if not row:
        return None
    r = dict(row)
    opts = {"a": r["opt_a"], "b": r["opt_b"], "c": r["opt_c"], "d": r["opt_d"]}
    return {
        "id":      r["id"],
        "kc_id":   r["kc_id"],
        "q":       r["question"],
        "options": [r["opt_a"], r["opt_b"], r["opt_c"], r["opt_d"]],
        "answer":  opts[r["answer"]],  # teks jawaban benar
    }

def count_questions(kc_id=None):
    with get_conn() as conn:
        if kc_id:
            r = conn.execute("SELECT COUNT(*) FROM questions WHERE kc_id=?", (kc_id,)).fetchone()
        else:
            r = conn.execute("SELECT COUNT(*) FROM questions").fetchone()
    return r[0]

def questions_seeded():
    return count_questions() > 0


if __name__ == "__main__":
    init_db()
    print("DB ready:", DB_PATH)
