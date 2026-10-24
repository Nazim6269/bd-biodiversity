#!/bin/bash
set -e
python scripts/02_download_large.py
python scripts/04_clean_data.py
python scripts/05_map_richness.py
python scripts/06_rarefaction.py
python scripts/07_summary.py
