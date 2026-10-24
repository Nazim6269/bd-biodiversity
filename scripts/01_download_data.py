from pygbif import occurrences as occ
import pandas as pd

result = occ.search(country="BD", taxonKey=212, limit=300)

print("Total bird records available in GBIF for Bangladesh:", result["count"])
print("Records downloaded now:", len(result["results"]))

# Convert the results into a table
df = pd.DataFrame(result["results"])
print()
print("Table shape (rows, columns):", df.shape)

# Look at key columns
cols = ["species", "decimalLatitude", "decimalLongitude", "year", "basisOfRecord"]
print()
print(df[cols].head(10))

# Data quality check
print()
print(df["species"].nunique(), "different species in this sample")
print()
print("Missing values in key columns:")
print(df[cols[:4]].isna().sum())

# Save the raw data
df.to_csv("data/raw_birds_sample.csv", index=False)
print()
print("Saved to data/raw_birds_sample.csv")
