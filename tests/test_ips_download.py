from __future__ import annotations

import csv
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from urllib.parse import parse_qs, urlparse

from scripts.telecharger_ips import FIELDS, fetch_records, save_records


def _row(uai: str) -> dict[str, str]:
    row = {field: "" for field in FIELDS}
    row.update({
        "rentree_scolaire": "2025-2026",
        "uai": uai,
        "secteur": "public",
        "type_de_lycee": "LEGT",
        "ips_etab": "100.0",
    })
    return row


class IPSSnapshotDownloaderTests(unittest.TestCase):
    def test_fetches_all_pages_and_keeps_only_requested_year(self) -> None:
        pages = [
            {"total_count": 2, "results": [_row("0010001A")]},
            {"total_count": 2, "results": [_row("0010002B")]},
        ]
        responses = [
            io.BytesIO(json.dumps(page).encode("utf-8")) for page in pages
        ]
        with patch("scripts.telecharger_ips.urlopen", side_effect=responses) as mocked:
            records = fetch_records("2025-2026")
        self.assertEqual([row["uai"] for row in records], ["0010001A", "0010002B"])
        self.assertEqual(mocked.call_count, 2)
        query_offsets = [
            parse_qs(urlparse(call.args[0].full_url).query)["offset"][0]
            for call in mocked.call_args_list
        ]
        self.assertEqual(query_offsets, ["0", "1"])

    def test_rejects_invalid_year_before_network_access(self) -> None:
        with patch("scripts.telecharger_ips.urlopen") as mocked:
            with self.assertRaisesRegex(ValueError, "AAAA-AAAA"):
                fetch_records("2026")
        mocked.assert_not_called()

    def test_saves_selected_fields_as_semicolon_csv(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "snapshot.csv"
            save_records([_row("0010001A")], output)
            with output.open(encoding="utf-8", newline="") as handle:
                reader = csv.DictReader(handle, delimiter=";")
                rows = list(reader)
            self.assertEqual(reader.fieldnames, list(FIELDS))
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]["uai"], "0010001A")
            self.assertEqual(rows[0]["ips_etab"], "100.0")


if __name__ == "__main__":
    unittest.main()
