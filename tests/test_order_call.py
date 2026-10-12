import itertools
import unittest
from fractions import Fraction

from parcoursup_prototype.order_call import (
    Applicant,
    choose_with_scholarship_reserve,
    prefix_quota_order,
)


class PrefixOrderTests(unittest.TestCase):
    def setUp(self):
        self.people = (
            Applicant("N1", 1, False),
            Applicant("N2", 2, False),
            Applicant("N3", 3, False),
            Applicant("B4", 4, True),
        )

    def test_prefix_quota_can_move_boursier_to_first_call(self):
        result = prefix_quota_order(self.people, Fraction(1, 4))
        self.assertEqual([p.applicant_id for p in result], ["B4", "N1", "N2", "N3"])

    def test_prefix_minimum_holds_until_scholar_pool_is_exhausted(self):
        people = (
            Applicant("B3", 3, True),
            Applicant("B5", 5, True),
            Applicant("N1", 1, False),
            Applicant("N2", 2, False),
            Applicant("N4", 4, False),
        )
        rate = Fraction(2, 5)
        order = prefix_quota_order(people, rate)
        seen_scholars = 0
        for k, person in enumerate(order, start=1):
            seen_scholars += person.scholarship_holder
            scholars_remain = any(p.scholarship_holder for p in order[k:])
            if scholars_remain:
                self.assertGreaterEqual(seen_scholars, -(-(rate * k).numerator // (rate * k).denominator))

    def test_zero_rate_preserves_educational_priority(self):
        result = prefix_quota_order(self.people, 0)
        self.assertEqual([p.applicant_id for p in result], ["N1", "N2", "N3", "B4"])


class ReserveChoiceTests(unittest.TestCase):
    def setUp(self):
        self.people = (
            Applicant("N1", 1, False),
            Applicant("N2", 2, False),
            Applicant("N3", 3, False),
            Applicant("B4", 4, True),
        )

    def test_reserve_returns_a_set_not_a_rewritten_call_order(self):
        selected = choose_with_scholarship_reserve(self.people, capacity=4, rate=Fraction(1, 4))
        self.assertEqual([p.applicant_id for p in selected], ["N1", "N2", "N3", "B4"])
        self.assertEqual({p.applicant_id for p in selected}, {p.applicant_id for p in self.people})

    def test_reserved_places_are_filled_by_best_scholars(self):
        selected = choose_with_scholarship_reserve(self.people, capacity=2, rate=Fraction(1, 2))
        self.assertEqual([p.applicant_id for p in selected], ["N1", "B4"])

    def test_unused_reserve_is_released(self):
        applicants = (Applicant("N1", 1, False), Applicant("N2", 2, False))
        selected = choose_with_scholarship_reserve(applicants, capacity=3, rate=Fraction(2, 3))
        self.assertEqual([p.applicant_id for p in selected], ["N1", "N2"])

    def test_rate_is_rounded_up_as_in_the_documented_rule(self):
        applicants = (
            Applicant("B2", 2, True),
            Applicant("N1", 1, False),
        )
        selected = choose_with_scholarship_reserve(applicants, capacity=1, rate=Fraction(1, 100))
        self.assertEqual([p.applicant_id for p in selected], ["B2"])

    def test_capacity_and_reserve_bounds(self):
        for capacity in range(7):
            for rate in (Fraction(0), Fraction(1, 4), Fraction(1, 2), Fraction(1)):
                for n in range(7):
                    people = tuple(
                        Applicant(f"A{i}", i + 1, i % 2 == 0)
                        for i in range(n)
                    )
                    selected = choose_with_scholarship_reserve(people, capacity, rate)
                    self.assertLessEqual(len(selected), capacity)
                    self.assertEqual(len(selected), min(capacity, len(people)))
                    self.assertTrue(set(selected).issubset(set(people)))
                    reserve = -(-(capacity * rate).numerator // (capacity * rate).denominator)
                    self.assertGreaterEqual(
                        sum(p.scholarship_holder for p in selected),
                        min(reserve, sum(p.scholarship_holder for p in people)),
                    )

    def test_choice_satisfies_substitutability_on_all_small_subsets(self):
        """Vérification exhaustive finie, distincte d'une preuve formelle générale."""
        universe = tuple(
            Applicant(f"A{i}", i + 1, i in {1, 3})
            for i in range(5)
        )
        for capacity in range(6):
            for rate in (Fraction(0), Fraction(1, 5), Fraction(2, 5), Fraction(1)):
                for mask in range(1 << len(universe)):
                    subset = tuple(universe[i] for i in range(len(universe)) if mask & (1 << i))
                    chosen = set(choose_with_scholarship_reserve(subset, capacity, rate))
                    for removed in subset:
                        if removed not in chosen:
                            continue
                        reduced = tuple(p for p in subset if p != removed)
                        # Removing another applicant must not cause a previously
                        # selected applicant to be rejected.
                        for other in subset:
                            if other == removed:
                                continue
                            if other in chosen:
                                reduced_choice = set(choose_with_scholarship_reserve(reduced, capacity, rate))
                                self.assertIn(other, reduced_choice)


class InputValidationTests(unittest.TestCase):
    def test_rejects_duplicate_ranks(self):
        with self.assertRaises(ValueError):
            prefix_quota_order((Applicant("A", 1, True), Applicant("B", 1, False)), 0.2)

    def test_rejects_rate_outside_unit_interval(self):
        with self.assertRaises(ValueError):
            choose_with_scholarship_reserve((), 2, 1.1)

    def test_rejects_negative_capacity(self):
        with self.assertRaises(ValueError):
            choose_with_scholarship_reserve((), -1, 0.2)


if __name__ == "__main__":
    unittest.main()
