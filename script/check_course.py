"""Verify the course in a disposable copy, without changing user output."""

import csv
import difflib
import math
import os
from pathlib import Path
import re
import shlex
import shutil
import subprocess
import sys
import tempfile


LESSON_SEQUENCE = (
    "01-run-python", "02-value-expression", "03-control-flow",
    "04-collection", "05-function", "06-file", "07-debug",
    "08-numpy", "09-plot", "10-numerical-error", "11-linear-algebra",
    "12-cool",
)
TEST_LESSON_SEQUENCE = (
    "06-file", "07-debug", "10-numerical-error", "11-linear-algebra",
    "12-cool",
)
WRITER_LESSON_SEQUENCE = ("06-file", "09-plot", "12-cool")
ARTIFACT_MAP = {
    ("06-file", "example.py"): ("summary.csv",),
    ("06-file", "solution.py"): ("position_cm.csv",),
    ("09-plot", "example.py"): ("oscillation.png",),
    ("09-plot", "solution.py"): ("motion.png", "decay.png", "rate.png"),
    ("12-cool", "example.py"): ("temperature.csv", "temperature.png"),
    ("12-cool", "solution.py"): (),
}
TEST_PROGRAM = """
import sys
import unittest

suite = unittest.defaultTestLoader.discover(sys.argv[1], pattern=sys.argv[2])
if suite.countTestCases() == 0:
    raise SystemExit("No tests discovered")
result = unittest.TextTestRunner(verbosity=2).run(suite)
raise SystemExit(not result.wasSuccessful())
"""
# Decode with a dependency already used by the lessons. The checker itself
# imports only the standard library and does not depend on PNG byte layouts.
# A marker on the line directly above a ```text fence declares that the block
# is the complete standard output of that script in the same lesson.
OUTPUT_MARKER = re.compile(r"<!-- check-output: (\S+) -->")
DOCUMENT_SEQUENCE = ("README.md", "exercise.md")
SCRIPT_SEQUENCE = ("example.py", "solution.py")
PROJECT_PLACEHOLDER = "<project-root>"
PNG_PROGRAM = """
import sys
import matplotlib.image
import numpy as np

pixel_array = matplotlib.image.imread(sys.argv[1])
if pixel_array.ndim not in (2, 3) or min(pixel_array.shape[:2]) <= 0:
    raise SystemExit("PNG has invalid dimensions")
if not np.all(np.isfinite(pixel_array)):
    raise SystemExit("PNG has nonfinite pixels")
"""


class CheckFailure(Exception):
    """A course contract failed, with enough context to reproduce it."""


def preflight(project):
    """Require the fixed course inventory before starting subprocesses."""
    lesson_root = project / "lesson"
    if not lesson_root.is_dir():
        raise CheckFailure(f"Missing lesson directory: {lesson_root}")
    actual = {path.name for path in lesson_root.iterdir()
              if path.is_dir() and path.name != "__pycache__"}
    if actual != set(LESSON_SEQUENCE):
        missing = sorted(set(LESSON_SEQUENCE) - actual)
        unexpected = sorted(actual - set(LESSON_SEQUENCE))
        raise CheckFailure(
            f"Lesson inventory mismatch: missing={missing}, unexpected={unexpected}"
        )
    for lesson in LESSON_SEQUENCE:
        required = ["README.md", "exercise.md", "example.py", "solution.py"]
        if lesson in TEST_LESSON_SEQUENCE:
            required.append("test_example.py")
        if lesson == "06-file":
            required.extend(["input/measurement.csv", "input/README.md"])
        for filename in required:
            path = lesson_root / lesson / filename
            if not path.is_file():
                raise CheckFailure(f"{lesson}: missing required file {filename}")


def run_command(label, command, cwd, environment, timeout=60):
    """Return the completed process; show child logs only on failure."""
    print(f"Checking {label}", flush=True)
    rendered = shlex.join(str(argument) for argument in command)
    try:
        result = subprocess.run(
            command, cwd=cwd, env=environment, capture_output=True, text=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired as error:
        # TimeoutExpired may contain bytes even when text=True.
        log_list = []
        for output in (error.stdout, error.stderr):
            if output:
                log_list.append(output.decode(errors="replace")
                                if isinstance(output, bytes) else output)
        raise CheckFailure(
            f"{label}: timed out after {timeout} seconds\n"
            f"Command: {rendered}\n{''.join(log_list)}"
        ) from error
    except OSError as error:
        raise CheckFailure(
            f"{label}: could not run command: {error}\nCommand: {rendered}"
        ) from error
    if result.returncode != 0:
        raise CheckFailure(
            f"{label}: exited with status {result.returncode}\n"
            f"Command: {rendered}\n{result.stdout}{result.stderr}"
        )
    return result


def read_csv(path, header):
    with path.open(encoding="utf-8", newline="") as stream:
        row_list = list(csv.reader(stream, strict=True))
    if not row_list or row_list[0] != header:
        raise ValueError(f"expected CSV header {header}")
    return row_list[1:]


def check_csv(path):
    if path.name == "summary.csv":
        row_list = read_csv(path, ["count", "mean_position_m"])
        if row_list != [["5", "5.000"]]:
            raise ValueError("expected five samples with mean position 5.000 m")
    elif path.name == "position_cm.csv":
        row_list = read_csv(path, ["time_s", "position_cm"])
        expected = [[f"{index:.1f}", f"{100 * (2 * index + 1):.1f}"]
                    for index in range(5)]
        if row_list != expected:
            raise ValueError("unexpected converted measurements")
    elif path.name == "temperature.csv":
        row_list = read_csv(
            path, ["time_min", "euler_C", "analytic_C", "absolute_error_C"]
        )
        if len(row_list) != 41 or any(len(row) != 4 for row in row_list):
            raise ValueError("expected 41 cooling rows with four fields each")
        value_list = [[float(field) for field in row] for row in row_list]
        if not all(math.isfinite(value) for row in value_list for value in row):
            raise ValueError("cooling values must be finite")
        if value_list[0] != [0.0, 80.0, 80.0, 0.0] or value_list[-1][0] != 10.0:
            raise ValueError("unexpected cooling endpoints or initial error")


def check_artifact(project, lesson, script, cwd, environment):
    command = [sys.executable, str(project / "lesson" / lesson / script)]
    for filename in ARTIFACT_MAP.get((lesson, script), ()):
        path = project / "output" / lesson / filename
        try:
            if not path.is_file():
                raise ValueError("missing generated file")
            if path.suffix == ".csv":
                check_csv(path)
            else:
                run_command(
                    f"{lesson}/{script}: decode {filename}",
                    [sys.executable, "-c", PNG_PROGRAM, str(path)],
                    cwd, environment,
                )
        except (OSError, ValueError, csv.Error) as error:
            raise CheckFailure(
                f"{lesson}/{script}: invalid artifact {filename}: {error}\n"
                f"Command: {shlex.join(command)}"
            ) from error


def clear_artifact(project):
    """A second pass must recreate output rather than pass on stale files."""
    for (lesson, _), filename_sequence in ARTIFACT_MAP.items():
        for filename in filename_sequence:
            (project / "output" / lesson / filename).unlink(missing_ok=True)


def extract_output_block(path):
    """Return {script: (line, text)} for each marked ```text block."""
    line_list = path.read_text(encoding="utf-8").splitlines()
    block_map = {}
    for index, line in enumerate(line_list):
        if "check-output" not in line:
            continue
        match = OUTPUT_MARKER.fullmatch(line.strip())
        if match is None:
            raise ValueError(f"line {index + 1}: malformed output marker")
        script = match.group(1)
        if script not in SCRIPT_SEQUENCE:
            raise ValueError(f"line {index + 1}: unknown script {script}")
        if script in block_map:
            raise ValueError(f"line {index + 1}: duplicate marker for {script}")
        if index + 1 >= len(line_list) or line_list[index + 1] != "```text":
            raise ValueError(f"line {index + 1}: marker must directly precede ```text")
        try:
            end = line_list.index("```", index + 2)
        except ValueError:
            raise ValueError(f"line {index + 2}: unterminated ```text block") from None
        block_map[script] = (index + 2, "\n".join(line_list[index + 2:end]))
    return block_map


def normalize_output(text, project):
    """Hide the scratch location and differences invisible in Markdown."""
    text = text.replace("\r\n", "\n").replace(str(project), PROJECT_PLACEHOLDER)
    return [line.rstrip() for line in text.rstrip("\n").split("\n")]


def check_documented_output(project, output_map):
    """Compare marked documentation blocks with captured script output."""
    count = 0
    for lesson in LESSON_SEQUENCE:
        for document in DOCUMENT_SEQUENCE:
            try:
                block_map = extract_output_block(project / "lesson" / lesson / document)
            except ValueError as error:
                raise CheckFailure(f"{lesson}/{document}: {error}") from error
            for script, (line, documented) in block_map.items():
                expected = normalize_output(documented, project)
                actual = normalize_output(output_map[(lesson, script)], project)
                if actual != expected:
                    diff = "\n".join(difflib.unified_diff(
                        expected, actual, f"{lesson}/{document}", f"{script} stdout",
                        lineterm="",
                    ))
                    raise CheckFailure(
                        f"{lesson}/{document}:{line}: documented output differs "
                        f"from {script}\n{diff}"
                    )
                count += 1
    return count


def check_input_unchanged(path, original):
    if path.read_bytes() != original:
        raise CheckFailure("06-file: input measurement.csv was modified")


def check_course(project):
    preflight(project)
    with tempfile.TemporaryDirectory(prefix="tutorial-python-check-") as directory:
        # Scripts print resolved paths; macOS temporary folders are symlinked.
        scratch = Path(directory).resolve()
        shutil.copytree(
            project / "lesson", scratch / "lesson",
            ignore=shutil.ignore_patterns("__pycache__"),
        )
        # Run checker regressions separately from lesson discovery: several
        # lessons intentionally have modules with the same local name.
        shutil.copytree(
            project / "script", scratch / "script",
            ignore=shutil.ignore_patterns("__pycache__"),
        )
        environment = os.environ.copy()
        environment.update({
            "PYTHONDONTWRITEBYTECODE": "1",
            "MPLCONFIGDIR": str(scratch / ".matplotlib"),
            "XDG_CACHE_HOME": str(scratch / ".cache"),
        })
        input_path = scratch / "lesson" / "06-file" / "input" / "measurement.csv"
        original_input = input_path.read_bytes()
        run_command(
            "course checker tests",
            [sys.executable, "-c", TEST_PROGRAM, str(scratch / "script"),
             "test_check_course.py"],
            scratch, environment,
        )
        for lesson in TEST_LESSON_SEQUENCE:
            run_command(
                f"{lesson} tests",
                [sys.executable, "-c", TEST_PROGRAM,
                 str(scratch / "lesson" / lesson), "test_example.py"],
                scratch, environment,
            )
        output_map = {}
        for lesson in LESSON_SEQUENCE:
            for script in SCRIPT_SEQUENCE:
                output_map[(lesson, script)] = run_command(
                    f"{lesson}/{script}",
                    [sys.executable, str(scratch / "lesson" / lesson / script)],
                    scratch, environment,
                ).stdout
                check_artifact(scratch, lesson, script, scratch, environment)
        check_input_unchanged(input_path, original_input)
        print("Checking documented output", flush=True)
        documented = check_documented_output(scratch, output_map)
        clear_artifact(scratch)
        foreign_cwd = scratch / "other-working-directory"
        foreign_cwd.mkdir()
        for lesson in WRITER_LESSON_SEQUENCE:
            for script in SCRIPT_SEQUENCE:
                run_command(
                    f"{lesson}/{script} from another working directory",
                    [sys.executable, str(scratch / "lesson" / lesson / script)],
                    foreign_cwd, environment,
                )
                check_artifact(scratch, lesson, script, foreign_cwd, environment)
        check_input_unchanged(input_path, original_input)
    print("Course verification passed: 12 lessons, 24 scripts, 8 artifacts, "
          f"{documented} documented outputs, and 6 working-directory checks.")


def main():
    try:
        check_course(Path(__file__).resolve().parents[1])
    except (CheckFailure, OSError) as error:
        print(f"Course verification failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
