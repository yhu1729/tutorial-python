# Exercises: numerical error

Attempt these in a scratch script before opening [solution.py](solution.py).

1. Compare `1e-12` with zero using `math.isclose`. First use only a relative
   tolerance of `1e-9`, then add an absolute tolerance of `2e-12`. Explain the
   different results and specify the units an absolute tolerance would have
   if these values represented temperatures.
2. Repeat the central-difference study at `x=0.5` with steps `0.2`, `0.1`,
   `0.05`, `0.025`, and `0.0125`. Print the error and
   `math.log2(previous_error / error)` for each available pair. Interpret all
   four estimated orders together; do not infer order from one pair alone.
3. At `x=1e-12`, calculate `sqrt(1+x)-1` directly and as
   `x/(sqrt(1+x)+1)`. Derive the second expression by rationalizing the first,
   compare with the leading Taylor term `x/2`, and explain the accuracy
   difference. The Taylor term is an approximation, not an exact reference.
