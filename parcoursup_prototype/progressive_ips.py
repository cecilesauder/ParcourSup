"""Simulation illustrative d'une pondération progressive du contexte IPS.

Ce module est distinct de l'ordre d'appel Parcoursup. Il utilise une petite
population construite pour l'exemple; il ne constitue ni une règle proposée
ni une mesure d'impact sur des candidatures réelles.
"""

from __future__ import annotations

import csv
import math
from dataclasses import dataclass
from pathlib import Path
from statistics import fmean, median
from typing import Iterable, Sequence


@dataclass(frozen=True, slots=True)
class FictionalCandidate:
    """Candidat·e fictif·ve et contexte IPS moyen du lycée d'origine."""

    candidate_id: str
    merit_score: float
    origin_school: str
    school_context_ips: float


@dataclass(frozen=True, slots=True)
class CandidateRanking:
    weight: float
    candidate_id: str
    origin_school: str
    school_context_ips: float
    merit_score: float
    merit_priority: float
    social_priority: float
    composite_score: float
    rank: int
    in_top_k: bool


@dataclass(frozen=True, slots=True)
class ScenarioSummary:
    weight: float
    capacity: int
    selected_candidate_ids: tuple[str, ...]
    selected_mean_school_ips: float
    selected_median_school_ips: float
    places_changed_from_baseline: int
    candidates_moved_in_rank: int
    mean_absolute_rank_change: float


@dataclass(frozen=True, slots=True)
class ProgressiveIPSSimulation:
    capacity: int
    rankings: tuple[CandidateRanking, ...]
    summaries: tuple[ScenarioSummary, ...]


def read_fictional_candidates(path: str | Path) -> tuple[FictionalCandidate, ...]:
    """Lit un CSV d'exemple séparé par des points-virgules."""

    source = Path(path)
    required = {"candidate_id", "merit_score", "origin_school", "school_ips"}
    candidates: list[FictionalCandidate] = []
    with source.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle, delimiter=";")
        if reader.fieldnames is None or not required.issubset(reader.fieldnames):
            missing = sorted(required - set(reader.fieldnames or ()))
            raise ValueError(f"Colonnes manquantes dans {source}: {missing}.")
        for row_number, row in enumerate(reader, start=2):
            candidate_id = (row.get("candidate_id") or "").strip()
            origin_school = (row.get("origin_school") or "").strip()
            try:
                merit_score = float((row.get("merit_score") or "").strip())
                school_ips = float((row.get("school_ips") or "").strip())
            except ValueError as exc:
                raise ValueError(f"Score ou IPS illisible à la ligne {row_number}.") from exc
            if not candidate_id or not origin_school:
                raise ValueError(f"Identifiant ou lycée fictif absent à la ligne {row_number}.")
            if not math.isfinite(merit_score) or not math.isfinite(school_ips) or school_ips <= 0:
                raise ValueError(f"Score ou IPS hors limites à la ligne {row_number}.")
            candidates.append(
                FictionalCandidate(candidate_id, merit_score, origin_school, school_ips)
            )
    if not candidates:
        raise ValueError(f"Aucun candidat fictif dans {source}.")
    return tuple(candidates)


def _percentile_priorities(values: Sequence[float], *, higher_is_better: bool) -> tuple[float, ...]:
    """Convertit un classement en scores entre 0 et 1, avec rang moyen pour les ex æquo."""

    count = len(values)
    order = sorted(range(count), key=lambda index: values[index], reverse=higher_is_better)
    priorities = [0.0] * count
    start = 0
    while start < count:
        end = start + 1
        while end < count and values[order[end]] == values[order[start]]:
            end += 1
        average_rank = ((start + 1) + end) / 2
        percentile = 0.5 if count == 1 else (count - average_rank) / (count - 1)
        for position in range(start, end):
            priorities[order[position]] = percentile
        start = end
    return tuple(priorities)


def _validate_weights(weights: Iterable[float]) -> tuple[float, ...]:
    result: list[float] = []
    for value in weights:
        if isinstance(value, bool):
            raise ValueError("Chaque poids doit être un nombre entre 0 et 1.")
        try:
            weight = float(value)
        except (TypeError, ValueError) as exc:
            raise ValueError("Chaque poids doit être un nombre entre 0 et 1.") from exc
        if not math.isfinite(weight) or not 0 <= weight <= 1:
            raise ValueError("Chaque poids doit être compris entre 0 et 1.")
        result.append(weight)
    if not result or result[0] != 0:
        raise ValueError("La progression doit commencer à 0 pour fournir le scénario de base.")
    if any(left >= right for left, right in zip(result, result[1:])):
        raise ValueError("Les poids doivent être strictement croissants.")
    return tuple(result)


def simulate_progressive_ips(
    candidates: Iterable[FictionalCandidate],
    weights: Iterable[float],
    capacity: int,
) -> ProgressiveIPSSimulation:
    """Compare des classements fictifs selon une pondération IPS croissante.

    Les priorités de mérite et de contexte sont des percentiles dans le même
    échantillon. Le score final est ``(1 - poids) * mérite + poids * social``.
    Pour le terme social, un IPS de lycée plus faible reçoit une priorité plus
    élevée. Les poids doivent inclure 0 comme référence et être croissants.
    """

    people = tuple(candidates)
    if not people:
        raise ValueError("La simulation nécessite au moins un·e candidat·e.")
    if any(not isinstance(person, FictionalCandidate) for person in people):
        raise TypeError("Chaque entrée doit être un FictionalCandidate.")
    ids = [person.candidate_id for person in people]
    if any(not candidate_id for candidate_id in ids) or len(ids) != len(set(ids)):
        raise ValueError("Les identifiants des candidat·es doivent être présents et uniques.")
    for person in people:
        if not person.origin_school:
            raise ValueError("Chaque candidat·e doit avoir un lycée fictif renseigné.")
        if not math.isfinite(person.merit_score):
            raise ValueError("Les scores de mérite doivent être finis.")
        if not math.isfinite(person.school_context_ips) or person.school_context_ips <= 0:
            raise ValueError("Les IPS de contexte doivent être finis et strictement positifs.")
    if isinstance(capacity, bool) or not isinstance(capacity, int) or not 1 <= capacity <= len(people):
        raise ValueError("La capacité doit être un entier entre 1 et le nombre de candidat·es.")

    progression = _validate_weights(weights)
    merit_priorities = _percentile_priorities(
        [person.merit_score for person in people], higher_is_better=True
    )
    social_priorities = _percentile_priorities(
        [person.school_context_ips for person in people], higher_is_better=False
    )

    rankings: list[CandidateRanking] = []
    summaries: list[ScenarioSummary] = []
    baseline_ranks: dict[str, int] | None = None
    baseline_selected: set[str] | None = None

    for weight in progression:
        composite_scores = [
            (1 - weight) * merit + weight * social
            for merit, social in zip(merit_priorities, social_priorities)
        ]
        order = sorted(
            range(len(people)),
            key=lambda index: (
                -composite_scores[index],
                -merit_priorities[index],
                people[index].candidate_id,
            ),
        )
        ranks = {people[index].candidate_id: position for position, index in enumerate(order, 1)}
        selected_ids = {people[index].candidate_id for index in order[:capacity]}
        ordered_ips = [people[index].school_context_ips for index in order[:capacity]]

        if baseline_ranks is None:
            baseline_ranks = ranks
            baseline_selected = selected_ids
        assert baseline_selected is not None
        assert baseline_ranks is not None
        rank_changes = [
            abs(ranks[candidate_id] - baseline_ranks[candidate_id]) for candidate_id in ids
        ]
        selected_in_order = tuple(people[index].candidate_id for index in order[:capacity])
        summaries.append(
            ScenarioSummary(
                weight=weight,
                capacity=capacity,
                selected_candidate_ids=selected_in_order,
                selected_mean_school_ips=round(fmean(ordered_ips), 2),
                selected_median_school_ips=round(float(median(ordered_ips)), 2),
                places_changed_from_baseline=len(baseline_selected - selected_ids),
                candidates_moved_in_rank=sum(change != 0 for change in rank_changes),
                mean_absolute_rank_change=round(fmean(rank_changes), 2),
            )
        )
        for position, index in enumerate(order, 1):
            person = people[index]
            rankings.append(
                CandidateRanking(
                    weight=weight,
                    candidate_id=person.candidate_id,
                    origin_school=person.origin_school,
                    school_context_ips=person.school_context_ips,
                    merit_score=person.merit_score,
                    merit_priority=round(merit_priorities[index], 6),
                    social_priority=round(social_priorities[index], 6),
                    composite_score=round(composite_scores[index], 6),
                    rank=position,
                    in_top_k=position <= capacity,
                )
            )

    return ProgressiveIPSSimulation(
        capacity=capacity,
        rankings=tuple(rankings),
        summaries=tuple(summaries),
    )
