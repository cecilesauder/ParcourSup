from __future__ import annotations

import csv
import tempfile
import unittest
from pathlib import Path

from parcoursup_prototype.ips_audit import (
    CSV_FIELDS,
    audit_ips,
    read_ips_records,
)
from parcoursup_prototype.order_call import Applicant, order_call_with_quotas

ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT = ROOT / "data" / "ips_lycees_2025-2026.csv"


class OfficialIPSSnapshotTests(unittest.TestCase):
    def test_real_snapshot_has_the_expected_year_and_school_count(self) -> None:
        records = read_ips_records(SNAPSHOT, rentree_scolaire="2025-2026")
        audit = audit_ips(records)
        self.assertEqual(audit["establishments"], 3662)
        self.assertEqual(audit["unique_uai"], 3662)
        self.assertEqual(audit["rentree_scolaire"], "2025-2026")
        self.assertEqual(audit["indicators"]["ips_etab"]["available"], 3661)
        self.assertEqual(audit["indicators"]["ips_etab"]["missing"], 1)

    def test_real_snapshot_describes_schools_not_individual_candidates(self) -> None:
        audit = audit_ips(read_ips_records(SNAPSHOT, "2025-2026"))
        self.assertEqual(audit["indicators"]["ips_etab"]["statistics"]["median"], 106.6)
        self.assertEqual(audit["interpretation"],
                         "Statistiques non pondérées par établissement; pas des résultats d'admission.")
        self.assertEqual(audit["ips_etab_by_sector"]["public"]["establishments"], 2424)
        self.assertEqual(audit["ips_etab_by_sector"]["privé sous contrat"]["establishments"], 1238)

    def test_school_context_audit_does_not_change_the_order_call(self) -> None:
        people = (
            Applicant("A", 1, False, False),
            Applicant("B", 2, True, False),
            Applicant("C", 3, False, True),
            Applicant("D", 4, True, True),
        )
        before = order_call_with_quotas(people, scholarship_rate="0.25", sector_rate="0.25")
        audit_ips(read_ips_records(SNAPSHOT, "2025-2026"))
        after = order_call_with_quotas(people, scholarship_rate="0.25", sector_rate="0.25")
        self.assertEqual(before, after)


class IPSCSVValidationTests(unittest.TestCase):
    def _write_csv(self, rows: list[dict[str, str]]) -> Path:
        handle = tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", newline="", suffix=".csv", delete=False
        )
        path = Path(handle.name)
        with handle:
            writer = csv.DictWriter(handle, fieldnames=CSV_FIELDS, delimiter=";")
            writer.writeheader()
            writer.writerows(rows)
        self.addCleanup(path.unlink, missing_ok=True)
        return path

    def _row(self, year: str, uai: str, sector: str, school_type: str,
             ips: str, ips_gt: str = "", ips_pro: str = "") -> dict[str, str]:
        return {
            "rentree_scolaire": year,
            "uai": uai,
            "secteur": sector,
            "type_de_lycee": school_type,
            "ips_etab": ips,
            "ips_voie_gt": ips_gt,
            "ips_voie_pro": ips_pro,
            "ips_post_bac": "",
            "ecart_type_etablissement": "20.0",
            "ecart_type_voie_gt": "",
            "ecart_type_voie_pro": "",
        }

    def test_filters_year_and_preserves_absence_as_none(self) -> None:
        path = self._write_csv([
            self._row("2024-2025", "0010001A", "public", "LEGT", "99.0"),
            self._row("2025-2026", "0010002B", "public", "LP", ""),
        ])
        records = read_ips_records(path, "2025-2026")
        self.assertEqual(len(records), 1)
        self.assertIsNone(records[0].ips_etab)

    def test_detects_duplicate_uai_in_one_year(self) -> None:
        row = self._row("2025-2026", "0010001A", "public", "LEGT", "99.0")
        path = self._write_csv([row, row])
        with self.assertRaisesRegex(ValueError, "dupliqué"):
            read_ips_records(path)

    def test_rejects_non_numeric_ips_instead_of_silently_dropping_it(self) -> None:
        path = self._write_csv([
            self._row("2025-2026", "0010001A", "public", "LEGT", "inconnu")
        ])
        with self.assertRaisesRegex(ValueError, "invalide"):
            read_ips_records(path)

    def test_distribution_is_unweighted_and_grouped_by_school(self) -> None:
        path = self._write_csv([
            self._row("2025-2026", "0010001A", "public", "LEGT", "80.0"),
            self._row("2025-2026", "0010002B", "public", "LEGT", "100.0"),
            self._row("2025-2026", "0010003C", "privé sous contrat", "LP", "120.0"),
        ])
        audit = audit_ips(read_ips_records(path))
        all_ips = audit["indicators"]["ips_etab"]["statistics"]
        self.assertEqual(all_ips["count"], 3)
        self.assertEqual(all_ips["mean"], 100.0)
        self.assertEqual(all_ips["median"], 100.0)
        self.assertEqual(audit["ips_etab_by_sector"]["public"]["establishments"], 2)
        self.assertEqual(audit["ips_etab_by_school_type"]["LP"]["establishments"], 1)


if __name__ == "__main__":
    unittest.main()
