"""Modèles simplifiés de l'ordre d'appel de groupes Parcoursup.

Le module traite un classement pédagogique strict, un taux minimum boursier
et un taux minimum de candidat·es du secteur. Il ne reproduit pas les
propositions quotidiennes, les groupes multiples ni les internats.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from fractions import Fraction
from typing import Iterable, TypeAlias

Rate: TypeAlias = Fraction | int | float | str
ApplicantType: TypeAlias = tuple[bool, bool]


@dataclass(frozen=True, slots=True)
class Applicant:
    """Candidat·e abstrait·e, avec rang, statut boursier et statut de secteur."""

    applicant_id: str
    rank: int
    scholarship_holder: bool
    resident_of_sector: bool = False


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
    if any(not isinstance(person.resident_of_sector, bool) for person in people):
        raise ValueError("Le statut de secteur doit être booléen.")
    return tuple(sorted(people, key=lambda person: person.rank))


def _is_rate_binding(called: int, total_available: int, rate: Fraction, prefix_size: int) -> bool:
    """Même comparaison exacte que dans le code officiel, sans arrondi flottant."""
    return total_available > called and called * rate.denominator < rate.numerator * prefix_size


def order_call_with_quotas(
    applicants: Iterable[Applicant],
    scholarship_rate: Rate,
    sector_rate: Rate = 0,
) -> tuple[Applicant, ...]:
    """Construit l'ordre d'appel d'un groupe soumis aux deux taux minimum.

    Les candidatures sont séparées en quatre files, triées par rang pédagogique :
    boursier·e du secteur, boursier·e hors secteur, non-boursier·e du secteur,
    non-boursier·e hors secteur. À chaque position, les taux encore réalisables
    contraignent les profils autorisés. Si les deux contraintes s'appliquent et
    qu'aucun profil ne peut satisfaire les deux, le meilleur rang boursier hors
    secteur est appelé : c'est la priorité donnée au taux boursier dans ce cas.

    Les taux sont des fractions entre 0 et 1 (par exemple 1/10 pour 10 %).
    Cette fonction reproduit l'ordre d'appel documenté pour un groupe à
    classement strict; elle ne calcule pas les propositions quotidiennes et ne
    modélise ni groupes multiples ni internats.
    """

    people = _validated_applicants(applicants)
    scholarship_quota = _as_rate(scholarship_rate)
    sector_quota = _as_rate(sector_rate)

    queues: dict[ApplicantType, deque[Applicant]] = {
        (True, True): deque(),
        (True, False): deque(),
        (False, True): deque(),
        (False, False): deque(),
    }
    for person in people:
        queues[(person.scholarship_holder, person.resident_of_sector)].append(person)

    total_scholars = sum(person.scholarship_holder for person in people)
    total_sector = sum(person.resident_of_sector for person in people)
    called_scholars = 0
    called_sector = 0
    result: list[Applicant] = []

    while len(result) < len(people):
        prefix_size = len(result) + 1
        scholarship_binding = _is_rate_binding(
            called_scholars, total_scholars, scholarship_quota, prefix_size
        )
        sector_binding = _is_rate_binding(
            called_sector, total_sector, sector_quota, prefix_size
        )

        eligible_heads = [
            queue[0]
            for (is_scholar, is_sector), queue in queues.items()
            if queue
            and (is_scholar or not scholarship_binding)
            and (is_sector or not sector_binding)
        ]

        if eligible_heads:
            chosen = min(eligible_heads, key=lambda person: person.rank)
        else:
            # Si aucun profil ne respecte les deux taux, ceux-ci doivent être
            # contraignants ensemble. Le code officiel donne alors priorité
            # aux boursier·es hors secteur.
            if not (scholarship_binding and sector_binding):
                raise AssertionError("Aucun profil admissible hors situation de conflit des deux taux.")
            scholarship_non_sector = queues[(True, False)]
            if not scholarship_non_sector:
                raise AssertionError("Le conflit des taux devrait laisser un·e boursier·e hors secteur.")
            chosen = scholarship_non_sector[0]

        queues[(chosen.scholarship_holder, chosen.resident_of_sector)].popleft()
        result.append(chosen)
        called_scholars += chosen.scholarship_holder
        called_sector += chosen.resident_of_sector

    return tuple(result)


def prefix_quota_order(applicants: Iterable[Applicant], rate: Rate) -> tuple[Applicant, ...]:
    """Compatibilité : ordre à quota boursier seul, sans taux de secteur."""
    return order_call_with_quotas(applicants, scholarship_rate=rate, sector_rate=0)


def _ceil_fraction(value: Fraction) -> int:
    return -(-value.numerator // value.denominator)


def choose_with_scholarship_reserve(
    applicants: Iterable[Applicant], capacity: int, rate: Rate
) -> tuple[Applicant, ...]:
    """Sélectionne un ensemble avec une réserve boursière libérée si inutilisée.

    Cette fonction expérimentale ne traite que le statut boursier et ne tient
    pas compte du secteur géographique. Elle renvoie un ensemble pour un ensemble
    donné de candidatures, pas un ordre d'appel.
    """

    people = _validated_applicants(applicants)
    quota_rate = _as_rate(rate)
    if isinstance(capacity, bool) or not isinstance(capacity, int) or capacity < 0:
        raise ValueError("La capacité doit être un entier positif ou nul.")

    reserve = _ceil_fraction(Fraction(capacity) * quota_rate)
    scholars = [person for person in people if person.scholarship_holder]
    chosen_scholars = scholars[:reserve]
    chosen_ids = {person.applicant_id for person in chosen_scholars}
    remaining = [person for person in people if person.applicant_id not in chosen_ids]
    general_seats = capacity - len(chosen_scholars)
    chosen = chosen_scholars + remaining[:general_seats]
    return tuple(sorted(chosen, key=lambda person: person.rank))
