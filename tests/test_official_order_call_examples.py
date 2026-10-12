"""Cas de référence pour l'ordre d'appel à taux boursier seul.

Sources des entrées : guide officiel 2025, section 4.1, et exemples A1/A2/A4
à commit public épinglé dans tests/fixtures/official_order_call_examples.json.
Le guide publie explicitement la sortie du cas à 25 %. Les démos A1/A2/A4
ne sont pas des assertions de sorties dans le JUnit officiel : leurs sorties
attendues sont consignées ici à partir de la règle publiée §4.1.
"""

import json
import unittest
from fractions import Fraction
from pathlib import Path

from parcoursup_prototype.order_call import Applicant, prefix_quota_order


FIXTURE_PATH = Path(__file__).parent / "fixtures" / "official_order_call_examples.json"


def load_cases():
    with FIXTURE_PATH.open(encoding="utf-8") as fixture_file:
        return json.load(fixture_file)["cases"]


class OfficialOrderCallExampleTests(unittest.TestCase):
    def test_documented_and_demo_examples_match_exact_expected_order(self):
        for case in load_cases():
            with self.subTest(case=case["id"]):
                numerator, denominator = case["rate"]
                applicants = tuple(
                    Applicant(applicant_id, rank, is_scholar)
                    for rank, (applicant_id, is_scholar) in enumerate(case["ranking"], start=1)
                )

                actual = prefix_quota_order(
                    applicants,
                    Fraction(numerator, denominator),
                )

                self.assertEqual(
                    [person.applicant_id for person in actual],
                    case["expected_order"],
                )
                self.assertEqual(len(actual), len(applicants))
                self.assertEqual(
                    {person.applicant_id for person in actual},
                    {person.applicant_id for person in applicants},
                )

    def test_official_large_demo_A3_expected_order(self):
        # L'exemple public A3 contient C1...C900 puis B901...B1000,
        # avec un taux boursier de 10 %. La règle officielle appelle le
        # premier boursier, puis neuf candidats du classement, et répète.
        applicants = tuple(
            [Applicant(f"C{i}", i, False) for i in range(1, 901)]
            + [Applicant(f"B{i}", i, True) for i in range(901, 1001)]
        )

        expected = []
        for block in range(100):
            expected.append(f"B{901 + block}")
            first_non_scholar = 1 + 9 * block
            last_non_scholar = min(first_non_scholar + 8, 900)
            expected.extend(
                f"C{i}" for i in range(first_non_scholar, last_non_scholar + 1)
            )

        actual = prefix_quota_order(applicants, Fraction(1, 10))
        self.assertEqual([person.applicant_id for person in actual], expected)
        self.assertEqual(len(actual), 1000)
        self.assertEqual(
            [person.applicant_id for person in actual if person.scholarship_holder],
            [f"B{i}" for i in range(901, 1001)],
        )


if __name__ == "__main__":
    unittest.main()
