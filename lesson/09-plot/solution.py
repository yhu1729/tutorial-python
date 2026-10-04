"""Worked solutions: physical axes, semilog decay, and model comparison."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


def save_figure(fig, destination):
    """Use the same output and lifetime policy for all three exercises."""
    fig.tight_layout()
    fig.savefig(destination, dpi=150)
    plt.close(fig)
    print("Saved:", destination)


def main():
    output_dir = Path(__file__).resolve().parents[2] / "output" / "09-plot"
    output_dir.mkdir(parents=True, exist_ok=True)

    time_s = np.array([0, 1, 2, 3], dtype=float)
    distance_m = np.array([0, 3, 6, 9], dtype=float)
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(time_s, distance_m, marker="o")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Distance (m)")
    ax.set_title("Constant-speed motion: 3 m/s")
    ax.grid(True, alpha=0.3)
    # Connecting samples here agrees with the stated constant-speed model.
    save_figure(fig, output_dir / "motion.png")

    time_s = np.linspace(0.0, 50.0, 101)
    normalized_amount = np.exp(-0.1 * time_s)
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(time_s, normalized_amount)
    ax.set_yscale("log")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Normalized amount (dimensionless, log scale)")
    ax.set_title("Exponential decay: rate = 0.1 /s")
    ax.grid(True, which="both", alpha=0.3)
    # ln(amount) = -0.1 * time_s; base-10 log has slope -0.1 / ln(10).
    save_figure(fig, output_dir / "decay.png")

    time_s = np.linspace(0.0, 10.0, 101)
    fig, ax = plt.subplots(figsize=(7, 4))
    for rate_s_inv in [0.1, 0.3]:
        ax.plot(time_s, np.exp(-rate_s_inv * time_s), label=f"Rate {rate_s_inv} /s")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Normalized amount (dimensionless)")
    ax.set_title("Two analytic decay models")
    ax.legend()
    ax.grid(True, alpha=0.3)
    save_figure(fig, output_dir / "rate.png")


if __name__ == "__main__":
    main()
