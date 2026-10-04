"""Regression checks for verification failures, without running the course."""

import csv
import os
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

from check_course import (
    ARTIFACT_MAP, CheckFailure, LESSON_SEQUENCE, SCRIPT_SEQUENCE,
    TEST_LESSON_SEQUENCE, TEST_PROGRAM,
    check_artifact, check_csv, check_documented_output, check_input_unchanged,
    clear_artifact, preflight, run_command,
)


class CourseCheckerTest(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.environment = os.environ.copy()
        self.environment["PYTHONDONTWRITEBYTECODE"] = "1"

    def make_inventory(self):
        for lesson in LESSON_SEQUENCE:
            path = self.root / "lesson" / lesson
            path.mkdir(parents=True)
            for filename in ("README.md", "exercise.md", "example.py", "solution.py"):
                (path / filename).touch()
            if lesson in TEST_LESSON_SEQUENCE:
                (path / "test_example.py").touch()
        input_directory = self.root / "lesson" / "06-file" / "input"
        input_directory.mkdir()
        (input_directory / "measurement.csv").touch()
        (input_directory / "README.md").touch()

    def test_missing_required_file(self):
        self.make_inventory()
        (self.root / "lesson" / "01-run-python" / "example.py").unlink()
        with self.assertRaisesRegex(CheckFailure, "01-run-python.*example.py"):
            preflight(self.root)

    def test_missing_expected_test_suite(self):
        self.make_inventory()
        (self.root / "lesson" / "06-file" / "test_example.py").unlink()
        with self.assertRaisesRegex(CheckFailure, "06-file.*test_example.py"):
            preflight(self.root)

    def test_reject_empty_test_suite(self):
        (self.root / "test_example.py").touch()
        with self.assertRaisesRegex(CheckFailure, "No tests discovered"):
            run_command("empty suite", [sys.executable, "-c", TEST_PROGRAM,
                        str(self.root), "test_example.py"],
                        self.root, self.environment)

    def test_include_command_and_log_on_child_failure(self):
        with self.assertRaisesRegex(CheckFailure, "Command:.*") as caught:
            run_command("broken lesson", [sys.executable, "-c",
                        "print('child detail'); raise SystemExit(7)"],
                        self.root, self.environment)
        self.assertIn("broken lesson", str(caught.exception))
        self.assertIn("status 7", str(caught.exception))
        self.assertIn("child detail", str(caught.exception))

    def test_child_timeout(self):
        with self.assertRaisesRegex(CheckFailure, "timed out"):
            run_command("slow lesson", [sys.executable, "-c",
                        "import time; time.sleep(60)"],
                        self.root, self.environment, timeout=0.1)

    def test_reject_stale_artifact_on_second_run(self):
        for (lesson, _), filename_sequence in ARTIFACT_MAP.items():
            for filename in filename_sequence:
                path = self.root / "output" / lesson / filename
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("stale", encoding="utf-8")
        clear_artifact(self.root)
        with self.assertRaisesRegex(CheckFailure, "06-file/example.py.*missing"):
            check_artifact(self.root, "06-file", "example.py",
                            self.root, self.environment)
        for (lesson, _), filename_sequence in ARTIFACT_MAP.items():
            for filename in filename_sequence:
                self.assertFalse((self.root / "output" / lesson / filename).exists())

    def test_malformed_artifact_csv(self):
        path = self.root / "summary.csv"
        for content in ('count,mean_position_m\n5,"5.000\n',
                        "count,mean_position_m\n5,nan\n"):
            with self.subTest(content=content):
                path.write_text(content, encoding="utf-8")
                with self.assertRaises((ValueError, csv.Error)):
                    check_csv(path)

    def test_invalid_temperature_row(self):
        path = self.root / "temperature.csv"
        header = "time_min,euler_C,analytic_C,absolute_error_C\n"
        valid_row_list = [f"{index / 4},80,80,0\n" for index in range(41)]
        path.write_text(header + "".join(valid_row_list), encoding="utf-8")
        check_csv(path)
        for bad_row in ("0.25,nan,80,0\n", "0.25,80,80\n"):
            with self.subTest(bad_row=bad_row):
                row_list = valid_row_list.copy()
                row_list[1] = bad_row
                path.write_text(header + "".join(row_list), encoding="utf-8")
                with self.assertRaises(ValueError):
                    check_csv(path)
        path.write_text(header + "".join(valid_row_list[:-1]), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "41 cooling rows"):
            check_csv(path)

    def test_reject_unreadable_png(self):
        path = self.root / "output" / "09-plot" / "oscillation.png"
        path.parent.mkdir(parents=True)
        path.write_bytes(b"not a PNG")
        with self.assertRaisesRegex(CheckFailure, "09-plot/example.py: decode"):
            check_artifact(self.root, "09-plot", "example.py",
                            self.root, self.environment)

    def write_document(self, text, lesson="01-run-python", name="README.md"):
        shutil.rmtree(self.root / "lesson", ignore_errors=True)
        self.make_inventory()
        (self.root / "lesson" / lesson / name).write_text(text, encoding="utf-8")

    def make_output_map(self, example="", solution_output=""):
        """Captured stdout for every script; lesson 1's can be customized."""
        result = {(lesson, script): "" for lesson in LESSON_SEQUENCE
                  for script in SCRIPT_SEQUENCE}
        result[("01-run-python", "example.py")] = example
        result[("01-run-python", "solution.py")] = solution_output
        return result

    def test_match_documented_output(self):
        self.write_document("Output:\n\n<!-- check-output: example.py -->\n"
                            "```text\nfirst\nsecond  \n```\n")
        output_map = self.make_output_map(example="first\r\nsecond\n")
        self.assertEqual(check_documented_output(self.root, output_map), 1)

    def test_show_diff_for_documented_output_mismatch(self):
        self.write_document("<!-- check-output: example.py -->\n```text\nfirst\nsecond\n```\n")
        with self.assertRaisesRegex(CheckFailure, "README.md:2: documented") as caught:
            check_documented_output(self.root, self.make_output_map(example="first\nother\n"))
        self.assertIn("-second", str(caught.exception))
        self.assertIn("+other", str(caught.exception))

    def test_hide_project_root_in_documented_output(self):
        self.write_document("<!-- check-output: solution.py -->\n```text\n"
                            "Saved: <project-root>/output/plot.png\n```\n")
        output_map = self.make_output_map(
            solution_output=f"Saved: {self.root}/output/plot.png\n"
        )
        self.assertEqual(check_documented_output(self.root, output_map), 1)

    def test_invalid_output_marker(self):
        case_map = {
            "<!-- check-output: example.py -->\nText\n```text\nx\n```\n": "precede",
            "<!-- check-output: other.py -->\n```text\nx\n```\n": "unknown script",
            "<!-- check-output: example.py -->\n```text\nx\n```\n"
            "<!-- check-output: example.py -->\n```text\nx\n```\n": "duplicate",
            "<!-- check-output: example.py -->\n```text\nx\n": "unterminated",
            "<!-- check-output example.py -->\n```text\nx\n```\n": "malformed",
        }
        for text, message in case_map.items():
            with self.subTest(message=message):
                self.write_document(text, lesson="12-cool", name="exercise.md")
                with self.assertRaisesRegex(CheckFailure, f"12-cool/exercise.md:.*{message}"):
                    check_documented_output(self.root, self.make_output_map(example="x\n"))

    def test_reject_modified_input(self):
        path = self.root / "measurement.csv"
        path.write_bytes(b"modified")
        with self.assertRaisesRegex(CheckFailure, "input measurement.csv was modified"):
            check_input_unchanged(path, b"original")


if __name__ == "__main__":
    unittest.main()
