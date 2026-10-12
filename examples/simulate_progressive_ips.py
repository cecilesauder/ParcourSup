#!/usr/bin/env python3
"""Simule, sur un échantillon fictif, une pondération IPS croissante."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

from parcoursup_prototype.progressive_ips import (
    read_fictional_candidates,
    simulate_progressive_ips,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "examples" / "fixtures" / "fictional_candidates.csv"
DEFAULT_WEIGHTS = (0, 0.1, 0.2, 0.3, 0.4)


def _write_detail(path: Path, simulation) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = (
        "weight",
        "rank",
        "candidate_id",
        "origin_school",
        "school_context_ips",
        "merit_score",
        "merit_priority",
        "social_priority",
        "composite_score",
        "in_top_k",
    )
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter=";")
        writer.writeheader()
        for row in simulation.rankings:
            writer.writerow({field: getattr(row, field) for field in fields})


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT,
                        help="CSV d'exemple fictif (par défaut: fixture du dépôt).")
    parser.add_argument("--capacity", type=int, default=6,
                        help="Taille illustrative du top-k, entre 1 et le nombre de lignes.")
    parser.add_argument("--weights", type=float, nargs="+", default=list(DEFAULT_WEIGHTS),
                        help="Poids croissants entre 0 et 1, en commençant par 0.")
    parser.add_argument("--output", type=Path,
                        help="CSV détaillé facultatif pour les rangs de chaque scénario.")
    args = parser.parse_args()

    candidates = read_fictional_candidates(args.input)
    simulation = simulate_progressive_ips(candidates, args.weights, args.capacity)
    print("Simulation théorique — échantillon entièrement fictif")
    print(f"{len(candidates)} candidat·es; top-k={args.capacity}; aucun effet sur l'ordre d'appel Parcoursup.")
    print("Score = (1 - poids) × percentile de mérite + poids × priorité IPS du lycée.")
    print("Un IPS de lycée plus bas augmente la priorité de contexte dans cet exemple seulement.\n")
    print("poids | candidat·es dans le top-k | IPS moyen des lycées retenus | places remplacées vs poids 0 | rangs déplacés")
    for summary in simulation.summaries:
        ids = ", ".join(summary.selected_candidate_ids)
        print(
            f"{summary.weight:>4.0%} | {ids} | "
            f"{summary.selected_mean_school_ips:.2f} | "
            f"{summary.places_changed_from_baseline} | "
            f"{summary.candidates_moved_in_rank} "
            f"(déplacement moyen absolu: {summary.mean_absolute_rank_change:.2f})"
        )
    if args.output:
        _write_detail(args.output, simulation)
        print(f"\nDétail des rangs écrit dans {args.output}")
    print("\nCe scénario n'est ni une recommandation de règle, ni une estimation empirique d'équité ou d'admission.")


if __name__ == "__main__":
    main()
