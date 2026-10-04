"""Worked solutions using the reader from example.py."""

import csv
from pathlib import Path

from example import read_measurement_list


def main():
    lesson_directory = Path(__file__).resolve().parent
    project_directory = Path(__file__).resolve().parents[2]
    measurement_list = read_measurement_list(lesson_directory / "input" / "measurement.csv")

    # Exercise 1: calculate the mean from the numeric values.
    total_m = 0.0
    for time_s, position_m in measurement_list:
        total_m += position_m
    print(f"Mean position: {total_m / len(measurement_list):.3f} m")

    # Exercise 2: save a conversion, preserving the original input data.
    output_path = project_directory / "output" / "06-file" / "position_cm.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(["time_s", "position_cm"])
        for time_s, position_m in measurement_list:
            writer.writerow([f"{time_s:.1f}", f"{100.0 * position_m:.1f}"])
    print("Saved output/06-file/position_cm.csv")

    # Exercise 3: select values, using an ordinary loop and condition.
    for time_s, position_m in measurement_list:
        if position_m > 5.0:
            print(f"Above 5 m: t={time_s:.1f} s, x={position_m:.1f} m")


if __name__ == "__main__":
    main()
