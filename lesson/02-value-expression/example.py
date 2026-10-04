sample_count = 5
mass_kg = 0.25
speed_m_per_s = 12.0
sample_name = "trial A"
calibration_valid = True

kinetic_energy_j = 0.5 * mass_kg * speed_m_per_s**2
amount_mol = 0.1
gas_constant_j_per_mol_k = 8.31446261815324
temperature_k = 300.0
volume_m3 = 2.0e-3
pressure_pa = amount_mol * gas_constant_j_per_mol_k * temperature_k / volume_m3

print(f"Sample: {sample_name}; count: {sample_count}; calibrated: {calibration_valid}")
print(f"Kinetic energy: {kinetic_energy_j:.2f} J")
print(f"Ideal-gas pressure: {pressure_pa:.2f} Pa")
print(f"Pressure in scientific notation: {pressure_pa:.3e} Pa")
print("Whole groups of two:", sample_count // 2)
print("Leftover samples:", sample_count % 2)
print("Pressure exceeds 100000 Pa:", pressure_pa > 100000.0)
print("0.1 + 0.2 == 0.3:", 0.1 + 0.2 == 0.3)
