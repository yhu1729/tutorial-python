"""Save a labeled plot of an analytic damped oscillation without a GUI."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


def main():
    time_s = np.linspace(0.0, 10.0, 101)
    decay_rate_s_inv = 0.2
    angular_frequency_rad_s = 2.0
    envelope = np.exp(-decay_rate_s_inv * time_s)
    amplitude = envelope * np.cos(angular_frequency_rad_s * time_s)

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(time_s, amplitude, label="Damped oscillation")
    ax.plot(time_s, envelope, linestyle="--", label="Positive envelope")
    ax.scatter(time_s[::10], amplitude[::10], label="Every tenth sample", s=20)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Normalized amplitude (dimensionless)")
    ax.set_title("Analytic damped oscillation")
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()

    output_dir = Path(__file__).resolve().parents[2] / "output" / "09-plot"
    output_dir.mkdir(parents=True, exist_ok=True)
    destination = output_dir / "oscillation.png"
    fig.savefig(destination, dpi=150)
    plt.close(fig)
    print("Samples:", time_s.size)
    print("Saved:", destination)


if __name__ == "__main__":
    main()
