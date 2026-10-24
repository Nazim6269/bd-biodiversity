import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/raw_birds_large.csv")
print("Start:", len(df), "records")

# 1. Remove records without a species name
df = df.dropna(subset=["species"])
print("After removing missing species:", len(df))

# 2. Remove records without coordinates
df = df.dropna(subset=["decimalLatitude", "decimalLongitude"])
print("After removing missing coordinates:", len(df))

# 3. Remove duplicate records
df = df.drop_duplicates(subset=["gbifID"])
print("After removing duplicates:", len(df))

# 4. Keep only points inside Bangladesh's rough bounding box
df = df[
    df["decimalLatitude"].between(20.5, 26.7)
    & df["decimalLongitude"].between(88.0, 92.8)
]
print("After keeping points inside Bangladesh box:", len(df))

# 5. Remove records with poor location accuracy (more than 10 km uncertainty)
df = df[(df["coordinateUncertaintyInMeters"].isna())
        | (df["coordinateUncertaintyInMeters"] <= 10000)]
print("After removing imprecise locations:", len(df))

# 6. Keep only observations of living birds (no fossils or specimens)
print()
print("Record types before filter:")
print(df["basisOfRecord"].value_counts())
df = df[df["basisOfRecord"].isin(["HUMAN_OBSERVATION", "MACHINE_OBSERVATION"])]
print("After keeping observations only:", len(df))

# Summary
print()
print("Final records:", len(df))
print("Final unique species:", df["species"].nunique())

# Save
df.to_csv("data/clean_birds.csv", index=False)

# Chart: top 15 most recorded species
top = df["species"].value_counts().head(15).sort_values()
plt.figure(figsize=(8, 6))
plt.barh(top.index, top.values, color="teal")
plt.xlabel("Number of records")
plt.title("Top 15 most recorded bird species (cleaned data)")
plt.tight_layout()
plt.savefig("figures/top_species.png", dpi=150)
plt.close()

print()
print("Saved data/clean_birds.csv and figures/top_species.png")
