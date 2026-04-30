"""
ontology.py — Pure logic, data-agnostic.

Cara pakai:
    import os as _os
    _base = _os.path.dirname(_os.path.abspath(__file__))
    G = build_ontology(_os.path.join(_base, "data", "math_grade1.json"))
    G = build_ontology("data/math_grade2.json")
"""

import json
import networkx as nx
from pathlib import Path


def build_ontology(data_path: str) -> nx.DiGraph:
    path = Path(data_path)
    if not path.exists():
        raise FileNotFoundError(f"Data file tidak ditemukan: {data_path}")
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    G = nx.DiGraph()
    G.graph["metadata"] = data.get("metadata", {})
    G.graph["topics"]   = data.get("topics", {})
    for kc in data["knowledge_components"]:
        G.add_node(kc["id"], **kc)
    for prereq, kc in data["prerequisites"]:
        G.add_edge(prereq, kc, relation="hasPrerequisite")
    return G


# ─── Query Functions ──────────────────────────────────────────────────────────
def get_prerequisites(G: nx.DiGraph, kc_id: str) -> list[str]:
    return list(G.predecessors(kc_id))

def get_all_prerequisites(G: nx.DiGraph, kc_id: str) -> list[str]:
    return list(nx.ancestors(G, kc_id))

def get_all_dependents(G: nx.DiGraph, kc_id: str) -> list[str]:
    """Semua KC yang (secara transitif) bergantung pada kc_id."""
    return list(nx.descendants(G, kc_id))

def get_dependents(G: nx.DiGraph, kc_id: str) -> list[str]:
    return list(G.successors(kc_id))

def get_kc_info(G: nx.DiGraph, kc_id: str) -> dict:
    return G.nodes[kc_id]

def get_kcs_by_topic(G: nx.DiGraph, topic: str) -> list[str]:
    return [n for n, d in G.nodes(data=True) if d.get("topic") == topic]

def get_available_kcs(G: nx.DiGraph, mastered: set[str]) -> list[str]:
    """KC yang belum mastered tapi semua prerequisite-nya sudah mastered."""
    return [
        kc_id for kc_id in G.nodes
        if kc_id not in mastered
        and all(p in mastered for p in get_prerequisites(G, kc_id))
    ]


# ─── Integrasi 1: Ontology-informed P(L₀) ────────────────────────────────────
def get_ontology_informed_prior(G: nx.DiGraph, kc_id: str) -> float:
    """
    P(L₀) berdasarkan posisi KC dalam ontologi.
    Dua faktor: difficulty (dari CP/TP) dan jumlah ancestor transitif.
    KC lebih jauh dari root kurikulum → prior lebih rendah.
    Rentang: 0.05–0.40. Acuan: Corbett & Anderson (1995).
    """
    n_prereqs  = len(get_all_prerequisites(G, kc_id))
    difficulty = G.nodes[kc_id].get("difficulty", 1)
    base       = {1: 0.35, 2: 0.25, 3: 0.15, 4: 0.10, 5: 0.05}
    prior      = base.get(difficulty, 0.20)
    penalty    = min(n_prereqs * 0.02, 0.15)
    return round(max(0.05, prior - penalty), 3)


# ─── Integrasi 4 (baru): Ontology-informed P(T) ───────────────────────────────
def get_ontology_informed_transit(G: nx.DiGraph, kc_id: str,
                                   base_pt: float = 0.10) -> float:
    """
    P(T) berdasarkan posisi KC dalam ontologi.

    Intuisi: KC yang lebih "fundamental" (banyak KC lain bergantung padanya)
    lebih mudah dipelajari karena menjadi pondasi yang sering diperkuat
    secara implisit. KC terminal (tidak ada dependent) lebih sulit karena
    tidak ada reinforcement dari KC lain.

    Mekanisme:
      - Hitung n_dependents: jumlah KC yang (transitif) bergantung pada KC ini
      - KC dengan banyak dependents → boost P(T) (lebih fundamental)
      - KC terminal → P(T) sedikit lebih rendah

    Rentang output: 0.07–0.20.
    Acuan: Konsisten dengan rentang Baker et al. (2008).
    """
    n_dep = len(get_all_dependents(G, kc_id))
    n_total = G.number_of_nodes()

    # Normalisasi: seberapa "sentral" KC ini (0.0 = terminal, 1.0 = paling fundamental)
    centrality = n_dep / (n_total - 1) if n_total > 1 else 0.0

    # Boost maksimal ±0.06 dari base
    boost = round(centrality * 0.06, 4)
    pt    = round(min(0.20, max(0.07, base_pt + boost)), 4)
    return pt


# ─── Integrasi 3 (improved): Learning-gain-aware KC selection ────────────────
def get_expected_learning_gain(G: nx.DiGraph, kc_id: str,
                                p_know: float, p_transit: float) -> float:
    """
    Expected learning gain jika KC ini dikerjakan satu soal.

    ELG = P(bisa belajar) × jumlah KC yang ter-unlock setelah mastery
        = (1 - P(L)) × P(T) × (1 + n_dependents_transitif)

    KC yang: (a) siswa belum kuasai, (b) P(T) tinggi, (c) banyak KC bergantung
    → ELG tinggi → prioritas lebih tinggi.
    """
    n_dep = len(get_all_dependents(G, kc_id))
    elg   = (1 - p_know) * p_transit * (1 + n_dep)
    return round(elg, 6)


def is_valid_learning_path(G: nx.DiGraph, path: list[str]) -> bool:
    mastered = set()
    for kc_id in path:
        if not all(p in mastered for p in get_prerequisites(G, kc_id)):
            return False
        mastered.add(kc_id)
    return True
