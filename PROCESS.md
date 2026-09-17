# Development Process

## Tools used
- Python: for data fetching and visualisation generation
- Requests library: download rainfall raw dataset from Hong‑Kong Observatory open data website
- Matplotlib: create rainfall chart and export png image

## What I kept
1. Original downloaded csv rainfall dataset inside data folder. I keep the untouched raw data, so the source data is preserved for review.
2. Final output png chart saved in out folder. This visual result shows the rainfall distribution from the dataset.
3. Two main scripts: fetch.py for downloading data, plot.py for cleaning data and drawing chart. Separate files make functions clear.

## What I rejected & reasons
1. I considered combining fetch and plot logic into one single python file. I rejected this idea. Reason: splitting download and visualisation into two files makes debugging easier. If download fails, I do not need to run plotting code repeatedly.
2. Initially I planned to filter and modify raw csv values before saving. I rejected this change. Reason: raw dataset should remain unchanged. Any data processing only happens inside plot script, without altering source file.

## Key issues during development
- At first I added data folder and out folder into gitignore. This caused CI test failure because raw csv and generated png were not committed to repository.
- When drawing chart, I adjusted figure size and label text to make axis readable. Some styling options were tried; finally I chose simple clean style for the rainfall plot.
