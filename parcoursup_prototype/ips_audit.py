"""Chargement et audit descriptif des IPS agrégés des lycées.

Ce module ne modifie pas l'ordre d'appel et ne déduit pas un statut social
individuel à partir de la moyenne d'un établissement.
"""

from __future__ import annotations

import csv
import math
from dataclasses import dataclass
from pathlib import Path
from statistics import fmean, median
from typing import Iterable

CSV_FIELDS = (
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

IPS_FIELDS = (
    "ips_etab",
    "ips_voie_gt",
    "ips_voie_pro",
    "ips_post_bac",
)

STANDARD_DEVIATION_FIELDS = (
    "ecart_type_etablissement",
    "ecart_type_voie_gt",
    "ecart_type_voie_pro",
)


@dataclass(frozen=True, slots=True)
class SchoolIPSRecord:
    """Un enregistrement officiel agrégé pour un lycée et une rentrée."""

    rentree_scolaire: str
    uai: str
    secteur: str
    type_de_lycee: str
    ips_etab: float | None
    ips_voie_gt: float | None
    ips_voie_pro: float | None
    ips_post_bac: float | None
    ecart_type_etablissement: float | None
    ecart_type_voie_gt: float | None
    ecart_type_voie_pro: float | None


def _optional_number(value: str | None, *, allow_zero: bool) -> float | None:
    if value is None or not value.strip() or value.strip() in {"-", "NA", "N/A"}:
        return None
    try:
        number = float(value.strip().replace(",", "."))
    except ValueError as exc:
        raise ValueError(f"Valeur numérique IPS invalide : {value!r}.") from exc
    if not math.isfinite(number) or number < 0 or (number == 0 and not allow_zero):
        raise ValueError(f"Valeur numérique IPS hors limites : {value!r}.")
    return number


def read_ips_records(
    path: str | Path,
    rentree_scolaire: str | None = None,
) -> tuple[SchoolIPSRecord, ...]:
    """Lit un CSV DEPP séparé par des points-virgules.

    Si une rentrée est donnée, les autres rentrées sont ignorées. Les lignes
    conservées doivent avoir un UAI et une rentrée uniques. Une mesure absente
    reste ``None``; elle n'est jamais transformée en zéro.
    """

    source = Path(path)
    required = set(CSV_FIELDS)
    records: list[SchoolIPSRecord] = []
    seen: set[tuple[str, str]] = set()
    with source.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle, delimiter=";")
        if reader.fieldnames is None or not required.issubset(reader.fieldnames):
            missing = sorted(required - set(reader.fieldnames or ()))
            raise ValueError(f"Colonnes IPS manquantes dans {source}: {missing}.")
        for row_number, row in enumerate(reader, start=2):
            year = (row.get("rentree_scolaire") or "").strip()
            if rentree_scolaire is not None and year != rentree_scolaire:
                continue
            uai = (row.get("uai") or "").strip()
            sector = (row.get("secteur") or "").strip()
            school_type = (row.get("type_de_lycee") or "").strip()
            if not year or not uai or not sector or not school_type:
                raise ValueError(f"Métadonnée obligatoire vide à la ligne {row_number}.")
            key = (year, uai)
            if key in seen:
                raise ValueError(f"UAI dupliqué pour la rentrée {year}: {uai}.")
            seen.add(key)

            numbers = {
                field: _optional_number(
                    row.get(field), allow_zero=field in STANDARD_DEVIATION_FIELDS
                )
                for field in (*IPS_FIELDS, *STANDARD_DEVIATION_FIELDS)
            }
            records.append(
                SchoolIPSRecord(
                    rentree_scolaire=year,
                    uai=uai,
                    secteur=sector,
                    type_de_lycee=school_type,
                    **numbers,
                )
            )

    if not records:
        suffix = f" pour la rentrée {rentree_scolaire}" if rentree_scolaire else ""
        raise ValueError(f"Aucun enregistrement IPS trouvé dans {source}{suffix}.")
    return tuple(records)


def _nearest_rank(values: list[float], probability: float) -> float:
    """Quantile par rang le plus proche : index ceil(p*n)-1."""

    ordered = sorted(values)
    index = max(0, math.ceil(probability * len(ordered)) - 1)
    return ordered[index]


def describe_values(values: Iterable[float]) -> dict[str, float | int] | None:
    """Résume des valeurs au niveau établissement, sans pondération d'effectif."""

    ordered = sorted(values)
    if not ordered:
        return None
    return {
        "count": len(ordered),
        "mean": round(fmean(ordered), 2),
        "p25": round(_nearest_rank(ordered, 0.25), 2),
        "median": round(float(median(ordered)), 2),
        "p75": round(_nearest_rank(ordered, 0.75), 2),
        "min": round(ordered[0], 2),
        "max": round(ordered[-1], 2),
    }


def _indicator_summary(records: tuple[SchoolIPSRecord, ...], field: str) -> dict:
    values = [value for record in records if (value := getattr(record, field)) is not None]
    return {
        "records": len(records),
        "available": len(values),
        "missing": len(records) - len(values),
        "statistics": describe_values(values),
    }


def _group_summary(records: tuple[SchoolIPSRecord, ...], field: str) -> dict[str, dict]:
    labels = sorted({getattr(record, field) for record in records})
    result: dict[str, dict] = {}
    for label in labels:
        group = tuple(record for record in records if getattr(record, field) == label)
        result[label] = {
            "establishments": len(group),
            **_indicator_summary(group, "ips_etab"),
        }
    return result


def audit_ips(records: Iterable[SchoolIPSRecord]) -> dict:
    """Produit des statistiques descriptives par établissement.

    Les moyennes et quantiles ne sont pas pondérés par le nombre d'élèves.
    Aucune donnée de candidature ou d'admission n'est entrée dans ce calcul.
    """

    rows = tuple(records)
    if not rows:
        raise ValueError("L'audit nécessite au moins un enregistrement IPS.")
    if any(not isinstance(row, SchoolIPSRecord) for row in rows):
        raise TypeError("Chaque enregistrement doit être un SchoolIPSRecord.")
    years = sorted({row.rentree_scolaire for row in rows})
    if len(years) != 1:
        raise ValueError("L'audit doit porter sur une seule rentrée scolaire.")
    keys = [(row.rentree_scolaire, row.uai) for row in rows]
    if len(keys) != len(set(keys)):
        raise ValueError("L'audit contient un UAI dupliqué pour une même rentrée.")

    return {
        "rentree_scolaire": years[0],
        "establishments": len(rows),
        "unique_uai": len({row.uai for row in rows}),
        "interpretation": "Statistiques non pondérées par établissement; pas des résultats d'admission.",
        "indicators": {field: _indicator_summary(rows, field) for field in IPS_FIELDS},
        "ips_etab_by_sector": _group_summary(rows, "secteur"),
        "ips_etab_by_school_type": _group_summary(rows, "type_de_lycee"),
    }
