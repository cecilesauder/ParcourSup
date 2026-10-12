"""Prototypes simplifiés pour étudier les priorités boursiers de Parcoursup.

Ce module ne reproduit ni tous les paramètres ni le code de production de
Parcoursup. Il couvre uniquement le cas abstrait d'un classement strict et
 d'un taux minimum boursiers, sans taux de résidents ni internat.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Iterable, TypeAlias

Rate: TypeAlias = Fraction | int | float | str


@dataclass(frozen=True, slots=True)
class Applicant:
    """Candidat·e abstrait·e, avec priorité pédagogique stricte et statut social."""

    applicant_id: str
    rank: int
    scholarship_holder: bool


def _as_rate(rate: Rate) -> Fraction:
    if isinstance(rate, bool):
        raise ValueError("Le taux doit être un nombre entre 0 et 1.")
    try:
        result = rate if isinstance(rate, Fraction) else Fraction(str(rate))
    except (ValueError, ZeroDivisionError) as exc:
        raise ValueError("Le taux doit être un nombre entre 0 et 1.") from exc
    if result < 0 or result > 1:
        raise ValueError("Le taux doit être compris entre 0 et 1.")
    return result


def _validated_applicants(applicants: Iterable[Applicant]) -> tuple[Applicant, ...]:
    people = tuple(applicants)
    if any(not isinstance(person, Applicant) for person in people):
        raise TypeError("Chaque entrée doit être une instance d'Applicant.")
    if any(not person.applicant_id for person in people):
        raise ValueError("L'identifiant d'un·e candidat·e ne peut pas être vide.")
    ids = [person.applicant_id for person in people]
    ranks = [person.rank for person in people]
    if len(ids) != len(set(ids)):
        raise ValueError("Les identifiants doivent être uniques.")
    if any(isinstance(rank, bool) or not isinstance(rank, int) or rank < 1 for rank in ranks):
        raise ValueError("Les rangs doivent être des entiers strictement positifs.")
    if len(ranks) != len(set(ranks)):
        raise ValueError("Le classement doit être strict : les rangs doivent être uniques.")
    if any(not isinstance(person.scholarship_holder, bool) for person in people):
        raise ValueError("Le statut boursier doit être booléen.")
    return tuple(sorted(people, key=lambda person: person.rank))


def _ceil_fraction(value: Fraction) -> int:
    return -(-value.numerator // value.denominator)


def prefix_quota_order(applicants: Iterable[Applicant], rate: Rate) -> tuple[Applicant, ...]:
    """Construit l'ordre d'appel du modèle officiel simplifié « taux boursier seul ».

    À chaque rang, on prend le meilleur classement pédagogique disponible,
    sauf si ce choix rendrait le taux minimum boursiers contraignant et qu'il
    reste des candidat·es boursier·es : dans ce cas, on appelle le/la meilleur·e
    boursier·e restant·e. C'est la règle de préfixe spécifiée pour le cas sans
    taux de résidents; ce n'est pas une reproduction de toutes les variantes
    Parcoursup (résidents, groupes, internats, etc.).
    """

    people = _validated_applicants(applicants)
    quota_rate = _as_rate(rate)
    remaining_scholars = [p for p in people if p.scholarship_holder]
    remaining_others = [p for p in people if not p.scholarship_holder]
    scholar_count = 0
    result: list[Applicant] = []

    for k in range(1, len(people) + 1):
        required_scholars = _ceil_fraction(quota_rate * k)
        quota_binding = scholar_count < required_scholars
        if quota_binding and remaining_scholars:
            chosen = remaining_scholars.pop(0)
            scholar_count += 1
        else:
            candidates = [lst[0] for lst in (remaining_scholars, remaining_others) if lst]
            chosen = min(candidates, key=lambda person: person.rank)
            if chosen.scholarship_holder:
                remaining_scholars.pop(0)
                scholar_count += 1
            else:
                remaining_others.pop(0)
        result.append(chosen)

    return tuple(result)


def choose_with_scholarship_reserve(
    applicants: Iterable[Applicant], capacity: int, rate: Rate
) -> tuple[Applicant, ...]:
    """Sélectionne un ensemble avec une réserve boursière libérée si inutilisée.

    La réserve vaut ceil(capacity * rate). On choisit d'abord jusqu'à ce nombre
    de boursier·es selon le classement strict, puis les meilleurs candidat·es
    restants, quel que soit leur statut, jusqu'à remplir la capacité. Toute
    place réservée non occupée faute de boursier·es est ainsi ouverte aux autres.

    Le résultat est trié par rang pour faciliter la lecture, mais cet ordre ne
    constitue PAS un nouvel ordre d'appel : la fonction renvoie un ensemble
    choisi pour un ensemble donné de candidatures.
    """

    people = _validated_applicants(applicants)
    quota_rate = _as_rate(rate)
    if isinstance(capacity, bool) or not isinstance(capacity, int) or capacity < 0:
        raise ValueError("La capacité doit être un entier positif ou nul.")

    reserve = _ceil_fraction(Fraction(capacity) * quota_rate)
    scholars = [p for p in people if p.scholarship_holder]
    chosen_scholars = scholars[:reserve]
    chosen_ids = {person.applicant_id for person in chosen_scholars}
    remaining = [p for p in people if p.applicant_id not in chosen_ids]
    general_seats = capacity - len(chosen_scholars)
    chosen = chosen_scholars + remaining[:general_seats]
    return tuple(sorted(chosen, key=lambda person: person.rank))
