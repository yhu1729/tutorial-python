# Python for scientific computing

A self-paced course for someone new to programming who already knows scientific
mathematics. Start with small programs, then work toward arrays, plots, error
analysis, least squares, and a verified cooling simulation.

## Start here

A **terminal** is a window where you type commands. The **working directory** is
the folder those commands operate in. Open a terminal in this project's folder.
In these instructions, every command starts from that project root. Do not type
the Markdown fences (` ``` `) around commands.

If your terminal starts elsewhere, use `cd` (change directory). For example,
`cd "/path/to/tutorial-python"` selects a folder; replace the quoted path with
this project's actual location. Quotes keep spaces in a path together. `pwd`
on macOS/Linux, or `Get-Location` in Windows PowerShell, displays your current
directory. You should see this project's README and `lesson` folder there.

You need [uv](https://docs.astral.sh/uv/getting-started/installation/), which
manages both Python and the course's packages. Check that it is installed:

```sh
uv --version
```

The course targets Python 3.14, recorded in `.python-version`. If Python 3.14
is not already installed, uv downloads it during the setup below. The course's
`uv run python ...` commands work the same way on Windows, macOS, and Linux.

Set up the course's isolated environment using the committed dependency versions:

```sh
uv sync --locked
uv run python --version
uv run python lesson/01-run-python/example.py
```

`uv sync` installs Python 3.14 if needed and the packages into `.venv`, a
private environment for this project; `uv run python --version` should report
Python 3.14. It needs internet access on the first installation. `--locked` checks that the
lockfile agrees with the project configuration. `uv run` uses that environment;
there is no need to activate it manually. Python executes a `.py` file from top
to bottom. These scripts are teaching examples, not a package to install.

Lessons 1–7 import only the Python standard library (included with Python).
NumPy begins in lesson 8; lessons 9 and 12 also use Matplotlib. Lesson 10's scalar
error study uses only the standard library. The final course environment installs
both external libraries so you can work through all lessons with one setup.

## How to study

Read each lesson's README, predict the example's output, run it, then change a
value and explain the result. Type some examples yourself: syntax becomes easier
to remember when you use it. Work through `exercise.md` before opening
`solution.py`; the solutions are complete scripts with explanations. Follow
the links to the next lesson once you can explain the recap in your own words.

Programming is cumulative. A familiar equation does not make its Python syntax
familiar; revisit earlier lessons whenever needed. No time limit is assumed.

## Course index

| Lesson | Topic | Practice |
| --- | --- | --- |
| [01](lesson/01-run-python/README.md) | Running Python, variables, printing | Unit conversion |
| [02](lesson/02-value-expression/README.md) | Types, expressions, strings | Scientific formulas |
| [03](lesson/03-control-flow/README.md) | Conditions and loops | Sampling and accumulation |
| [04](lesson/04-collection/README.md) | Lists, tuples, dictionaries, mutability | Measurement records |
| [05](lesson/05-function/README.md) | Functions and modules | Reusable calculations |
| [06](lesson/06-file/README.md) | Paths, context managers, CSV | Reading and writing data |
| [07](lesson/07-debug/README.md) | Exceptions, debugging, tests | Diagnosing calculations |
| [08](lesson/08-numpy/README.md) | Arrays, shapes, broadcasting, views | Vectorized calculations |
| [09](lesson/09-plot/README.md) | Figures, labels, units, saving plots | Scientific visualization |
| [10](lesson/10-numerical-error/README.md) | Roundoff, cancellation, finite differences | Error studies |
| [11](lesson/11-linear-algebra/README.md) | Solves, least squares, conditioning | Calibration |
| [12](lesson/12-cool/README.md) | A complete numerical workflow | Cooling simulation |

## Files and reproducibility

Every lesson contains its own instructions, runnable example, three exercises,
and worked solutions. Small datasets are synthetic; their provenance and units
are documented beside them. Examples that write files use the ignored `output/`
folder, never overwrite input datasets, and report their destinations. Rerunning
an example replaces its own generated output. Plots are saved as PNGs without
requiring a graphical desktop; open those files in your image viewer.

Dependencies are recorded in `pyproject.toml` and `uv.lock`; the Python version
is recorded in `.python-version`. The course targets Python 3.14. Continuous
integration checks it on Ubuntu and macOS; Windows is not verified.

## Verification

Run the shared course check from the project root:

```sh
uv run --locked python script/check_course.py
```

The checker works on a temporary copy of the lessons. It runs each lesson's
tests in a separate process and runs all 24 example and solution scripts. It
checks generated CSV and PNG output, and compares each script's printed output
with the expected-output blocks in the lesson pages marked
`<!-- check-output: example.py -->` (or `solution.py`). It then reruns six
scripts from the three lessons that produce files, using a different working
directory. These checks do not change files in your project's `output/` folder.
Blocks whose last digits depend on the platform's math library are not marked.

CI runs this same check with Python 3.14 on `ubuntu-latest` and `macos-latest`.
The individual test commands are also available when you want to focus on one
lesson:

```sh
uv run python -m unittest discover -s lesson/06-file -p 'test_*.py' -v
uv run python -m unittest discover -s lesson/07-debug -p 'test_*.py' -v
uv run python -m unittest discover -s lesson/10-numerical-error -p 'test_*.py' -v
uv run python -m unittest discover -s lesson/11-linear-algebra -p 'test_*.py' -v
uv run python -m unittest discover -s lesson/12-cool -p 'test_*.py' -v
```

Run tests in separate processes as shown: lesson folders intentionally use the
same simple filenames, rather than an installed package hierarchy. Passing a
test establishes only what that test measures. The numerical lessons compare
against analytic solutions, examine refinement trends, and distinguish code
correctness from numerical accuracy and the validity of a physical model.

## Reference documentation

- [Python tutorial](https://docs.python.org/3/tutorial/)
- [uv project environments](https://docs.astral.sh/uv/guides/projects/)
- [NumPy beginner's guide](https://numpy.org/doc/stable/user/absolute_beginners.html)
- [Matplotlib quick start](https://matplotlib.org/stable/users/explain/quick_start.html)

Project engineering instructions are recorded in [AGENTS.md](AGENTS.md).
