#!/usr/bin/env python3
"""Télécharge un snapshot annuel agrégé du jeu IPS des lycées de la DEPP.

Exemple : python scripts/telecharger_ips.py --rentree 2025-2026
Le fichier est récupéré depuis l'API officielle data.education.gouv.fr.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import tempfile
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
API_URL = (
    "https://data.education.gouv.fr/api/explore/v2.1/catalog/datasets/"
    "fr-en-ips-lycees-ap2023/records"
)
FIELDS = (
    "rentree_scolaire",
    "uai",
    "secteur",
    "type_de_lycee",
    "ips_etab",
    "ips_voie_gt",
    "ips_voie_pro",
    "ips_post_bac",
    "ecart_type_etablissement",
    "ecart_type_voie_gt",
    "ecart_type_voie_pro",
)
PAGE_SIZE = 100


def fetch_records(rentree: str) -> list[dict]:
    if not re.fullmatch(r"\d{4}-\d{4}", rentree):
        raise ValueError("La rentrée doit avoir le format AAAA-AAAA, par exemple 2025-2026.")
    records: list[dict] = []
    expected_count: int | None = None
    offset = 0
    while expected_count is None or offset < expected_count:
        params = urlencode(
            {
                "select": ",".join(FIELDS),
                "where": f"rentree_scolaire='{rentree}'",
                "limit": PAGE_SIZE,
                "offset": offset,
            }
        )
        request = Request(
            f"{API_URL}?{params}",
            headers={"User-Agent": "ParcourSup-IPS-audit/1.0 (public-data research)"},
        )
        with urlopen(request, timeout=60) as response:
            page = json.load(response)
        if expected_count is None:
            expected_count = int(page["total_count"])
        batch = page.get("results", [])
        if not batch and offset < expected_count:
            raise RuntimeError(
                f"L'API n'a renvoyé aucune ligne à l'offset {offset}, "
                f"alors que {expected_count} enregistrements étaient annoncés."
            )
        if any(row.get("rentree_scolaire") != rentree for row in batch):
            raise RuntimeError("L'API a renvoyé une ligne d'un autre millésime.")
        records.extend(batch)
        offset += len(batch)

    keys = [(row["rentree_scolaire"], row["uai"]) for row in records]
    if len(keys) != len(set(keys)):
        raise RuntimeError("L'API a renvoyé des doublons UAI pour cette rentrée.")
    if len(records) != expected_count:
        raise RuntimeError(
            f"Téléchargement incomplet : {len(records)} lignes reçues, "
            f"{expected_count} annoncées."
        )
    return records


def save_records(records: list[dict], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            "w", encoding="utf-8", newline="", dir=output.parent, delete=False
        ) as handle:
            temporary_path = Path(handle.name)
            writer = csv.DictWriter(
                handle, fieldnames=FIELDS, delimiter=";", extrasaction="ignore"
            )
            writer.writeheader()
            writer.writerows(records)
        os.replace(temporary_path, output)
    finally:
        if temporary_path is not None and temporary_path.exists():
            temporary_path.unlink()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rentree", default="2025-2026", help="Millésime AAAA-AAAA.")
    parser.add_argument("--output", type=Path, help="Chemin CSV de sortie.")
    args = parser.parse_args()
    output = args.output or ROOT / "data" / f"ips_lycees_{args.rentree}.csv"
    rows = fetch_records(args.rentree)
    save_records(rows, output)
    print(f"{len(rows)} enregistrements enregistrés dans {output}")
    print("Source : jeu DEPP fr-en-ips-lycees-ap2023, licence Etalab 2.0.")


if __name__ == "__main__":
    main()
