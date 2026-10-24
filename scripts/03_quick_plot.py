import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/raw_birds_large.csv")

# Chart 1: records per year
counts = df["year"].value_counts().sort_index()
plt.figure(figsize=(8, 4))
plt.bar(counts.index, counts.values, color="seagreen")
plt.xlabel("Year")
plt.ylabel("Number of records")
plt.title("Bird records per year (Bangladesh, GBIF sample)")
plt.tight_layout()
plt.savefig("figures/records_per_year.png", dpi=150)
plt.close()

# Chart 2: simple map of all points
plt.figure(figsize=(6, 7))
plt.scatter(df["decimalLongitude"], df["decimalLatitude"], s=2, alpha=0.3, color="darkblue")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.title("Where the bird records are located")
plt.tight_layout()
plt.savefig("figures/points_map.png", dpi=150)
plt.close()

print("Saved figures/records_per_year.png and figures/points_map.png")
