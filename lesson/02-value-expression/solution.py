# Exercise 1: ** is exponentiation. The printed unit follows from kg*(m/s)**2 = J.
mass_kg = 2.0
speed_m_per_s = 3.0
energy_j = 0.5 * mass_kg * speed_m_per_s**2
print(f"1. Kinetic energy: {energy_j:.3f} J")

# Exercise 2: division counts full groups; remainder counts the leftover samples.
sample_count = 17
group_size = 4
print(f"2. Full groups: {sample_count // group_size}")
print(f"2. Remaining samples: {sample_count % group_size}")

# Exercise 3: scale pressure by absolute temperature for fixed n and V.
pressure_initial_pa = 100000.0
temperature_initial_k = 250.0
temperature_final_k = 300.0
pressure_final_pa = pressure_initial_pa * temperature_final_k / temperature_initial_k
print(f"3. Final pressure: {pressure_final_pa:.2f} Pa")
print("3. Above initial pressure:", pressure_final_pa > pressure_initial_pa)
