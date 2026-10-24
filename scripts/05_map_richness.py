import io
import zipfile
import requests
import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

df = pd.read_csv("data/clean_birds.csv")

# 1. Download Bangladesh border (Natural Earth, free) if not already saved
URL = "https://naturalearth.s3.amazonaws.com/10m_cultural/ne_10m_admin_0_countries.zip"
SHP = "data/ne_countries/ne_10m_admin_0_countries.shp"
try:
    world = gpd.read_file(SHP)
except Exception:
    print("Downloading country borders...")
    r = requests.get(URL, timeout=120)
    r.raise_for_status()
    zipfile.ZipFile(io.BytesIO(r.content)).extractall("data/ne_countries")
    world = gpd.read_file(SHP)

name_col = "NAME" if "NAME" in world.columns else "name"
bd = world[world[name_col] == "Bangladesh"]

# 2. Put records into 0.25 degree grid cells (about 28 km)
CELL = 0.25
df["cell_x"] = (np.floor(df["decimalLongitude"] / CELL) * CELL).round(2)
df["cell_y"] = (np.floor(df["decimalLatitude"] / CELL) * CELL).round(2)

grid = (df.groupby(["cell_x", "cell_y"])
          .agg(records=("gbifID", "count"), richness=("species", "nunique"))
          .reset_index())
grid["cx"] = grid["cell_x"] + CELL / 2
grid["cy"] = grid["cell_y"] + CELL / 2

print("Grid cells with data:", len(grid))
print()
print("Top 10 cells by species richness:")
print(grid.sort_values("richness", ascending=False).head(10)[["cell_x", "cell_y", "records", "richness"]])
print()
print("Cells with fewer than 10 records:", (grid["records"] < 10).sum())

grid.to_csv("data/grid_richness.csv", index=False)

# 3. Two maps: sampling effort and species richness
fig, axes = plt.subplots(1, 2, figsize=(13, 7))
for ax, col, title, cmap in [
    (axes[0], "records", "Number of records (sampling effort)", "YlOrRd"),
    (axes[1], "richness", "Observed species richness", "viridis"),
]:
    bd.boundary.plot(ax=ax, color="black", linewidth=0.8)
    sc = ax.scatter(grid["cx"], grid["cy"], c=grid[col], cmap=cmap,
                    s=140, marker="s", alpha=0.9)
    plt.colorbar(sc, ax=ax, shrink=0.7)
    ax.set_title(title)
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")

plt.tight_layout()
plt.savefig("figures/richness_map.png", dpi=150)
plt.close()
print()
print("Saved figures/richness_map.png")
