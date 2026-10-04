# Lesson 1: Run Python and calculate with variables

[Course home](../../README.md) · [Next: values and expressions](../02-value-expression/README.md)

## What you will learn

- Run a saved Python program from a terminal.
- Display text and numerical results.
- Assign descriptive names to values and use them in arithmetic.
- Keep scientific units explicit when converting measurements.

No programming background is needed. Complete the environment setup in the
[course home](../../README.md) first. You need a text editor and a terminal.
A terminal is a window where you type commands and see their output.

## Your first program

A Python program is a plain-text file, usually ending in `.py`. Python is the
interpreter: the program that reads your instructions and carries them out.
Code means those instructions; a script is a file containing them.

Open [example.py](example.py) in your editor. The file is already saved here.
In a terminal whose working directory is this project's root folder, enter:

```sh
uv run python lesson/01-run-python/example.py
```

Press Enter to execute the command. `uv run` chooses the project environment,
`python` starts the interpreter, and the remaining text identifies the script.
The path uses `/` to separate folders. Do not type the surrounding code-fence
marks or a shell prompt such as `$`; they are not part of the command.

The working directory is the folder from which the command runs. If you get a
"can't open file" message, check that you are at the project root and that the
path matches exactly. The course home's [Start here](../../README.md#start-here)
section explains changing directories with `cd`.

## Display text with `print`

This is a complete Python statement:

```python
print("Hello, Python")
```

A statement is an instruction. `print` is a built-in function: an operation
Python already provides. The parentheses call that operation. The value inside
the parentheses is an argument, the input passed to it.
Here the argument is a string, a piece of text enclosed in quotation marks.
The quotes mark its beginning and end; they do not appear in the printed output.
We will write our own functions in lesson 5.

Use ordinary straight quotation marks, not typographic curly quotes. Single
quotes also work, but each string must end with the same kind it starts with.

## Give values names

```python
temperature_c = 25.0
temperature_k = temperature_c + 273.15
print("Temperature (K):", temperature_k)
```

The first line assigns a value to the name `temperature_c`. We call this name a
variable. The `=` sign means assignment; it does not assert a mathematical
equality. Python evaluates the expression on its right, then binds the name on
its left to the resulting value. The decimal point makes `25.0` a floating-point
number, a finite-precision representation for numbers with a fractional part.

The second line uses the already assigned value in an addition. Python executes
these statements from top to bottom. A name must be assigned before it is used.
Two arguments separated by a comma in `print` produce a label and value with a
space between them. Each call ends its output with a new line.

Names are case-sensitive: `temperature_c` and `Temperature_c` are different.
Use letters, digits, and underscores, but do not start a name with a digit.
Choose names such as `length_mm` that also communicate the unit.

## Arithmetic and units

| Python symbol | Meaning | Example |
|---|---|---|
| `+` | Add | `25.0 + 273.15` |
| `-` | Subtract | `300.0 - 273.15` |
| `*` | Multiply | `2.0 * 3.0` |
| `/` | Divide | `125.0 / 1000.0` |

Use parentheses to make evaluation order clear, for example
`(temperature_c + 273.15) / 300.0`. Multiplication and division normally occur
before addition and subtraction, as in elementary algebra.
Python requires an explicit multiplication sign: write `2.0 * length_m`, not
`2.0 length_m`. Division by zero fails; a time duration used as a denominator
must be nonzero.

The example converts `125.0` mm to `0.125` m, then divides by `5.0` s to find
an average speed of `0.025` m/s. Python does not attach physical dimensions to
these plain numbers. Dividing millimetres by seconds would run successfully but
produce a number in mm/s, not m/s. Unit checking is your responsibility.

For Celsius to kelvin, the conversion is an offset, `T_K = T_C + 273.15`.
For millimetres to metres, it is a scale, `L_m = L_mm / 1000`.
These are different operations even though both are called conversions.

## Comments and execution order

A `#` starts a comment extending to the end of that line. Python ignores the
comment when executing the program. Use comments to explain an assumption or
the reason for a conversion. Blank lines separate related groups of statements.
They do not change the calculation.

Changing a value in the editor does not change a running result automatically.
Save the file, then run the command again. Each execution starts the script
from its beginning; variables from an earlier run are not remembered.

## Expected output

The complete example prints:

<!-- check-output: example.py -->
```text
First scientific Python calculation
Temperature (C): 25.0
Temperature (K): 298.15
Length (m): 0.125
Average speed (m/s): 0.025
```

Before editing, predict what will change if `duration_s` becomes `10.0`. Try it,
save, run, and compare. Then restore `5.0`. This predict–run–explain cycle is a
useful way to learn a programming language.

## Common mistakes

- Leaving off a closing quote or parenthesis produces a syntax error: Python
  cannot parse the instruction. Check the indicated line and the one above it.
- Using a name before assigning it produces `NameError`; check spelling and order.
- Writing `"temperature_k"` prints the name as text. Use `temperature_k` without
  quotes to print its assigned value.
- Unsaved edits have no effect when you rerun the file.
- Numerically plausible output does not establish correct units or a valid model.

## Practice and recap

Attempt [the three exercises](exercise.md) before opening
[the worked solutions](solution.py). Run the solutions with:

```sh
uv run python lesson/01-run-python/solution.py
```

You can now run a script, print labelled values, assign names, and perform unit
conversions. In lesson 2 you will distinguish Python's basic value types and
format scientific results more clearly.
