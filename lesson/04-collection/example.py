# Synthetic temperatures in Celsius, chosen for a simple arithmetic mean.
temperature_list_c = [20.0, 21.0, 19.0]
temperature_list_c.append(22.0)
total_c = 0.0
for temperature_c in temperature_list_c:
    total_c = total_c + temperature_c
mean_c = total_c / len(temperature_list_c)

position_m = (1.0, 2.0, 3.0)
metadata = {"sample": "trial A", "unit": "deg C", "count": len(temperature_list_c)}

print("Readings:", temperature_list_c)
print("First reading:", temperature_list_c[0])
print("Last reading:", temperature_list_c[-1])
print("First two readings:", temperature_list_c[:2])
print(f"Mean temperature: {mean_c:.2f} deg C")
print("Position (m):", position_m)
print("Sample:", metadata["sample"])
print("Count:", metadata["count"])

# A second name shares the list; a shallow copy separates this flat list.
reading_alias = temperature_list_c
reading_copy = temperature_list_c.copy()
reading_alias[0] = 99.0
print("Original after alias change:", temperature_list_c)
print("Copy retains old readings:", reading_copy)
