#!/usr/bin/env python3
"""Affiche un résumé descriptif du snapshot IPS choisi."""

from __future__ import annotations

import argparse
from pathlib import Path

from parcoursup_prototype.ips_audit import audit_ips, read_ips_records

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CSV = ROOT / "data" / "ips_lycees_2025-2026.csv"
INDICATOR_LABELS = {
    "ips_etab": "IPS de l'établissement",
    "ips_voie_gt": "IPS voie générale et technologique",
    "ips_voie_pro": "IPS voie professionnelle",
    "ips_post_bac": "IPS post-bac",
}
TYPE_LABELS = {
    "LEGT": "LEGT",
    "LP": "LP",
    "LPO": "LPO",
}


def _print_statistics(statistics: dict | None) -> None:
    if statistics is None:
        print("aucune valeur renseignée")
        return
    print(
        f"n={statistics['count']}; moyenne={statistics['mean']}; "
        f"médiane={statistics['median']}; quartiles="
        f"[{statistics['p25']}, {statistics['p75']}]; "
        f"min-max=[{statistics['min']}, {statistics['max']}]"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv", type=Path, default=DEFAULT_CSV, help="Snapshot IPS CSV.")
    parser.add_argument("--rentree", default="2025-2026", help="Rentrée AAAA-AAAA.")
    args = parser.parse_args()

    records = read_ips_records(args.csv, rentree_scolaire=args.rentree)
    audit = audit_ips(records)
    print(f"Audit descriptif de l'IPS des lycées — {audit['rentree_scolaire']}")
    print(
        f"{audit['establishments']} établissements distincts; "
        f"{audit['unique_uai']} UAI distincts."
    )
    print("Chaque lycée compte une fois; les statistiques ne sont pas pondérées par effectif.")
    print("Aucune donnée de candidature ou d'admission n'est utilisée.")

    print("\nCouverture et distribution des indicateurs")
    for field, label in INDICATOR_LABELS.items():
        summary = audit["indicators"][field]
        print(
            f"- {label}: {summary['available']} renseignés, "
            f"{summary['missing']} absents sur {summary['records']}; "
            ""
        )
        print("  ", end="")
        _print_statistics(summary["statistics"])

    print("\nIPS moyen d'établissement par secteur")
    for label, summary in audit["ips_etab_by_sector"].items():
        print(
            f"- {label}: {summary['establishments']} lycées, "
            f"{summary['available']} IPS disponibles; "
            f"médiane={summary['statistics']['median'] if summary['statistics'] else 'n/a'}"
        )

    print("\nIPS moyen d'établissement par type de lycée")
    for label, summary in audit["ips_etab_by_school_type"].items():
        stat = summary["statistics"]
        print(
            f"- {TYPE_LABELS.get(label, label)}: {summary['establishments']} lycées, "
            f"{summary['available']} IPS disponibles; "
            f"médiane={stat['median'] if stat else 'n/a'}"
        )


if __name__ == "__main__":
    main()
