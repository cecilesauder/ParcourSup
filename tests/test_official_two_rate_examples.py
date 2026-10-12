"""Références officielles pour les taux boursier et secteur simultanés."""

import json
import random
import unittest
from fractions import Fraction
from pathlib import Path

from parcoursup_prototype.order_call import Applicant, order_call_with_quotas


FIXTURE_PATH = Path(__file__).parent / "fixtures" / "official_two_rate_examples.json"


def load_cases():
    with FIXTURE_PATH.open(encoding="utf-8") as fixture_file:
        return json.load(fixture_file)["cases"]


def _expand_ranges(ranges):
    return {
        number
        for first, last in ranges
        for number in range(first, last + 1)
    }


def applicants_from_case(case):
    """Reconstruit les entrées dans l’ordre pédagogique décrit par la source."""
    if "ranking" in case:
        return tuple(
            Applicant(applicant_id, rank, is_scholar, is_sector)
            for rank, (applicant_id, is_scholar, is_sector) in enumerate(
                case["ranking"], start=1
            )
        )

    group_ranges = case["groups_by_rank_range"]
    categories = {
        "boursier_du_secteur": (True, True),
        "boursier_hors_secteur": (True, False),
        "non_boursier_du_secteur": (False, True),
        "non_boursier_hors_secteur": (False, False),
    }
    membership = {}
    for group_name, ranges in group_ranges.items():
        if group_name not in categories:
            raise AssertionError(f"Profil inconnu dans le fixture : {group_name}")
        for rank in _expand_ranges(ranges):
            if rank in membership:
                raise AssertionError(f"Le rang {rank} appartient à deux profils.")
            membership[rank] = categories[group_name]

    expected_ranks = set(range(1, max(membership, default=0) + 1))
    if set(membership) != expected_ranks:
        raise AssertionError(f"Les rangs du fixture {case['id']} ne sont pas continus.")

    return tuple(
        Applicant(str(rank), rank, *membership[rank])
        for rank in sorted(membership)
    )


class OfficialTwoRateExampleTests(unittest.TestCase):
    def test_published_two_rate_example_and_demos_A5_A6_match_reference_orders(self):
        for case in load_cases():
            with self.subTest(case=case["id"]):
                scholarship_rate = Fraction(*case["scholarship_rate"])
                sector_rate = Fraction(*case["sector_rate"])
                applicants = applicants_from_case(case)

                actual = order_call_with_quotas(
                    applicants,
                    scholarship_rate=scholarship_rate,
                    sector_rate=sector_rate,
                )

                self.assertEqual(
                    [person.applicant_id for person in actual],
                    [str(value) for value in case["expected_order"]],
                )
                self.assertEqual(len(actual), len(applicants))
                self.assertEqual(
                    len({person.applicant_id for person in actual}),
                    len(applicants),
                )

    def test_demo_A6_starts_with_boursier_when_both_rates_conflict(self):
        case = next(case for case in load_cases() if case["id"] == "demo_A6")
        actual = order_call_with_quotas(
            applicants_from_case(case),
            scholarship_rate=Fraction(*case["scholarship_rate"]),
            sector_rate=Fraction(*case["sector_rate"]),
        )

        # Avec 10 % de boursier·es et 95 % du secteur, les deux taux
        # contraignent le premier appel. La règle officielle donne priorité
        # au taux boursier : B101 précède les résident·es classé·es 1 à 9.
        self.assertEqual(
            [person.applicant_id for person in actual[:10]],
            ["101", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
        )

    def test_demo_A5_overlapping_profiles_are_one_person_each(self):
        case = next(case for case in load_cases() if case["id"] == "demo_A5")
        applicants = applicants_from_case(case)
        actual = order_call_with_quotas(
            applicants,
            scholarship_rate=Fraction(*case["scholarship_rate"]),
            sector_rate=Fraction(*case["sector_rate"]),
        )

        both = [person for person in actual if person.scholarship_holder and person.resident_of_sector]
        self.assertEqual(
            [person.applicant_id for person in both],
            ["1", "2", "21", "22", "41"],
        )
        self.assertEqual(len({person.applicant_id for person in actual}), 100)

    def test_two_rate_order_is_independent_of_input_iteration_order(self):
        case = next(case for case in load_cases() if case["id"] == "demo_A6")
        applicants = applicants_from_case(case)
        shuffled = list(applicants)
        random.Random(20261012).shuffle(shuffled)

        expected = [str(value) for value in case["expected_order"]]
        actual = order_call_with_quotas(
            shuffled,
            scholarship_rate=Fraction(*case["scholarship_rate"]),
            sector_rate=Fraction(*case["sector_rate"]),
        )
        self.assertEqual([person.applicant_id for person in actual], expected)

    def test_invalid_sector_status_is_rejected(self):
        applicants = (Applicant("A", 1, False, 1),)
        with self.assertRaises(ValueError):
            order_call_with_quotas(applicants, Fraction(0), Fraction(0))

    def test_each_rate_is_validated_independently(self):
        with self.assertRaises(ValueError):
            order_call_with_quotas((), Fraction(0), Fraction(101, 100))
        with self.assertRaises(ValueError):
            order_call_with_quotas((), Fraction(-1, 100), Fraction(0))


if __name__ == "__main__":
    unittest.main()
