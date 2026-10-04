"""Read a synthetic experiment and save a deterministic summary."""

import csv
import math
from pathlib import Path


def read_measurement_list(path):
    """Return finite time/position pairs from a nonempty, two-column CSV."""
    measurement_list = []
    with path.open("r", encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream, strict=True)
        try:
            field_name_list = reader.fieldnames
        except csv.Error as error:
            raise ValueError("CSV header: malformed CSV syntax") from error
        if field_name_list != ["time_s", "position_m"]:
            raise ValueError(f"CSV header must be time_s,position_m; got {field_name_list!r}")
        try:
            for row in reader:
                # The file line where this record ends; blank lines are skipped.
                line = reader.line_num
                if None in row or None in row.values():
                    raise ValueError(f"line {line}: expected exactly two fields")
                try:
                    time_s = float(row["time_s"])
                    position_m = float(row["position_m"])
                except ValueError as error:
                    raise ValueError(f"line {line}: expected numeric values") from error
                if not math.isfinite(time_s) or not math.isfinite(position_m):
                    raise ValueError(f"line {line}: values must be finite")
                measurement_list.append((time_s, position_m))
        except csv.Error as error:
            # line_num still counts the last record that parsed successfully.
            raise ValueError(
                f"CSV data after line {reader.line_num}: malformed CSV syntax"
            ) from error
    if not measurement_list:
        raise ValueError("CSV must contain at least one measurement")
    return measurement_list


def write_summary(path, measurement_list):
    """Save sample count and mean position, creating the output folder."""
    total_m = 0.0
    for time_s, position_m in measurement_list:
        total_m += position_m
    mean_m = total_m / len(measurement_list)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(["count", "mean_position_m"])
        writer.writerow([len(measurement_list), f"{mean_m:.3f}"])


def main():
    lesson_directory = Path(__file__).resolve().parent
    project_directory = Path(__file__).resolve().parents[2]
    measurement_list = read_measurement_list(lesson_directory / "input" / "measurement.csv")
    output_path = project_directory / "output" / "06-file" / "summary.csv"
    write_summary(output_path, measurement_list)
    print(f"Read {len(measurement_list)} measurements")
    for time_s, position_m in measurement_list:
        print(f"t={time_s:.1f} s, x={position_m:.1f} m")
    print("Saved output/06-file/summary.csv")


if __name__ == "__main__":
    main()
