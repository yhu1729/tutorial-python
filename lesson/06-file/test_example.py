"""Reader contract checks; unittest is introduced in lesson 7."""

import csv
import tempfile
import unittest
from pathlib import Path

from example import read_measurement_list


class MeasurementReaderTest(unittest.TestCase):
    def read_text(self, text):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "measurement.csv"
            path.write_text(text, encoding="utf-8")
            return read_measurement_list(path)

    def test_valid_numeric_data(self):
        self.assertEqual(
            self.read_text("time_s,position_m\n0,1\n1,3\n"),
            [(0.0, 1.0), (1.0, 3.0)],
        )

    def test_valid_quoted_numeric_field(self):
        self.assertEqual(
            self.read_text('"time_s","position_m"\n"0","1"\n"1","3"\n'),
            [(0.0, 1.0), (1.0, 3.0)],
        )

    def test_unterminated_header(self):
        with self.assertRaisesRegex(ValueError, "header.*malformed CSV") as caught:
            self.read_text('time_s,"position_m\n0,1\n')
        self.assertIsInstance(caught.exception.__cause__, csv.Error)

    def test_unterminated_field(self):
        with self.assertRaisesRegex(ValueError, "after line 1: malformed CSV") as caught:
            self.read_text('time_s,position_m\n0,"1\n')
        self.assertIsInstance(caught.exception.__cause__, csv.Error)

    def test_invalid_closing_quote(self):
        with self.assertRaisesRegex(ValueError, "after line 2: malformed CSV") as caught:
            self.read_text('time_s,position_m\n0,1\n0,"1"x\n')
        self.assertIsInstance(caught.exception.__cause__, csv.Error)

    def test_missing_column(self):
        with self.assertRaisesRegex(ValueError, "header"):
            self.read_text("time_s\n0\n")

    def test_header_must_match_exactly_and_in_order(self):
        for header in ["position_m,time_s", "time_s,position_m,note",
                       "time_s,time_s", "Time_s,position_m"]:
            with self.subTest(header=header):
                with self.assertRaisesRegex(ValueError, "header.*got"):
                    self.read_text(f"{header}\n0,1\n")

    def test_show_byte_order_mark_in_header_error(self):
        with self.assertRaisesRegex(ValueError, r"got \['\\ufefftime_s'"):
            self.read_text("\ufefftime_s,position_m\n0,1\n")

    def test_malformed_number(self):
        with self.assertRaisesRegex(ValueError, "line 2: expected numeric"):
            self.read_text("time_s,position_m\n0,broken\n")

    def test_count_blank_line_in_line_number(self):
        self.assertEqual(
            self.read_text("time_s,position_m\n0,1\n\n1,3\n"),
            [(0.0, 1.0), (1.0, 3.0)],
        )
        with self.assertRaisesRegex(ValueError, "line 4: expected numeric"):
            self.read_text("time_s,position_m\n0,1\n\n2,bad\n")

    def test_header_only(self):
        with self.assertRaisesRegex(ValueError, "at least one"):
            self.read_text("time_s,position_m\n")

    def test_empty_file(self):
        with self.assertRaisesRegex(ValueError, "header"):
            self.read_text("")

    def test_nonfinite_value(self):
        for row in ["nan,1", "0,inf", "-inf,1", "0,nan"]:
            with self.subTest(row=row):
                with self.assertRaisesRegex(ValueError, "finite"):
                    self.read_text(f"time_s,position_m\n{row}\n")

    def test_wrong_row_width(self):
        for row in ["0", "0,1,2"]:
            with self.subTest(row=row):
                with self.assertRaisesRegex(ValueError, "two fields"):
                    self.read_text(f"time_s,position_m\n{row}\n")


if __name__ == "__main__":
    unittest.main()
