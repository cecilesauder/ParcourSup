from __future__ import annotations

import unittest
from pathlib import Path

from parcoursup_prototype.progressive_ips import (
    FictionalCandidate,
    read_fictional_candidates,
    simulate_progressive_ips,
)

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "examples" / "fixtures" / "fictional_candidates.csv"
DEFAULT_WEIGHTS = (0, 0.1, 0.2, 0.3, 0.4)


class ProgressiveIPSSimulationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.candidates = read_fictional_candidates(FIXTURE)

    def test_fixture_is_fixed_fictional_and_does_not_use_real_uai(self) -> None:
        self.assertEqual(len(self.candidates), 12)
        self.assertTrue(all("fictif" in person.origin_school.lower() for person in self.candidates))

    def test_zero_weight_preserves_merit_order_and_top_k(self) -> None:
        simulation = simulate_progressive_ips(self.candidates, DEFAULT_WEIGHTS, capacity=6)
        baseline = simulation.summaries[0]
        self.assertEqual(baseline.weight, 0)
        self.assertEqual(baseline.selected_candidate_ids,
                         ("F07", "F04", "F10", "F01", "F05", "F08"))
        self.assertEqual(baseline.places_changed_from_baseline, 0)
        self.assertEqual(baseline.candidates_moved_in_rank, 0)

    def test_increasing_weight_changes_only_the_separate_illustrative_order(self) -> None:
        simulation = simulate_progressive_ips(self.candidates, DEFAULT_WEIGHTS, capacity=6)
        summaries = simulation.summaries
        self.assertEqual(tuple(item.weight for item in summaries), DEFAULT_WEIGHTS)
        self.assertTrue(any(item.places_changed_from_baseline > 0 for item in summaries[1:]))
        self.assertEqual(len(simulation.rankings), len(self.candidates) * len(DEFAULT_WEIGHTS))
        for weight in DEFAULT_WEIGHTS:
            rows = [row for row in simulation.rankings if row.weight == weight]
            self.assertEqual(sorted(row.rank for row in rows), list(range(1, 13)))
            self.assertEqual(sum(row.in_top_k for row in rows), 6)

    def test_low_ips_context_can_overtake_higher_merit_only_at_large_weight(self) -> None:
        candidates = (
            FictionalCandidate("HIGH", 95, "Lycée fictif favorisé", 140),
            FictionalCandidate("LOW", 90, "Lycée fictif moins favorisé", 70),
        )
        simulation = simulate_progressive_ips(candidates, (0, 0.4, 0.6, 1), capacity=1)
        selected = [item.selected_candidate_ids[0] for item in simulation.summaries]
        self.assertEqual(selected, ["HIGH", "HIGH", "LOW", "LOW"])

    def test_invalid_weights_are_rejected(self) -> None:
        for weights in ((), (0.1, 0.2), (0, 0.2, 0.1), (0, 1.1), (False, 0.5)):
            with self.subTest(weights=weights), self.assertRaises(ValueError):
                simulate_progressive_ips(self.candidates, weights, capacity=6)

    def test_invalid_capacity_and_duplicate_ids_are_rejected(self) -> None:
        with self.assertRaises(ValueError):
            simulate_progressive_ips(self.candidates, DEFAULT_WEIGHTS, capacity=0)
        duplicate = (self.candidates[0], self.candidates[0])
        with self.assertRaisesRegex(ValueError, "uniques"):
            simulate_progressive_ips(duplicate, (0, 0.5), capacity=1)

    def test_social_priority_is_based_on_school_context_not_candidate_ips(self) -> None:
        simulation = simulate_progressive_ips(self.candidates, (0, 0.5), capacity=6)
        at_half = [row for row in simulation.rankings if row.weight == 0.5]
        by_id = {row.candidate_id: row for row in at_half}
        self.assertEqual(by_id["F01"].social_priority, by_id["F02"].social_priority)
        self.assertEqual(by_id["F01"].school_context_ips, 80.0)
        self.assertFalse(hasattr(self.candidates[0], "applicant_ips"))


if __name__ == "__main__":
    unittest.main()
