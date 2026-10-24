import time
import warnings
import pandas as pd
from pygbif import occurrences as occ

warnings.filterwarnings("ignore", category=DeprecationWarning)

YEARS = range(2010, 2026)      # 2010 to 2025
PAGES_PER_YEAR = 5             # 5 pages x 300 = up to 1500 records per year

KEEP = ["gbifID", "species", "genus", "family", "order",
        "decimalLatitude", "decimalLongitude", "coordinateUncertaintyInMeters",
        "year", "month", "stateProvince", "basisOfRecord", "datasetName"]

all_rows = []

for year in YEARS:
    for page in range(PAGES_PER_YEAR):
        res = occ.search(
            country="BD",
            taxonKey=212,
            year=year,
            hasCoordinate=True,
            hasGeospatialIssue=False,
            limit=300,
            offset=page * 300,
        )
        rows = res["results"]
        all_rows.extend(rows)
        print(f"Year {year}, page {page + 1}: got {len(rows)} records")
        if res["endOfRecords"]:
            break
        time.sleep(0.5)  # be polite to the server

df = pd.DataFrame(all_rows).reindex(columns=KEEP)

print()
print("Total records downloaded:", len(df))
print("Unique species:", df["species"].nunique())
print("Records without species name:", df["species"].isna().sum())
print()
print("Records per year:")
print(df["year"].value_counts().sort_index())

df.to_csv("data/raw_birds_large.csv", index=False)
print()
print("Saved to data/raw_birds_large.csv")
