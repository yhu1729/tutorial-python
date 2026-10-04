# Celsius and kelvin differ by an offset, not a scale factor.
temperature_c = 25.0
temperature_k = temperature_c + 273.15

# Millimetres to metres is a scale conversion.
length_mm = 125.0
length_m = length_mm / 1000.0

duration_s = 5.0
speed_m_per_s = length_m / duration_s

print("First scientific Python calculation")
print("Temperature (C):", temperature_c)
print("Temperature (K):", temperature_k)
print("Length (m):", length_m)
print("Average speed (m/s):", speed_m_per_s)
