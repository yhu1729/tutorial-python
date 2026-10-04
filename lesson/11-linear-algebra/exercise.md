# Exercises: linear algebra

Try each calculation before opening [solution.py](solution.py).

1. Solve `2*x - y = 1` and `x + y = 5` using `solve_system`. Verify both
   equations by substituting the returned values. Explain why `matrix * result`
   does not perform the same operation as `matrix @ result`.
2. Generate five displacements `[-2, -1, 0, 1, 2]` metres and exact forces from
   `F=4*x-0.5` newtons. Fit a slope and intercept, inspect the residual norm,
   and explain why floating-point residuals need not be exactly zero. Contrast
   this residual with the intentionally noisy example's residual.
3. Generate displacements `[1e6, 1e6+1, ..., 1e6+4]` and forces `3*x+2`.
   Compare the design matrix condition number before and after subtracting the
   mean displacement. Fit in centered coordinates, subtracting the mean force
   too, and transform the fitted intercept back. Derive
   `original_intercept = mean_force + centered_intercept - slope*mean_displacement`.
   Compare its error with a fit in the original coordinates. Explain why
   subtracting large quantities during this conversion still limits the
   accuracy of the original intercept.
