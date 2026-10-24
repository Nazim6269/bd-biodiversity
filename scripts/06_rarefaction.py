import math
import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

df = pd.read_csv("data/clean_birds.csv")
bd = gpd.read_file("data/ne_countries/ne_10m_admin_0_countries.shp")
name_col = "NAME" if "NAME" in bd.columns else "name"
bd = bd[bd[name_col] == "Bangladesh"]

CELL = 0.25
N_RARE = 50   # standard sample size for comparing cells

df["cell_x"] = (np.floor(df["decimalLongitude"] / CELL) * CELL).round(2)
df["cell_y"] = (np.floor(df["decimalLatitude"] / CELL) * CELL).round(2)


def rarefy(counts, n):
    """Expected number of species in a random subsample of n records."""
    total = sum(counts)
    denom = math.comb(total, n)
    return sum(1 - math.comb(total - c, n) / denom for c in counts)


# 1. Rarefied richness per cell (only cells with enough records)
rows = []
for (x, y), g in df.groupby(["cell_x", "cell_y"]):
    counts = g["species"].value_counts().tolist()
    n_records = len(g)
    if n_records >= N_RARE:
        rows.append({"cx": x + CELL / 2, "cy": y + CELL / 2,
                     "records": n_records,
                     "observed": len(counts),
                     "rarefied": rarefy(counts, N_RARE)})

res = pd.DataFrame(rows)
print(f"Cells with at least {N_RARE} records:", len(res))
print()
print("Top 5 cells by rarefied richness:")
print(res.sort_values("rarefied", ascending=False).head(5).round(1))

# 2. How strongly does each measure depend on sampling effort?
ranks = res[["records", "observed", "rarefied"]].rank()
print()
print("Correlation with number of records (1 = fully effort-driven):")
print("  Observed richness:", round(ranks["records"].corr(ranks["observed"]), 2))
print("  Rarefied richness:", round(ranks["records"].corr(ranks["rarefied"]), 2))

res.to_csv("data/rarefied_richness.csv", index=False)

# 3. Map of rarefied richness
fig, ax = plt.subplots(figsize=(7, 8))
bd.boundary.plot(ax=ax, color="black", linewidth=0.8)
sc = ax.scatter(res["cx"], res["cy"], c=res["rarefied"], cmap="viridis",
                s=170, marker="s")
plt.colorbar(sc, ax=ax, shrink=0.7, label=f"Expected species in {N_RARE} records")
ax.set_title("Rarefied bird species richness")
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")
plt.tight_layout()
plt.savefig("figures/rarefied_map.png", dpi=150)
plt.close()

# 4. Species accumulation curve for the whole dataset
codes = pd.factorize(df["species"])[0]
rng = np.random.default_rng(42)
plt.figure(figsize=(8, 5))
for _ in range(5):
    perm = rng.permutation(codes)
    new_species = ~pd.Series(perm).duplicated().to_numpy()
    plt.plot(np.cumsum(new_species), color="seagreen", alpha=0.6)
plt.xlabel("Number of records")
plt.ylabel("Cumulative number of species")
plt.title("Species accumulation curve (5 random orderings)")
plt.tight_layout()
plt.savefig("figures/accumulation_curve.png", dpi=150)
plt.close()

print()
print("Saved figures/rarefied_map.png and figures/accumulation_curve.png")
